package com.videomeeting.service;

import com.videomeeting.domain.Meeting;
import com.videomeeting.dto.MeetingCreateDto;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public interface MeetingService {
    Meeting getMeetingById(String meetingId);
    ResponseEntity<String> addMeeting(MeetingCreateDto meetingCreateDto);
}
