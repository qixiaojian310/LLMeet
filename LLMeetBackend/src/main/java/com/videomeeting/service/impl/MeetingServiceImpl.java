package com.videomeeting.service.impl;

import com.videomeeting.domain.Meeting;
import com.videomeeting.dto.*;
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
    public ResponseEntity<MeetingGetResponse> getMeetingById(MeetingGetDto meetingGetDto) {
        Meeting meeting = meetingMapper.findByMeetingId(meetingGetDto.getMeetingId());
        if (meeting == null){
            MeetingGetResponse response = new MeetingGetResponse();
            response.setSuccess(false);
            return ResponseEntity.ok(response);
        }
        MeetingGetResponse response = new MeetingGetResponse();
        response.setMeeting(meeting);
        response.setSuccess(true);
        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<MeetingJoinResponse> joinMeeting(MeetingJoinDto meetingJoinDto) {
        // 1. 获取当前用户
        JwtUserContextUtil.UserHolder userHolder = JwtUserContextUtil.getCurrentUser();
        Integer userId = userHolder.getUserId();
        if (userId == null) {
            // 无用户信息，直接返回失败
            MeetingJoinResponse response = new MeetingJoinResponse();
            response.setSuccess(false);
            return ResponseEntity.ok(response);
        }

        // 2. 记录加入时间
        OffsetDateTime joinTime = OffsetDateTime.now();
        // 3. 调用 Mapper 加入会议
        int inserted = meetingMapper.addUserToMeeting(userId, meetingJoinDto.getMeetingId(), joinTime);
        // 4. 构造返回
        MeetingJoinResponse response = new MeetingJoinResponse();
        response.setSuccess(inserted > 0);
        return ResponseEntity.ok(response);
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
        String meetingId = IdGeneratorUtil.generateCustomId();
        Meeting meeting = new Meeting(meetingId, meetingCreateDto.getTitle(), meetingCreateDto.getDescription(),
                creatorId, createTime,status, meetingCreateDto.getStartTime(), meetingCreateDto.getEndTime());
        if(meetingMapper.addMeeting(meeting)==0)
            return null;

        if(meetingMapper.addUserToMeeting(creatorId, meetingId, createTime)==0)
            return null;

        MeetingCreateResponse response = new MeetingCreateResponse();
        response.setMeetingId(meetingId);
        response.setCreateTime(createTime);
        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<MeetingDeleteResponse> deleteMeeting(MeetingDeleteDto meetingDeleteDto){
        MeetingDeleteResponse response = new MeetingDeleteResponse();
        response.setSuccess(meetingMapper.deleteMeeting(meetingDeleteDto.getMeetingId())==0);
        return ResponseEntity.ok(response);
    }

    @Override
    public ResponseEntity<MeetingListGetResponse> getMeetingsByUserId(){
        MeetingListGetResponse response = new MeetingListGetResponse();
        JwtUserContextUtil.UserHolder userHolder = JwtUserContextUtil.getCurrentUser();
        Integer userId = userHolder.getUserId();
        response.setMeetings(meetingMapper.findMeetingsByUserId(userId));
        response.setSuccess(true);
        return ResponseEntity.ok(response);
    }
}
