package com.videomeeting.service.impl;

import com.videomeeting.domain.Meeting;
import com.videomeeting.dto.MeetingCreateDto;
import com.videomeeting.dto.MeetingCreateResponse;
import com.videomeeting.dto.MeetingDeleteDto;
import com.videomeeting.dto.MeetingDeleteResponse;
import com.videomeeting.mapper.MeetingMapper;
import com.videomeeting.service.MeetingService;
import com.videomeeting.utils.JwtUserContextUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import com.videomeeting.utils.IdGeneratorUtil;

import java.time.OffsetDateTime;

@Service
public class MeetingServiceImpl implements MeetingService {

    @Autowired
    MeetingMapper meetingMapper;

    @Override
    public Meeting getMeetingById(String meetingId) {
        return meetingMapper.findByMeetingId(meetingId);
    }

    @Override
    public ResponseEntity<MeetingCreateResponse> addMeeting(MeetingCreateDto meetingCreateDto){
        String status = "ready";
        System.out.println(status);
        JwtUserContextUtil.UserHolder userHolder = JwtUserContextUtil.getCurrentUser();
        Integer creatorId = userHolder.getUserId();
        if (creatorId == null){
            return null;
        }
        OffsetDateTime createTime = OffsetDateTime.now();
        System.out.println(createTime);
        System.out.println(meetingCreateDto.getStartTime());
        System.out.println(meetingCreateDto.getEndTime());
        String meetingId = IdGeneratorUtil.generateCustomId();
        Meeting meeting = new Meeting(meetingId, meetingCreateDto.getTitle(), meetingCreateDto.getDescription(),
                creatorId, createTime,status, meetingCreateDto.getStartTime(), meetingCreateDto.getEndTime());
        if(meetingMapper.addMeeting(meeting) == 0)
            return null;

        MeetingCreateResponse response = new MeetingCreateResponse();
        response.setMeetingId(meetingId);
        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<MeetingDeleteResponse> deleteMeeting(MeetingDeleteDto meetingDeleteDto){
        MeetingDeleteResponse response = new MeetingDeleteResponse();
        response.setSuccess(meetingMapper.deleteMeeting(meetingDeleteDto.getMeetingId())==0);
        return ResponseEntity.ok(response);
    }
}
