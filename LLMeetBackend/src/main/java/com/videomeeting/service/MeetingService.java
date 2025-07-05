package com.videomeeting.service;

import com.videomeeting.domain.Meeting;
import com.videomeeting.dto.*;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public interface MeetingService {
    ResponseEntity<MeetingGetResponse> getMeetingById(MeetingGetDto meetingGetDto);

    ResponseEntity<MeetingJoinResponse> joinMeeting(MeetingJoinDto meetingJoinDto);

    ResponseEntity<MeetingCreateResponse> addMeeting(MeetingCreateDto meetingCreateDto);
    ResponseEntity<MeetingDeleteResponse> deleteMeeting(MeetingDeleteDto meetingDeleteDto);
    ResponseEntity<MeetingListGetResponse> getMeetingsByUserId();
}
