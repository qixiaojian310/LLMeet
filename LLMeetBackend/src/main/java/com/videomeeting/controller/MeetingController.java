package com.videomeeting.controller;

import com.videomeeting.dto.MeetingCreateDto;
import com.videomeeting.dto.MeetingDeleteDto;
import com.videomeeting.dto.MeetingGetDto;
import com.videomeeting.service.MeetingService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/meeting")
public class MeetingController {
    @Autowired
    private MeetingService meetingService;

    @PostMapping("/create")
    public ResponseEntity<?> saveMeeting(@RequestBody @Valid MeetingCreateDto meetingCreateDto) {
        return meetingService.addMeeting(meetingCreateDto);
    }

    @PostMapping("/delete")
    public ResponseEntity<?> deleteMeeting(@RequestBody @Valid MeetingDeleteDto meetingDeleteDto) {
        return meetingService.deleteMeeting(meetingDeleteDto);
    }

    @PostMapping("/get")
    public ResponseEntity<?> getMeeting(@RequestBody @Valid MeetingGetDto meetingGetDto) {
        return meetingService.getMeetingById(meetingGetDto);
    }
}
