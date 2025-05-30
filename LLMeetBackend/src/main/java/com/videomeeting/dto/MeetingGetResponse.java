package com.videomeeting.dto;

import com.videomeeting.domain.Meeting;
import lombok.Data;

@Data
public class MeetingGetResponse {
    private Meeting meeting;
    private boolean success;
}
