package com.videomeeting.domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Data;
import org.hibernate.annotations.GenericGenerator;
import java.time.LocalDateTime;

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
    private LocalDateTime createdAt;

    @Column(name = "start_time")
    private LocalDateTime startTime;

    @Column(name = "end_time")
    private LocalDateTime endedAt;

    public Meeting() {}


    public Meeting(String meetingId,String title, String description, Integer creatorId, LocalDateTime createTime, String status) {
        this.meetingId = meetingId;
        this.title = title;
        this.description = description;
        this.creatorId = creatorId;
        this.createdAt = createTime;
        this.status = status;
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

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
    public LocalDateTime getStartTime() {
        return startTime;
    }

    public void setStartTime(LocalDateTime startTime) {
        this.startTime = startTime;
    }
    public LocalDateTime getEndedAt() {
        return endedAt;
    }
    public void setEndedAt(LocalDateTime endedAt) {
        this.endedAt = endedAt;
    }
    public String getStatus() {
        return status;
    }
    public void setStatus(String status) {
        this.status = status;
    }

}

