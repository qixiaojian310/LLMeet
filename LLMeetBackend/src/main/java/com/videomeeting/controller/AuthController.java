package com.videomeeting.controller;

import com.videomeeting.domain.User;
import com.videomeeting.dto.LoginRequest;
import com.videomeeting.dto.RegisterRequest;
import com.videomeeting.service.AuthService;
import com.videomeeting.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;
    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public void register(
            @RequestBody @Valid RegisterRequest registerRequest){

        // 注册用户
        userService.register(registerRequest);

        // 自动登录（可选）
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request) {
        System.out.println(request);
        return authService.login(request.getUsername(), request.getPassword());
    }
}