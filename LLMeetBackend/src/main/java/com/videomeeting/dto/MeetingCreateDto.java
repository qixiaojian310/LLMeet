package com.videomeeting.dto;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.OffsetDateTime;


@Data
public class MeetingCreateDto {


    public MeetingCreateDto() {}
    private String title;
    private String description;
    private OffsetDateTime startTime;
    private OffsetDateTime endTime;

}
