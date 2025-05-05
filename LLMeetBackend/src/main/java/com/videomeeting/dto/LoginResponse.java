package com.videomeeting.dto;


import jakarta.annotation.Nullable;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public class LoginResponse {
    public LoginResponse() {}
    private String accessToken;
    private Integer userId;
    private String username;
    private String email;
    public String getAccessToken() {
        return accessToken;
    }
    public void setAccessToken(String token) {
        this.accessToken = token;
    }

    public Integer getUserId() {
        return userId;
    }
    public void setUserId(Integer userId) {
        this.userId = userId;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getEmail() {
        return email;
    }
}