package com.videomeeting.dto;

import com.videomeeting.domain.Meeting;
import lombok.Data;

import java.util.List;

@Data
public class MeetingListGetResponse {
    private List<Meeting> meetings;
    private boolean success;
}
