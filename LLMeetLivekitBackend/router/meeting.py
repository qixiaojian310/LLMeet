import os
import asyncio
import subprocess
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

from utils.jwt_utils import get_current_user  # 你的 JWT 验证依赖
from livekit import api as livekit_api, rtc as livekit_rtc

import cv2
import numpy as np
from datetime import datetime
from loguru import logger
import wave
import threading
import time

# -----------------------------
# 1. 定义 Router 和 数据模型
# -----------------------------
router = APIRouter(prefix="/meeting", tags=["meeting"])

class MeetingRequest(BaseModel):
    meetingId: str
    username: str

class BotRequest(BaseModel):
    meetingId: str

# 录制会话管理器
class RecordingSession:
    def __init__(self, participant_identity: str, session_id: str):
        self.participant_identity = participant_identity
        self.session_id = session_id
        self.start_time = time.time()
        self.video_file = None
        self.audio_file = None
        self.video_writer = None
        self.audio_writer = None
        base_dir = os.path.join(os.getcwd(), "recordings", session_id)
        os.makedirs(base_dir, exist_ok=True)
        self.temp_dir = base_dir
        self.is_recording = False
        
        # 同步标记
        self.video_frame_count = 0
        self.audio_frame_count = 0
        self.expected_fps = 24
        self.audio_sample_rate = 48000
        
        # 创建临时文件路径
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.video_file = os.path.join(self.temp_dir, f"video_{participant_identity}_{timestamp}.avi")
        self.audio_file = os.path.join(self.temp_dir, f"audio_{participant_identity}_{timestamp}.wav")
        self.final_file = f"recordings/final_{participant_identity}_{timestamp}.mp4"
        
        # 确保输出目录存在
        os.makedirs("recordings", exist_ok=True)
        
    async def finalize_recording(self):
        """使用 FFmpeg 合并音视频并确保同步"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        # 关闭写入器
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            
        if self.audio_writer:
            self.audio_writer.close()
            self.audio_writer = None
        
        # 检查文件是否存在
        video_exists = os.path.exists(self.video_file) and os.path.getsize(self.video_file) > 0
        audio_exists = os.path.exists(self.audio_file) and os.path.getsize(self.audio_file) > 0
        
        if not video_exists and not audio_exists:
            logger.error(f"[Recording] 没有有效的音视频文件可以合并: {self.participant_identity}")
            self.cleanup()
            return
        
        try:
            await self._merge_audio_video()
            logger.info(f"[Recording] 录制完成并保存到: {self.final_file}")
        except Exception as e:
            logger.error(f"[Recording] 合并音视频失败: {e}")
        finally:
            
    # 插入数据库
            from ..static.memory import insert_meeting_minute
            inserted_id = insert_meeting_minute(
                meeting_id=self.meeting_id,
                minute_record_path=self.final_file,
                content=""   # 如果后续要填 content，可以再改
            )
            if inserted_id:
                logger.info(f"[Recording] 数据库记录插入成功，minutes_id={inserted_id}")
            else:
                logger.warning(f"[Recording] 数据库记录插入失败：meeting_id={self.meeting_id}")
        #     self.cleanup()
    

    async def _merge_audio_video(self):
        """使用 FFmpeg 合并音视频（同步 subprocess.run + run_in_executor）"""
        video_exists = os.path.exists(self.video_file) and os.path.getsize(self.video_file) > 0
        audio_exists = os.path.exists(self.audio_file) and os.path.getsize(self.audio_file) > 0

        if video_exists and audio_exists:
            cmd = [
                'ffmpeg', '-y', '-report', '-loglevel', 'verbose',
                '-i', self.video_file,
                '-i', self.audio_file,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'medium',
                '-crf', '23',
                '-shortest',
                '-vsync', 'cfr',
                self.final_file
            ]
        elif video_exists:
            cmd = [
                'ffmpeg', '-y', '-report', '-loglevel', 'verbose',
                '-i', self.video_file,
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                self.final_file
            ]
        elif audio_exists:
            cmd = [
                'ffmpeg', '-y', '-report', '-loglevel', 'verbose',
                '-i', self.audio_file,
                '-c:a', 'aac',
                self.final_file
            ]
        else:
            raise Exception("没有可用的音视频文件")

        logger.debug(f"[Recording] 准备执行 FFmpeg: {' '.join(cmd)}")

        # 在后台线程用同步 subprocess.run 执行
        loop = asyncio.get_event_loop()
        def _run():
            return subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        result = await loop.run_in_executor(None, _run)

        # 日志输出
        logger.debug(f"[Recording] FFmpeg 返回码: {result.returncode}")
        logger.debug(f"[Recording] FFmpeg stdout: {result.stdout!r}")
        logger.debug(f"[Recording] FFmpeg stderr: {result.stderr!r}")

        if result.returncode != 0:
            raise Exception(f"FFmpeg 执行失败 (code={result.returncode})，stderr:\n{result.stderr}")

        logger.info(f"[Recording] FFmpeg 合并成功: {self.final_file}")

    def cleanup(self):
        """清理临时文件"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.debug(f"[Recording] 清理临时目录: {self.temp_dir}")
        except Exception as e:
            logger.warning(f"[Recording] 清理临时文件失败: {e}")

# 全局变量
room: Optional[livekit_rtc.Room] = None
recording_sessions: Dict[str, RecordingSession] = {}
bot_task: Optional[asyncio.Task] = None

# -----------------------------
# 2. Bot 主逻辑：run_bot()
# -----------------------------
async def run_bot(room_name: str, bot_identity: str):
    """
    优化版本的 Bot，支持音视频同步录制
    """
    global room, recording_sessions

    # 2.1 生成 Token
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")
    livekit_url = os.environ.get("LIVEKIT_URL")

    if not (api_key and api_secret and livekit_url):
        logger.error("未配置 LIVEKIT_API_KEY / LIVEKIT_API_SECRET / LIVEKIT_URL")
        return

    token = (
        livekit_api.AccessToken()
        .with_identity(bot_identity)
        .with_name(bot_identity)
        .with_grants(
            livekit_api.VideoGrants(
                room_join=True,
                room=room_name,
            )
        )
        .to_jwt()
    )

    # 2.2 创建 Room 实例
    room = livekit_rtc.Room()

    # 2.3 参与者连接事件
    @room.on("participant_connected")
    def on_participant_connected(participant: livekit_rtc.RemoteParticipant):
        logger.info(f"[Bot] 参与者连接 → sid={participant.sid}, identity={participant.identity}")

    # 2.4 参与者断开事件
    @room.on("participant_disconnected")
    def on_participant_disconnected(participant: livekit_rtc.RemoteParticipant):
        logger.info(f"[Bot] 参与者断开 → identity={participant.identity}")
        # 结束该参与者的录制会话
        session_id = f"{participant.identity}_{participant.sid}"
        if session_id in recording_sessions:
            asyncio.create_task(recording_sessions[session_id].finalize_recording())
            del recording_sessions[session_id]

    # 2.5 轨道订阅事件
    @room.on("track_subscribed")
    def on_track_subscribed(
        track: livekit_rtc.Track,
        publication: livekit_rtc.RemoteTrackPublication,
        participant: livekit_rtc.RemoteParticipant,
    ):
        session_id = f"{participant.identity}_{participant.sid}"
        
        # 获取或创建录制会话
        if session_id not in recording_sessions:
            recording_sessions[session_id] = RecordingSession(participant.identity, session_id)
        
        session = recording_sessions[session_id]
        session.is_recording = True

        if track.kind == livekit_rtc.TrackKind.KIND_VIDEO:
            logger.info(f"[Bot] 订阅视频轨道 ← {participant.identity}")
            asyncio.create_task(record_video(track, session))
            
        elif track.kind == livekit_rtc.TrackKind.KIND_AUDIO:
            logger.info(f"[Bot] 订阅音频轨道 ← {participant.identity}")
            asyncio.create_task(record_audio(track, session))

    # 2.6 轨道取消订阅事件
    @room.on("track_unsubscribed")
    def on_track_unsubscribed(
        track: livekit_rtc.Track,
        publication: livekit_rtc.RemoteTrackPublication,
        participant: livekit_rtc.RemoteParticipant,
    ):
        logger.info(f"[Bot] 取消订阅轨道 ← {participant.identity}, kind={track.kind}")

    # 2.7 连接到房间
    try:
        logger.info(f"[Bot] 正在连接房间 → {room_name}")
        await room.connect(livekit_url, token)
        logger.info(f"[Bot] 已加入房间：{room_name}")
    except Exception as exc:
        logger.error(f"[Bot] 无法加入房间: {exc}")
        return

    # 2.8 列出现有参与者
    for identity, participant in room.remote_participants.items():
        logger.info(f"[Bot] 现有参与者 identity={identity}")

    # 2.9 保持连接
    try:
        while True:
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        logger.info("[Bot] 收到取消信号，开始清理...")
        
        # 结束所有录制会话
        tasks = []
        for session in recording_sessions.values():
            tasks.append(session.finalize_recording())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        recording_sessions.clear()
        await room.disconnect()
        return

async def record_video(track: livekit_rtc.Track, session: RecordingSession):
    """录制视频轨道"""
    
    video_stream = livekit_rtc.VideoStream(track, format=livekit_rtc.VideoBufferType.RGB24)
    target_size = (1920, 1080)
        # 用于测帧率
    ts_list = []
    last_ts = None
    buffer_frames = []
    try:
        logger.info(f"[Video] 开始录制视频: {session.video_file}")
        
        async for ev in video_stream:
                if not session.is_recording:
                    break

                frame = ev.frame  # VideoFrame
                # 获取时间戳（秒）
                ts = ev.timestamp_us / 1_000_000  
                if last_ts is not None:
                    ts_list.append(ts - last_ts)
                last_ts = ts

                # 解码并缓存原始帧
                arr = np.frombuffer(frame.data, dtype=np.uint8)
                arr = arr.reshape((frame.height, frame.width, 3))
                bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
                bgr = cv2.resize(bgr, target_size)
                buffer_frames.append(bgr)

                # 测够 30 帧之后，初始化 VideoWriter
                if session.video_writer is None and len(ts_list) >= 30:
                    avg_interval = sum(ts_list) / len(ts_list)
                    fps = 1.0 / avg_interval if avg_interval > 0 else session.expected_fps
                    logger.info(f"[Video] 检测到真实 fps={fps:.2f}，初始化 VideoWriter")

                    h, w, _ = buffer_frames[0].shape
                    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                    session.video_writer = cv2.VideoWriter(
                        session.video_file,
                        fourcc,
                        fps,
                        (w, h),
                    )
                    if not session.video_writer.isOpened():
                        logger.error("[Video] VideoWriter 初始化失败")
                        return

                    # 把缓存的帧一次写入
                    for f in buffer_frames:
                        session.video_writer.write(f)
                    session.video_frame_count += len(buffer_frames)
                    buffer_frames.clear()

                # 如果已经初始化，直接写入
                if session.video_writer is not None:
                    session.video_writer.write(bgr)
                    session.video_frame_count += 1

                if session.video_frame_count % 240 == 0:
                    logger.debug(f"[Video] 已录制 {session.video_frame_count} 帧")
    except asyncio.CancelledError:
        logger.info(f"[Video] 视频录制被取消: {session.participant_identity}")
    except Exception as exc:
        logger.error(f"[Video] 视频录制错误: {exc}")
    finally:
        try:
            await video_stream.aclose()
        except Exception as e:
            logger.warning(f"[Video] 关闭视频流时出错: {e}")
        
        logger.info(f"[Video] 视频录制结束: {session.participant_identity}, 总帧数: {session.video_frame_count}")

async def record_audio(track: livekit_rtc.Track, session: RecordingSession):
    """录制音频轨道"""
    audio_stream = livekit_rtc.AudioStream(
        track, sample_rate=session.audio_sample_rate, num_channels=2
    )
    
    try:
        logger.info(f"[Audio] 开始录制音频: {session.audio_file}")
        
        # 初始化音频写入器
        session.audio_writer = wave.open(session.audio_file, "wb")
        session.audio_writer.setnchannels(2)
        session.audio_writer.setsampwidth(2)  # 16-bit
        session.audio_writer.setframerate(session.audio_sample_rate)
        
        await asyncio.sleep(0.1)  # 等待音频流准备
        
        async for frame_event in audio_stream:
            if not session.is_recording:
                break
                
            if frame_event.frame and frame_event.frame.data:
                session.audio_writer.writeframes(frame_event.frame.data.tobytes())
                session.audio_frame_count += 1
                
                # 定期记录进度
                if session.audio_frame_count % 2400 == 0:  # 约每50ms * 2400 = 2分钟
                    logger.debug(f"[Audio] {session.participant_identity} 已录制 {session.audio_frame_count} 音频帧")
                    
    except asyncio.CancelledError:
        logger.info(f"[Audio] 音频录制被取消: {session.participant_identity}")
    except Exception as exc:
        logger.error(f"[Audio] 音频录制错误: {exc}")
    finally:
        try:
            await audio_stream.aclose()
        except Exception as e:
            logger.warning(f"[Audio] 关闭音频流时出错: {e}")
        
        logger.info(f"[Audio] 音频录制结束: {session.participant_identity}, 总帧数: {session.audio_frame_count}")

# -----------------------------
# 3. API 端点
# -----------------------------
@router.post("/start_bot")
async def start_bot(request: BotRequest, user_id: int = Depends(get_current_user)):
    """启动录制 Bot"""
    global room, bot_task

    if room is not None and room.connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED:
        return {"status": "already connected"}

    bot_identity = "recording-bot"
    room_name = request.meetingId

    bot_task = asyncio.create_task(run_bot(room_name, bot_identity))

    return {"status": "connecting", "room": room_name, "identity": bot_identity}

@router.post("/stop_bot")
async def stop_bot(user_id: int = Depends(get_current_user)):
    """停止录制 Bot"""
    global room, recording_sessions, bot_task

    if room is not None and room.connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED:
        if bot_task:
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
            bot_task = None
        
        # 等待所有录制会话完成
        if recording_sessions:
            logger.info(f"[Bot] 正在完成 {len(recording_sessions)} 个录制会话...")
            tasks = [session.finalize_recording() for session in recording_sessions.values()]
            await asyncio.gather(*tasks, return_exceptions=True)
            recording_sessions.clear()
        
        await room.disconnect()
        room = None
        return {"status": "disconnected"}

    return {"status": "not connected"}

@router.post("/token")
async def get_token(
    request: MeetingRequest, user_id: int = Depends(get_current_user)
):
    """生成 LiveKit 访问令牌"""
    token = livekit_api.AccessToken() \
        .with_identity(str(user_id)) \
        .with_name(request.username) \
        .with_grants(livekit_api.VideoGrants(
            room_join=True,
            room=request.meetingId,
        )).to_jwt()
    return {"token": token}

@router.get("/recordings")
async def list_recordings(user_id: int = Depends(get_current_user)):
    """列出所有录制文件"""
    recordings_dir = Path("recordings")
    if not recordings_dir.exists():
        return {"recordings": []}
    
    recordings = []
    for file_path in recordings_dir.glob("final_*.mp4"):
        stat = file_path.stat()
        recordings.append({
            "filename": file_path.name,
            "size": stat.st_size,
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
        })
    
    return {"recordings": sorted(recordings, key=lambda x: x["created_at"], reverse=True)}

@router.get("/status")
async def get_status(user_id: int = Depends(get_current_user)):
    """获取录制状态"""
    global room, recording_sessions
    
    status = {
        "connected": room is not None and room.connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED,
        "room_name": getattr(room, 'name', None) if room else None,
        "active_recordings": len(recording_sessions),
        "recording_sessions": []
    }
    
    for session_id, session in recording_sessions.items():
        status["recording_sessions"].append({
            "session_id": session_id,
            "participant": session.participant_identity,
            "video_frames": session.video_frame_count,
            "audio_frames": session.audio_frame_count,
            "duration": time.time() - session.start_time
        })
    
    return status