package com.videomeeting.utils;

public class JwtUserContextUtil {
    private static final ThreadLocal<UserHolder> USER_CONTEXT = new ThreadLocal<>();

    public static void setCurrentUser(UserHolder user) {
        USER_CONTEXT.set(user);
    }

    public static UserHolder getCurrentUser() {
        return USER_CONTEXT.get();
    }

    public static void clear() {
        USER_CONTEXT.remove();
    }

    public static class UserHolder {
        private  Integer userId;
        private final String username;

        public UserHolder(Integer userId, String username) {
            this.userId = userId;
            this.username = username;
        }
        public Integer getUserId() {
            return userId;
        }
        public String getUsername() {
            return username;
        }

        public void setUserId(long l) {
            this.userId = Math.toIntExact(l);
        }
    }
}
