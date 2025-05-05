package com.videomeeting.dto;

import lombok.Data;

import java.time.LocalDateTime;
@Data
public class MeetingCreateDto {
    public MeetingCreateDto() {}
    private String token;
    private String title;
    private String description;

}
