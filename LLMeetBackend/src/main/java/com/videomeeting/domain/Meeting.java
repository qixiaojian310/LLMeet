package com.videomeeting.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Data;
import org.hibernate.annotations.GenericGenerator;
import java.time.OffsetDateTime;

@Entity
@Table(name = "meeting")
@Data
public class Meeting {
    @Id
    @Column(name = "meeting_id")
    private String meetingId;

    @Column(name = "title")
    private String title;

    @Column(name = "description")
    private String description;

    @Column(name = "creator_id")  // 直接存储ID，去掉@ManyToOne
    private Integer creatorId;

    @Column(name = "status")
    private String status; // "ACTIVE" or "ENDED"

    @Column(name = "created_at")
    private OffsetDateTime createdAt;

    @Column(name = "start_time")
    private OffsetDateTime startTime;

    @Column(name = "end_time")
    private OffsetDateTime endTime;

    public Meeting() {}


    public Meeting(String meetingId,String title, String description, Integer creatorId, OffsetDateTime createTime, String status, OffsetDateTime startTime ,OffsetDateTime endTime) {
        this.meetingId = meetingId;
        this.title = title;
        this.description = description;
        this.creatorId = creatorId;
        this.createdAt = createTime;
        this.status = status;
        this.endTime = endTime;
        this.startTime = startTime;
    }
    public String getMeetingId() {
        return meetingId;
    }
    public void setMeetingId(String meetingId) {
        this.meetingId = meetingId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }
    public String getDescription() {
        return description;
    }
    public void setDescription(String description) {
        this.description = description;
    }
    public Integer getCreatorId() {
        return creatorId;
    }

    public void setCreatorId(Integer creatorId) {
        this.creatorId = creatorId;
    }

    public OffsetDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(OffsetDateTime createdAt) {
        this.createdAt = createdAt;
    }
    public OffsetDateTime getStartTime() {
        return startTime;
    }

    public void setStartTime(OffsetDateTime startTime) {
        this.startTime = startTime;
    }
    public OffsetDateTime getEndedAt() {
        return endTime;
    }
    public void setEndedAt(OffsetDateTime endedAt) {
        this.endTime = endedAt;
    }
    public String getStatus() {
        return status;
    }
    public void setStatus(String status) {
        this.status = status;
    }

}

