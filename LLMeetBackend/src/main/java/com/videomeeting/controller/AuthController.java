package com.videomeeting.controller;

import com.videomeeting.domain.User;
import com.videomeeting.dto.LoginRequest;
import com.videomeeting.dto.RegisterRequest;
import com.videomeeting.dto.RegisterResponse;
import com.videomeeting.service.AuthService;
import com.videomeeting.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;
    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register(
            @RequestBody @Valid RegisterRequest register){

        User user = new User();
        user.setUsername(register.getUsername());
        user.setPassword(register.getPassword());
        user.setEmail(register.getEmail());
        // 注册用户
        return authService.register(user);

        // 自动登录（可选）
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request) {
        return authService.login(request.getUsername(), request.getPassword());
    }
}