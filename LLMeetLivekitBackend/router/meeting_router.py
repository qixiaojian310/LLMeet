

import random
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from static.meeting import add_meeting, delete_meeting, find_meeting_by_id, find_meetings_by_user_id, add_user_to_meeting

from utils.jwt_utils import get_current_user

class MeetingCreateDto(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class MeetingCreateResponse(BaseModel):
    meeting_id: str
    create_time: datetime

class MeetingDeleteDto(BaseModel):
    meeting_id: str

class MeetingDeleteResponse(BaseModel):
    success: bool

class MeetingGetDto(BaseModel):
    meeting_id: str

class MeetingJoinDto(BaseModel):
    meeting_id: str

class MeetingJoinResponse(BaseModel):
    success: bool

class MeetingGetResponse(BaseModel):
    success: bool
    meeting: Optional[dict] = None

class MeetingListGetResponse(BaseModel):
    success: bool
    meetings: List[dict]

class Meeting:
    meeting_id: str
    title: str
    description: str
    creator_id: int
    created_at: datetime
    status: str
    start_time: datetime
    end_time: datetime

router = APIRouter(prefix="/bot", tags=["bot"])
@router.post("/meeting/create", response_model=MeetingCreateResponse)
async def create_meeting(data: MeetingCreateDto, user_id: int = Depends(get_current_user)):
    meeting_id = str(random.randint(100_000_000, 999_999_999))
    now = datetime.now()

    meeting = Meeting(
        meeting_id=meeting_id,
        title=data.title,
        description=data.description,
        creator_id=user_id,
        created_at=now,
        status="ready",
        start_time=data.start_time,
        end_time=data.end_time,
    )

    if add_meeting(meeting) == 0:
        raise HTTPException(status_code=500, detail="会议创建失败")

    if add_user_to_meeting(user_id, meeting_id, now) == 0:
        raise HTTPException(status_code=500, detail="加入会议失败")

    return MeetingCreateResponse(meeting_id=meeting_id, create_time=now)


@router.post("/meeting/delete", response_model=MeetingDeleteResponse)
async def delete_meeting(data: MeetingDeleteDto, user_id: int = Depends(get_current_user)):
    success = delete_meeting(data.meeting_id) > 0
    return MeetingDeleteResponse(success=success)


@router.post("/meeting/get", response_model=MeetingGetResponse)
async def get_meeting(data: MeetingGetDto, user_id: int = Depends(get_current_user)):
    meeting = find_meeting_by_id(data.meeting_id)
    return MeetingGetResponse(success=bool(meeting), meeting=meeting)


@router.post("/meeting/join", response_model=MeetingJoinResponse)
async def join_meeting(data: MeetingJoinDto, user_id: int = Depends(get_current_user)):
    inserted = add_user_to_meeting(user_id, data.meeting_id, datetime.now())
    return MeetingJoinResponse(success=inserted > 0)


@router.get("/meeting/getAll", response_model=MeetingListGetResponse)
async def get_all_meetings(user_id: int = Depends(get_current_user)):
    meetings = find_meetings_by_user_id(user_id)
    return MeetingListGetResponse(success=True, meetings=meetings)