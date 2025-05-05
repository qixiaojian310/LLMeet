package com.videomeeting.mapper;

import com.videomeeting.domain.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Select;
import java.util.Optional;

@Mapper
public interface UserMapper {

    @Insert("INSERT INTO user (username, email, password, created_at) " +
            "VALUES (#{username}, #{email}, #{password}, #{createdAt})")
    @Options(useGeneratedKeys = true, keyProperty = "userId")
    void save(User user);

    @Select("SELECT COUNT(*) > 0 FROM user WHERE username = #{username}")
    boolean existsByUsername(String username);

    @Select("SELECT COUNT(*) > 0 FROM user WHERE email = #{email}")
    boolean existsByEmail(String email);

    @Select("SELECT * FROM user WHERE username= #{username}")
    Optional<User> findByUsername(String username);


}
