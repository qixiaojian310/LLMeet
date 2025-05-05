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
    @GeneratedValue(generator = "custom_id")
    @GenericGenerator(name = "custom_id", strategy = "com.videomeeting.utils.CustomeIdGenerator")
    @Column(name = "meeting_id")
    private String meetingId;

    @Column(name = "title")
    private String title;

    @Column(name = "description")
    private String description;

    @ManyToOne
    @JoinColumn(name = "creator_id", referencedColumnName = "user_id")
    private User creator;

    @Column(name = "status")
    private String status; // "ACTIVE" or "ENDED"

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "start_time")
    private LocalDateTime startTime;

    @Column(name = "end_time")
    private LocalDateTime endedAt;

    public Meeting() {}


}

