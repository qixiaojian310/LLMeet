package com.videomeeting.service.impl;

import com.videomeeting.domain.Meeting;
import com.videomeeting.mapper.MeetingMapper;
import com.videomeeting.service.MeetingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MeetingServiceImpl implements MeetingService {

    @Autowired
    MeetingMapper meetingMapper;

    @Override
    public Meeting getMeetingById(String id) {
        return meetingMapper.getMeetingByMeetingId(id);
    }

    @Override
    public int addMeeting(Meeting meeting){
        return meetingMapper.addMeeting(meeting);
    }
}
