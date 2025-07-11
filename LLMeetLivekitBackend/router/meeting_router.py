

import random
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
from static.user import get_user_timezone
from static.meeting import add_meeting, delete_meeting, find_meeting_by_id, find_meetings_by_username, add_user_to_meeting, find_recorded_meetings_by_username
from dataclasses import dataclass
import pytz
from utils.jwt_utils import get_current_user

class MeetingCreateDto(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    join_meeting: bool = True

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
    reason: Optional[str] = None

class MeetingGetResponse(BaseModel):
    success: bool
    meeting: Optional[dict] = None

class MeetingListGetResponse(BaseModel):
    success: bool
    meetings: List[dict]

@dataclass
class Meeting:
    meeting_id: str
    title: str
    description: str
    creator_id: int
    created_at: datetime
    status: str
    start_time: datetime
    end_time: datetime

router = APIRouter(prefix="/meeting", tags=["meeting"])
@router.post("/create", response_model=MeetingCreateResponse)
async def create_meeting_controller(data: MeetingCreateDto, username: str = Depends(get_current_user)):
    meeting_id = str(random.randint(100_000_000, 999_999_999))
    tz = pytz.timezone(get_user_timezone(username))  # 用户绑定的时区
    now = datetime.now(tz).astimezone(pytz.utc)

    meeting = Meeting(
        meeting_id=meeting_id,
        title=data.title,
        description=data.description,
        creator_id=username,
        created_at=now,
        status="ready",
        start_time=data.start_time,
        end_time=data.end_time,
    )

    if add_meeting(meeting) == 0:
        raise HTTPException(status_code=500, detail="会议创建失败")
    if add_user_to_meeting(username, meeting_id, now) == 0:
        raise HTTPException(status_code=500, detail="加入会议失败")
    return MeetingCreateResponse(meeting_id=meeting_id, create_time=now)

@router.post("/delete", response_model=MeetingDeleteResponse)
async def delete_meeting_controller(data: MeetingDeleteDto, username: str = Depends(get_current_user)):
    success = delete_meeting(data.meeting_id) > 0
    return MeetingDeleteResponse(success=success)


@router.post("/get", response_model=MeetingGetResponse)
async def get_meeting_controller(data: MeetingGetDto, username: str = Depends(get_current_user)):
    meeting = find_meeting_by_id(data.meeting_id)
    return MeetingGetResponse(success=bool(meeting), meeting=meeting)


@router.post("/join", response_model=MeetingJoinResponse)
async def join_meeting_controller(data: MeetingJoinDto, username: str = Depends(get_current_user)):
    meeting = find_meeting_by_id(data.meeting_id)
    tz = pytz.timezone(get_user_timezone(username))  # 用户绑定的时区
    
    if meeting is None:
        return MeetingJoinResponse(success=False, reason="Meeting not found")
    if meeting.end_time < datetime.now(tz).astimezone(pytz.utc):
        return MeetingJoinResponse(success=False, reason="Meeting has ended")
    if meeting.start_time > datetime.now(tz).astimezone(pytz.utc):
        return MeetingJoinResponse(success=False, reason="Meeting has not started")
    inserted = add_user_to_meeting(username, data.meeting_id, datetime.now(tz).astimezone(pytz.utc))

    return MeetingJoinResponse(success=inserted > 0)


@router.get("/get_all", response_model=MeetingListGetResponse)
async def get_all_meetings_controller(username: str = Depends(get_current_user)):
    meetings = find_meetings_by_username(username)
    return MeetingListGetResponse(success=True, meetings=meetings)

@router.get("/get_all_with_records", response_model=MeetingListGetResponse)
async def get_all_meetings_with_records_controller(username: str = Depends(get_current_user)):
    meetings = find_recorded_meetings_by_username(username)
    return MeetingListGetResponse(success=True, meetings=meetings)