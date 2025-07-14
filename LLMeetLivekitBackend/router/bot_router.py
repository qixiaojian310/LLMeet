import os
import asyncio
import subprocess
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, List

import pytz

from static.meeting import fetch_meeting_records, get_meeting_minutes
from utils.jwt_utils import get_current_user  # 你的 JWT 验证依赖
from utils.record_notificator import record_notificator
from utils.livekit_bot import run_bot, rooms, recording_sessions, bot_tasks
from livekit import api as livekit_api, rtc as livekit_rtc

import cv2
import numpy as np
from datetime import datetime
from loguru import logger
import wave
import time
import httpx

# -----------------------------
# 数据模型
# -----------------------------
class MeetingRequest(BaseModel):
    meeting_id: str
    username: str

class BotRequest(BaseModel):
    meeting_id: str

class StopRequest(BaseModel):
    meeting_id: str

class VideoPathRequest(BaseModel):
    path: str
    
class ConvertContentRequest(BaseModel):
    meeting_id: str

class VideoPathsRequest(BaseModel):
    meeting_id: str
    
# 定义请求结构体（与前面 /summarize 接口保持一致）
class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str
    speaker: str
# -----------------------------
# API 端点
# -----------------------------
router = APIRouter(prefix="/meeting", tags=["meeting"])

@router.post("/start_bot")
async def start_bot(req: BotRequest, username: str = Depends(get_current_user)):
    room_name = req.meeting_id
    if room_name in rooms and rooms[room_name].connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED:
        logger.info(f"[{room_name}] Bot 已连接，无需重复启动")
        return {"status": "already connected", "room": room_name}
    bot_tasks[room_name] = asyncio.create_task(run_bot(room_name, f"bot-{room_name}", str(username)))
    return {"status": "connecting", "room": room_name}

@router.post("/token")
async def get_token(request: MeetingRequest, username: str = Depends(get_current_user)):
    token = (
        livekit_api.AccessToken()
        .with_identity(str(username))
        .with_name(request.username)
        .with_grants(livekit_api.VideoGrants(room_join=True, room=request.meeting_id))
        .to_jwt()
    )
    return {"token": token}

@router.get("/video")
async def get_video(request: Request, path: str):
    print(path)
    fp = Path(path)
    if not fp.exists() or not fp.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    size = fp.stat().st_size
    range_hdr = request.headers.get("range")
    if range_hdr:
        start, end = 0, size - 1
        bytes_range = range_hdr.replace("bytes=", "").split("-")
        start = int(bytes_range[0])
        if bytes_range[1]: end = int(bytes_range[1])
        length = end - start + 1
        def iter_chunk():
            with open(fp, 'rb') as f:
                f.seek(start)
                yield f.read(length)
        return StreamingResponse(iter_chunk(), status_code=206, media_type="video/mp4", headers={
            "Content-Range": f"bytes {start}-{end}/{size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length)
        })
    else:
        def full():
            with open(fp, 'rb') as f:
                yield from f
        return StreamingResponse(full(), media_type="video/mp4", headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(size)
        })

@router.get("/recordings")
async def list_recordings():
    d = Path("recordings")
    if not d.exists():
        return {"recordings": []}
    recs = []
    for f in d.glob("**/final_*.mp4"):
        s = f.stat()
        recs.append({
            "filename": f.name,
            "size": s.st_size,
            "created_at": datetime.fromtimestamp(s.st_ctime, pytz.UTC).isoformat(),
            "modified_at": datetime.fromtimestamp(s.st_mtime, pytz.UTC).isoformat()
        })
    return {"recordings": sorted(recs, key=lambda x: x["created_at"], reverse=True)}

@router.get("/status")
async def status(meeting_id: Optional[str] = Query(None)):
    if meeting_id:
        rm = rooms.get(meeting_id)
        sess = recording_sessions.get(meeting_id, {})
        return {
            "room": meeting_id,
            "connected": bool(rm and rm.connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED),
            "active_recordings": len(sess),
            "recording_sessions": [
                {"session_id": sid, "participant": s.participant_identity,
                 "video_frames": s.video_frame_count, "audio_frames": s.audio_frame_count,
                 "duration": time.time() - s.start_time}
                for sid, s in sess.items()
            ]
        }
    return {"active_rooms": list(rooms.keys())}

@router.post("/recordingPath", response_model=List[Dict[str, str]])
async def recording_paths(req: VideoPathsRequest, username: str = Depends(get_current_user)):
    print(req.meeting_id)
    try:
        recs = fetch_meeting_records(req.meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return [{"path": r["minutes_path"], "username": r["username"]} for r in recs]

@router.post("/convert_content")
async def convert_content(req: ConvertContentRequest, username: str = Depends(get_current_user)):
    try:
        content = get_meeting_minutes(req.meeting_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return content

@router.post("/get_summarization")
async def get_summarization(req: List[TranscriptSegment]):
    try:
        # 请求转发到本地模型服务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:6007/summarize",
                json=[segment.dict() for segment in req],  # 注意：直接发送 List[Dict]
                timeout=60.0
            )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forwarding failed: {str(e)}")


@router.websocket("/ws/recordings")
async def websocket_endpoint(ws: WebSocket):
    await record_notificator.connect(ws)
    try:
        while True:
            # 如果需要双向通信，可以在这里 await ws.receive_text()
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        record_notificator.disconnect(ws)