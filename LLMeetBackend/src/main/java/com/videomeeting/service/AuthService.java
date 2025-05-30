package com.videomeeting.service;

import com.videomeeting.domain.User;
import org.springframework.http.ResponseEntity;

public interface AuthService {
    ResponseEntity<?> login(String username, String password);
    ResponseEntity<?> register(User user);
}