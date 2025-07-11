import os
import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List
import httpx

from static.meeting import insert_meeting_minute
from utils.record_notificator import record_notificator
from livekit import api as livekit_api, rtc as livekit_rtc

import cv2
import numpy as np
from datetime import datetime, timezone
from loguru import logger
import wave
import time

# -----------------------------
# 全局状态：支持多房间多 Bot
# -----------------------------
rooms: Dict[str, livekit_rtc.Room] = {}
bot_tasks: Dict[str, asyncio.Task] = {}
recording_sessions: Dict[str, Dict[str, 'RecordingSession']] = {}

class RecordingSession:
    def __init__(self, participant_identity: str, session_id: str, meeting_id: str):
        self.participant_identity = participant_identity
        self.session_id = session_id
        self.meeting_id = meeting_id
        self.start_time = time.time()
        # 文件路径
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        temp_dir = Path(f"temps/{meeting_id}")
        temp_dir.mkdir(parents=True, exist_ok=True)
        rec_dir = Path(f"recordings/{meeting_id}")
        rec_dir.mkdir(parents=True, exist_ok=True)
        self.video_file = temp_dir / f"video_{participant_identity}_{timestamp}.avi"
        self.audio_file = temp_dir / f"audio_{participant_identity}_{timestamp}.wav"
        self.final_file = rec_dir / f"final_{participant_identity}_{timestamp}.mp4"

        self.video_writer = None
        self.audio_writer = None
        self.is_recording = False
        self.video_frame_count = 0
        self.audio_frame_count = 0
        self.expected_fps = 24
        self.audio_sample_rate = 48000
        self.final_files: List[Dict[str, str]] = []

    async def finalize_recording(self):
        self.is_recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        if self.audio_writer:
            self.audio_writer.close()
            self.audio_writer = None
        # 合并
        video_exists = self.video_file.exists() and self.video_file.stat().st_size > 0
        audio_exists = self.audio_file.exists() and self.audio_file.stat().st_size > 0
        if not (video_exists or audio_exists):
            logger.error(f"[Recording] 无效音视频: {self.session_id}")
            self.cleanup()
            return
        try:
            logger.info(f"[Recording] 合并开始: {self.final_file}")
            await self._merge_audio_video(video_exists, audio_exists)
            self.final_files.append({
                'meeting_id': self.meeting_id,
                'username': self.participant_identity,
                'path': str(self.final_file)
            })
        except Exception as e:
            logger.error(f"[Recording] 合并失败 {self.session_id}: {e}")
        finally:
            self.cleanup()
            logger.info(f"[Recording] 合并完成: {self.final_file}")

    async def _merge_audio_video(self, video_exists: bool, audio_exists: bool):
        # 获取时长
        def probe(path, s):
            cmd = ["ffprobe", "-v", "error", "-select_streams", f"{s}:0", 
                   "-show_entries", "stream=duration", 
                   "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
            r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return float(r.stdout.strip() or 0)
        vd = probe(self.video_file, 'v') if video_exists else 0
        ad = probe(self.audio_file, 'a') if audio_exists else 0
        atempo = None
        if vd and ad > vd:
            speed = ad / vd
            factors = []
            while speed > 2.0:
                factors.append(2.0)
                speed /= 2.0
            factors.append(speed)
            atempo = ",".join(f"atempo={f:.6f}" for f in factors)
        # 构造 ffmpeg
        cmd = ["ffmpeg", "-y", "-report", "-loglevel", "error"]
        if video_exists:
            cmd += ["-i", str(self.video_file)]
        if audio_exists:
            cmd += ["-i", str(self.audio_file)]
        if atempo:
            cmd += ["-filter:a", atempo]
        if video_exists:
            cmd += ["-c:v", "libx264"]
        if audio_exists:
            cmd += ["-c:a", "aac"]
        cmd += ["-preset", "medium", "-crf", "23", "-shortest", str(self.final_file)]
        loop = asyncio.get_event_loop()
        def run_ff():
            logger.info(f"[FFmpeg] 正在合并: {' '.join(cmd)}")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            logger.info(f"[FFmpeg 输出] {result.stdout}")
            return result
        res = await loop.run_in_executor(None, run_ff)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg 失败: {res.stderr}")

    def cleanup(self):
        try:
            tmp = self.video_file.parent
            if tmp.exists(): shutil.rmtree(tmp)
        except Exception as e:
            logger.warning(f"清理失败 {self.session_id}: {e}")

# -----------------------------
# Bot 主逻辑 + 自动停止
# -----------------------------
async def run_bot(room_name: str, bot_identity: str, username: str):
    logger.info(f"[{room_name}][{username}] Bot 启动")
    sessions: Dict[str, RecordingSession] = {}
    recording_sessions[room_name] = sessions
    # 生成 token
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    livekit_url = os.getenv("LIVEKIT_URL")
    if not (api_key and api_secret and livekit_url):
        logger.error("缺少 LiveKit 配置")
        return
    token = (
        livekit_api.AccessToken()
        .with_identity(bot_identity)
        .with_name(bot_identity)
        .with_grants(livekit_api.VideoGrants(room_join=True, room=room_name))
        .to_jwt()
    )
    # 连接
    room = livekit_rtc.Room()
    rooms[room_name] = room
    @room.on("participant_connected")
    def on_join(p):
        logger.info(f"[{room_name}] 用户加入: {p.identity}")
    @room.on("participant_disconnected")
    def on_leave(p):
        sid = f"{p.identity}_{p.sid}" 
        if sid in sessions:
            sessions[sid].is_recording = False
        if len(room.remote_participants) == 0:
            logger.info(f"[{room_name}] 房间空，自动关闭 Bot")
            asyncio.create_task(shutdown_bot(room_name))
    @room.on("track_subscribed")
    def on_track(track, pub, p):
        sid = f"{p.identity}_{p.sid}"
        if sid not in sessions:
            sessions[sid] = RecordingSession(p.identity, sid, room_name)
        sess = sessions[sid]
        sess.is_recording = True
        if track.kind == livekit_rtc.TrackKind.KIND_VIDEO:
            asyncio.create_task(record_video(track, sess))
        else:
            asyncio.create_task(record_audio(track, sess))
    try:
        await room.connect(livekit_url, token)
    except Exception as e:
        logger.error(f"连接失败 {room_name}: {e}")
        return
    try:
        while True:
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        await room.disconnect()

async def shutdown_bot(room_name: str):
    task = bot_tasks.get(room_name)
    if task:
        task.cancel()
        try: await task
        except: pass
    sessions = recording_sessions.get(room_name, {})
    await asyncio.gather(*(s.finalize_recording() for s in sessions.values()), return_exceptions=True)
    for s in sessions.values():
        for rec in s.final_files:
            insert_meeting_minute(rec['meeting_id'], rec['username'], rec['path'])
    room = rooms.get(room_name)
    if room: await room.disconnect()
    # 2. 调用 AI 服务器做转写
    files_to_send = [
        (
            "files",
            (
                Path(rec["path"]).name,                 # filename
                open(rec["path"], "rb"),               # file obj
                "video/mp4"                            # MIME type
            )
        )
        for rec in recording_sessions[room_name].values()
        for rec in rec.final_files
    ]

    # 如果想传 num_speakers，可作为 query param 或 form field
    data = {"num_speakers": 3}

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            resp = await client.post(
                "http://localhost:8000/transcribe",
                data=data,
                files=files_to_send
            )
            resp.raise_for_status()
            ai_result = resp.json()  # {'language':..., 'segments':[...]}

    except Exception as e:
        logger.error(f"[{room_name}] 调用 /transcribe 失败：{e}")
        return

    # 3. 将 AI 转写结果写入会议纪要
    for seg in ai_result.get("segments", []):
        insert_meeting_minute(
            meeting_id=room_name,
            username=seg["speaker"],  # 说话人标签
            content=seg["text"]
        )
    logger.info(f"[{room_name}] 已将转写结果写入会议纪要")
    bot_tasks.pop(room_name, None)
    rooms.pop(room_name, None)
    recording_sessions.pop(room_name, None)
    logger.info(f"[{room_name}] Bot 已完全停止")
    await record_notificator.broadcast({
        "event": "merge_complete",
        "meeting_id": room_name,
    })

# 录制细节
async def record_video(track, session: RecordingSession):
    stream = livekit_rtc.VideoStream(track, format=livekit_rtc.VideoBufferType.RGB24)
    ts_list, last_ts, buffer = [], None, []
    try:
        async for ev in stream:
            if not session.is_recording: break
            ts = ev.timestamp_us / 1e6
            if last_ts is not None: ts_list.append(ts - last_ts)
            last_ts = ts
            arr = np.frombuffer(ev.frame.data, np.uint8).reshape((ev.frame.height, ev.frame.width, 3))
            frame = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (1920,1080))
            buffer.append(frame)
            if not session.video_writer and len(ts_list) >= 30:
                fps = 1/(sum(ts_list)/len(ts_list))
                h,w,_ = frame.shape
                session.video_writer = cv2.VideoWriter(str(session.video_file), cv2.VideoWriter_fourcc(*"MJPG"), fps, (w,h))
                for f in buffer: session.video_writer.write(f)
                session.video_frame_count += len(buffer)
                buffer.clear()
            elif session.video_writer:
                session.video_writer.write(frame)
                session.video_frame_count += 1
    finally:
        await stream.aclose()

async def record_audio(track, session: RecordingSession):
    stream = livekit_rtc.AudioStream(track, sample_rate=session.audio_sample_rate, num_channels=2)
    session.audio_writer = wave.open(str(session.audio_file), 'wb')
    session.audio_writer.setnchannels(2)
    session.audio_writer.setsampwidth(2)
    session.audio_writer.setframerate(session.audio_sample_rate)
    try:
        async for ev in stream:
            if not session.is_recording: break
            if ev.frame and ev.frame.data:
                session.audio_writer.writeframes(ev.frame.data.tobytes())
                session.audio_frame_count += 1
    finally:
        await stream.aclose()
