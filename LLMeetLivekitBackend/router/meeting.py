from fastapi import APIRouter, Depends
from pydantic import BaseModel
from utils.jwt_utils import get_current_user, jwt_manager
from livekit import api
import os

class MeetingRequest(BaseModel):
    meetingId: str
    username: str
class StartRecordingRequest(BaseModel):
    meetingId: str

router = APIRouter(prefix="/meeting")  # 这里注意不是 app，是 router！
@router.post("/token")
async def get_wordbook_list(
    request: MeetingRequest, user_id: int = Depends(get_current_user)
):
    # will automatically use the LIVEKIT_API_KEY and LIVEKIT_API_SECRET env vars
    token = api.AccessToken() \
        .with_identity(user_id) \
        .with_name(request.username) \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=request.meetingId,
        )).to_jwt()
        
    return {
        "token": token,
    }

@router.post("/start-recording")
async def start_recording(
    request: StartRecordingRequest,
    user_id: int = Depends(get_current_user)
):
    lkapi = api.LiveKitAPI(
        host=os.environ.get("LIVEKIT_HOST", "http://localhost:7880"),
        api_key=os.environ["LIVEKIT_API_KEY"],
        api_secret=os.environ["LIVEKIT_API_SECRET"]
    )

    egress_req = api.RoomCompositeEgressRequest(
        room_name=request.meetingId,
        layout="speaker",
        preset=api.EncodingOptionsPreset.H264_720P_30,
        audio_only=False,
        file_outputs=[
            api.EncodedFileOutput(
                filepath=f"/tmp/recordings/{request.meetingId}-{user_id}.mp4"
            )
        ]
    )

    try:
        res = await lkapi.egress.start_room_composite_egress(egress_req)
        return {
            "egress_id": res.egress_id,
            "status": res.status.name
        }
    except Exception as e:
        return {
            "error": str(e)
        }