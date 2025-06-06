package com.videomeeting.service.impl;

import com.videomeeting.domain.CustomUserDetails;
import com.videomeeting.domain.User;
import com.videomeeting.dto.LoginResponse;
import com.videomeeting.dto.RegisterRequest;
import com.videomeeting.dto.RegisterResponse;
import com.videomeeting.utils.JwtTokenUtil;
import com.videomeeting.service.AuthService;
import com.videomeeting.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
public class AuthServiceImpl implements AuthService {

    @Autowired
    private AuthenticationManager authenticationManager;
    @Autowired
    private JwtTokenUtil jwtUtil;
    @Autowired
    private UserService userService;

    @Override
    public ResponseEntity<Object> login(String username, String password) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(username, password));
            SecurityContextHolder.getContext().setAuthentication(authentication);
            CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
            // 直接复用认证结果
            System.out.println("111111111111111111111111111111111111111111");
            LoginResponse response = new LoginResponse();
            response.setAccessToken(jwtUtil.generateToken(userDetails));
            response.setUserId(userDetails.getUserId());
            response.setUsername(userDetails.getUsername());
            return ResponseEntity.ok(response);
        } catch (AuthenticationException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("username or password is wrong!");
        }
    }

    public ResponseEntity<Object> register(User user) {
        RegisterRequest request = new RegisterRequest();
        request.setUsername(user.getUsername());
        request.setPassword(user.getPassword());
        request.setEmail(user.getEmail());
        boolean res = userService.register(request);
        RegisterResponse response = new RegisterResponse();
        response.setSuccess(res);
        return ResponseEntity.ok(response);
    }
}