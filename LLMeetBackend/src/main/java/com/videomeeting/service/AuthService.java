package com.videomeeting.service;

import com.videomeeting.domain.User;
import org.springframework.http.ResponseEntity;

public interface AuthService {
    ResponseEntity<String> login(String username, String password);
    void register(User user);
}