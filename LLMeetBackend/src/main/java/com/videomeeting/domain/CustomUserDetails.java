package com.videomeeting.domain;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.GrantedAuthority;

import java.util.Collection;

public class CustomUserDetails implements UserDetails {
    private Integer userId;
    private String username;
    private String password;
    private Collection<? extends GrantedAuthority> authorities;

    public CustomUserDetails(Integer userId, String username, String password) {
        this.userId = userId;
        this.username = username;
        this.password = password;
        this.authorities = authorities;
    }
    public Integer getUserId() {
        return userId;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return password;
    }

    @Override
    public String getUsername() {
        return username;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;  // 账户是否未过期（根据业务调整）
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;  // 账户是否未锁定
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;  // 凭证是否未过期
    }

    @Override
    public boolean isEnabled() {
        return true;  // 账户是否启用
    }
}
