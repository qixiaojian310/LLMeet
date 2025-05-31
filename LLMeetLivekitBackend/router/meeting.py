import os
import asyncio

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from utils.jwt_utils import get_current_user  # 你的 JWT 验证依赖
from livekit import api as livekit_api, rtc as livekit_rtc

import cv2
import numpy as np
from datetime import datetime
from loguru import logger

# -----------------------------
# 1. 定义 Router 和 数据模型
# -----------------------------
router = APIRouter(prefix="/meeting", tags=["meeting"])

class MeetingRequest(BaseModel):
    meetingId: str
    username: str

class BotRequest(BaseModel):
    meetingId: str

# 全局保存当前的 Room 引用（单例 Bot）
room: Optional[livekit_rtc.Room] = None
recorders: dict[str, asyncio.Task] = {}      # pub_sid ➜ record_task


# -----------------------------
# 2. Bot 主逻辑：run_bot()
# -----------------------------
async def run_bot(room_name: str, bot_identity: str):
    """
    1. 生成一个临时的 LiveKit Access Token
    2. 创建 Room()，注册事件回调
    3. await room.connect(...)
    4. 持续监听，直到任务被取消
    """
    global room

    # 2.1 生成 Token
    # 注意：这里假设你在环境变量里设置了 LIVEKIT_API_KEY、LIVEKIT_API_SECRET、LIVEKIT_URL
    api_key = os.environ.get("LIVEKIT_API_KEY")
    api_secret = os.environ.get("LIVEKIT_API_SECRET")
    livekit_url = os.environ.get("LIVEKIT_URL")  # e.g. "wss://livekit.example.com:7880"

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

    # 2.2 创建 Room 实例（**不要**传 loop 参数，让 SDK 自动使用当前 EventLoop）
    room = livekit_rtc.Room()

    # 2.3 注册 “participant_connected” 事件
    @room.on("participant_connected")
    def on_participant_connected(participant: livekit_rtc.RemoteParticipant):
        logger.info(f"[Bot] Participant connected → sid={participant.sid}, identity={participant.identity}")

    # 2.4 注册 “track_subscribed” 事件（这里只演示基于 OpenCV VideoWriter 的录制）
    @room.on("track_subscribed")
    def on_track_subscribed(
        track: livekit_rtc.Track,
        publication: livekit_rtc.RemoteTrackPublication,
        participant: livekit_rtc.RemoteParticipant,
    ):
        # 仅处理视频轨道
        if track.kind == livekit_rtc.TrackKind.KIND_VIDEO:
            logger.info(f"[Bot] 已订阅到视频轨道，来自 → {participant.identity}")

            # 这里指定 VideoStream 输出为 RGB24，每帧的数据就是 RGB24 原始字节
            video_stream = livekit_rtc.VideoStream(track, format=livekit_rtc.VideoBufferType.RGB24)
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("recordings", exist_ok=True)
            filename = f"recordings/recording_{participant.identity}_{now_str}.avi"

            async def record_task():
                logger.info(f"[Bot] 开始录制到文件：{filename}")
                writer = None

                try:
                    # 异步遍历每一帧
                    async for frame_event in video_stream:
                        buffer = frame_event.frame
                        # buffer.data 是一个 memoryview，长度 = width * height * 3（RGB24）
                        # 先转为 numpy，再 reshape 成 (height, width, 3)，便于 OpenCV 操作
                        arr = np.frombuffer(buffer.data, dtype=np.uint8)
                        arr = arr.reshape((buffer.height, buffer.width, 3))  # RGB

                        # OpenCV 的 VideoWriter 需要 BGR，所以先把 RGB 转 BGR
                        bgr_frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

                        # 第一次拿到帧时，初始化 VideoWriter
                        if writer is None:
                            h, w, _ = bgr_frame.shape
                            # 使用 mp4v 编码，24 帧率
                            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                            writer = cv2.VideoWriter(
                                filename,
                                fourcc,
                                24.0,
                                (w, h),
                            )
                            if not writer.isOpened():
                                logger.error("[Bot] VideoWriter 打开失败，请检查编解码器支持")
                                return

                        writer.write(bgr_frame)

                except asyncio.CancelledError:            # stop_bot 调用了 task.cancel()
                        pass                                   # 跳到 finally
                except Exception as exc:
                    logger.error(f"[Bot] 录制过程中发生错误：{exc}")
                finally:
                    await video_stream.stop()              # 主动关闭底层 track
                    # 结束后释放 VideoWriter
                    if writer:
                        writer.release()
                    logger.info(f"[Bot] 录制结束：{filename}")

            # 把 record_task 丢到当前运行 loop 去执行
            recorders[publication.sid] = asyncio.get_running_loop().create_task(record_task())

    # 2.5 真正连接到 LiveKit 房间
    try:
        logger.info(f"[Bot] 正在连接房间 → {room_name}")
        await room.connect(livekit_url, token)
        logger.info(f"[Bot] 已加入房间：{room_name}")
    except Exception as exc:
        logger.error(f"[Bot] 无法加入房间: {exc}")
        return

    # 2.6 可选：列出房间里已经存在的远端参与者／轨道
    for identity, participant in room.remote_participants.items():
        logger.info(f"[Bot] 现有参与者 identity={identity}")
        for pub_sid, publication in participant.track_publications.items():
            logger.info(f"    └ track publication → {publication}")

    # 2.7 保持本协程不退出（只要不被取消，就一直 sleep）
    try:
        while True:
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        # 收到取消信号后，断开并退出
        logger.info("[Bot] 收到取消信号，开始断开房间")
        await room.disconnect()
        return


# -----------------------------
# 3. POST /meeting/start_bot
# -----------------------------
@router.post("/start_bot")
async def start_bot(request: BotRequest, user_id: int = Depends(get_current_user)):
    """
    以当前 user_id 做鉴权，收到房间名后：如果 Bot 尚未连接，则在后台启动 run_bot() 去加入房间并监听；
    如果已经连接，直接返回 "already connected"。
    """
    global room

    # 3.1 检查是否已经存在有效连接
    if room is not None and room.connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED:
        return {"status": "already connected"}

    # 3.2 调用 run_bot(room_name, bot_identity)，用 asyncio.create_task 在后台执行
    #     这里我们暂时将 bot_identity 固定写成 "python-bot"，也可以从请求里改成动态
    bot_identity = "python-bot"
    room_name = request.meetingId

    # 在当前运行 loop 中创建后台任务
    asyncio.get_running_loop().create_task(run_bot(room_name, bot_identity))

    return {"status": "connecting", "room": room_name, "identity": bot_identity}


# -----------------------------
# 4. POST /meeting/stop_bot
# -----------------------------
@router.post("/stop_bot")
async def stop_bot(user_id: int = Depends(get_current_user)):
    """
    如果 room 存在且已连接，就断开并清空 room 引用；否则返回 "not connected"。
    """
    global room, recorders

    if room is not None and room.connection_state == livekit_rtc.ConnectionState.CONN_CONNECTED:
       # ① 取消所有录像任务
        for task in recorders.values():
            logger.info(f"[Bot] 取消录像任务中：{task}")
            task.cancel()
        # 等所有任务跑到 finally: writer.release()
        await asyncio.gather(*recorders.values(), return_exceptions=True)
        recorders.clear()

        # ② 正常断房间
        await room.disconnect()
        room = None
        return {"status": "disconnected"}

    return {"status": "not connected"}


# -----------------------------
# 5. POST /meeting/token
# -----------------------------
@router.post("/token")
async def get_token(
    request: MeetingRequest, user_id: int = Depends(get_current_user)
):
    token = livekit_api.AccessToken() \
        .with_identity(user_id) \
        .with_name(request.username) \
        .with_grants(livekit_api.VideoGrants(
            room_join=True,
            room=request.meetingId,
        )).to_jwt()
    return {"token": token}
