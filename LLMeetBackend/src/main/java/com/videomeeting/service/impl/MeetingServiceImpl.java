package com.videomeeting.service.impl;

import com.videomeeting.domain.Meeting;
import com.videomeeting.dto.MeetingCreateDto;
import com.videomeeting.mapper.MeetingMapper;
import com.videomeeting.service.MeetingService;
import com.videomeeting.utils.JwtUserContextUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import com.videomeeting.utils.IdGeneratorUtil;

import java.time.LocalDateTime;

@Service
public class MeetingServiceImpl implements MeetingService {

    @Autowired
    MeetingMapper meetingMapper;

    @Override
    public Meeting getMeetingById(String meetingId) {
        return meetingMapper.findByMeetingId(meetingId);
    }

    @Override
    public ResponseEntity<String> addMeeting(MeetingCreateDto meetingCreateDto){
        String status = "ready";
        System.out.println(status);
        JwtUserContextUtil.UserHolder userHolder = JwtUserContextUtil.getCurrentUser();
        Integer creatorId = userHolder.getUserId();
        if (creatorId == null){
            return null;
        }
        LocalDateTime createTime = LocalDateTime.now();
        System.out.println(createTime);
        String meetingId = IdGeneratorUtil.generateCustomId();
        Meeting meeting = new Meeting(meetingId, meetingCreateDto.getTitle(), meetingCreateDto.getDescription(),
                creatorId, createTime,status);
        if(meetingMapper.addMeeting(meeting) == 0)
            return null;

        return ResponseEntity.ok(meetingId);
    }
}
