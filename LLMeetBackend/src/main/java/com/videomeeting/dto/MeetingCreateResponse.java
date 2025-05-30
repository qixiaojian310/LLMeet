package com.videomeeting.dto;


import lombok.Getter;
import lombok.Setter;

import java.time.OffsetDateTime;

@Setter
@Getter
public class MeetingCreateResponse {
    private String meetingId;
    private OffsetDateTime createTime;
}
