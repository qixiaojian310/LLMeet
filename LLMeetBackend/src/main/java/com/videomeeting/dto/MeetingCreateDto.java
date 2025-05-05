package com.videomeeting.dto;


import java.time.LocalDateTime;
public class MeetingCreateDto {


    public MeetingCreateDto() {}
    private String title;
    private String description;


    public String getTitle(){
        return title;
    }

    public String getDescription(){
        return description;
    }


    public MeetingCreateDto(String title, String description) {
        this.title = title;
        this.description = description;
    }

}
