package com.videomeeting.controller;

import com.videomeeting.dto.MeetingCreateDto;
import com.videomeeting.service.MeetingService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/meeting")
public class MeetingController {
    @Autowired
    private MeetingService meetingService;

    @PostMapping("/create")
    public ResponseEntity<String> saveMeeting(@RequestBody @Valid MeetingCreateDto meetingCreateDto) {
        return meetingService.addMeeting(meetingCreateDto);
    }

}
