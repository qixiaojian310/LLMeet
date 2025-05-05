package com.videomeeting.mapper;

import com.videomeeting.domain.Meeting;
import com.videomeeting.domain.User;
import org.apache.ibatis.annotations.*;

import java.util.Optional;


@Mapper
public interface MeetingMapper {
    @Insert("INSERT INTO meeting (meeting_id,title, description, creator_id, created_at, status, start_time, end_time) " +
            "VALUES (#{meetingId}, #{title}, #{description}, #{creatorId}, #{createdAt}, #{status}, #{startTime}, #{endTime})")
    int addMeeting(Meeting meeting);

    @Update("UPDATE meeting SET " +
            "title = #{title}, " +
            "description = #{description}, " +
            "status = #{status}, " +
            "start_time = #{startTime}, " +
            "end_time = #{endedAt} " +
            "WHERE meeting_id = #{meetingId}")
    int update(Meeting meeting);

    @Select("SELECT * FROM meeting WHERE meeting_id = #{meetingId}")
    Meeting findByMeetingId(String meetingId);

}
