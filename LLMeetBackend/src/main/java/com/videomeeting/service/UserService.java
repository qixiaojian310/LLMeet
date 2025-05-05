package com.videomeeting.service;

import com.videomeeting.domain.User;
import com.videomeeting.dto.RegisterRequest;
import org.springframework.security.core.userdetails.UserDetailsService;

public interface UserService extends UserDetailsService {
    void register(RegisterRequest registerRequest);
    User findByUsername(String username);
}