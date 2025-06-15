package com.videomeeting.mapper;

import com.videomeeting.domain.Meeting;
import com.videomeeting.domain.User;
import org.apache.ibatis.annotations.*;

import java.time.OffsetDateTime;
import java.util.List;
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

    @Delete("DELETE FROM meeting WHERE meeting_id = #{meetingId}")
    int deleteMeeting(String meetingId);

    @Select("SELECT * FROM meeting WHERE meeting_id = #{meetingId}")
    Meeting findByMeetingId(String meetingId);
    // 新增方法：添加用户到会议关联表
    @Insert("INSERT INTO user_meeting (user_id, meeting_id, joined_at) " +
            "VALUES (#{userId}, #{meetingId}, #{joinedAt})")
    int addUserToMeeting(
            @Param("userId") int userId,
            @Param("meetingId") String meetingId,
            @Param("joinedAt") OffsetDateTime joinedAt
    );
    // 可选：根据用户ID查询参加的所有会议
    @Select("SELECT m.* FROM meeting m " +
            "JOIN user_meeting um ON m.meeting_id = um.meeting_id " +
            "WHERE um.user_id = #{userId}")
    List<Meeting> findMeetingsByUserId(int userId);

    // 可选：根据会议ID查询所有参会用户
    @Select("SELECT u.* FROM user u " +
            "JOIN user_meeting um ON u.user_id = um.user_id " +
            "WHERE um.meeting_id = #{meetingId}")
    List<User> findUsersByMeetingId(String meetingId);
}
