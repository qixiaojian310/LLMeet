from fastapi import APIRouter, Depends
from pydantic import BaseModel
from utils.jwt_utils import get_current_user, jwt_manager
from livekit import api
import os

class MeetingRequest(BaseModel):
    meetingId: str
    username: str

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