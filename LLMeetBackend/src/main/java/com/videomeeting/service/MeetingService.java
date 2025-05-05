package com.videomeeting.service;

import com.videomeeting.domain.Meeting;
import org.springframework.stereotype.Service;

@Service
public interface MeetingService {
    int addMeeting(Meeting meeting);
    public Meeting getMeetingById(String id);
}
