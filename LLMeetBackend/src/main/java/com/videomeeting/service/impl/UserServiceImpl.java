package com.videomeeting.service.impl;

import com.videomeeting.domain.CustomUserDetails;
import com.videomeeting.domain.User;
import com.videomeeting.dto.RegisterRequest;
import com.videomeeting.exception.BusinessException;
import com.videomeeting.mapper.UserMapper;
import com.videomeeting.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public boolean register(RegisterRequest registerRequest) {
        if (userMapper.existsByUsername(registerRequest.getUsername())) {
            throw new BusinessException("用户名已存在");
        }

        if (userMapper.existsByEmail(registerRequest.getEmail())) {
            throw new BusinessException("邮箱已被注册");
        }

        User user = new User(registerRequest.getUsername(),registerRequest.getEmail(),passwordEncoder.encode(registerRequest.getPassword()),LocalDateTime.now());

        userMapper.save(user);
        return userMapper.existsByUsername(registerRequest.getUsername());
    }

    @Override
    public User findByUsername(String username) {
        return userMapper.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }

    @Override
    public CustomUserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = findByUsername(username);
        return new CustomUserDetails(user.getUserID(),user.getUsername(), user.getPassword());
    }
}