package com.videomeeting.mapper;

import com.videomeeting.domain.Meeting;
import com.videomeeting.domain.User;
import org.apache.ibatis.annotations.*;


@Mapper
public interface MeetingMapper {
    @Insert("INSERT INTO meeting (meeting_id, title, description, creator_id, created_at, status) " +
            "VALUES (#{meetingId}, #{title}, #{description}, #{creatorId}, #{createdAt}, #{status})")
    @Options(useGeneratedKeys = true, keyProperty = "meetingId")
    int addMeeting(Meeting meeting);

    @Update("UPDATE meeting SET " +
            "title = #{title}, " +
            "description = #{description}, " +
            "status = #{status}, " +
            "start_time = #{startTime}, " +
            "end_time = #{endedAt} " +
            "WHERE meeting_id = #{meetingId}")
    int update(Meeting meeting);


    @Select("SELECT * FROM meeting WHERE meeting_id = #{meeting_id}")
    Meeting getMeetingByMeetingId(String meeting_id);
}
