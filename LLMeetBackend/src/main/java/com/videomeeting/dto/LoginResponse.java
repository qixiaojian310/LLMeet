package com.videomeeting.dto;



public class LoginResponse {
    public LoginResponse() {}
    private String token;
    private Integer userId;
    private String username;
    private String email;
    public String getToken() {
        return token;
    }
    public void setToken(String token) {
        this.token = token;
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