package com.videomeeting;

import com.videomeeting.domain.User;
import com.videomeeting.dto.LoginRequest;
import com.videomeeting.dto.RegisterRequest;
import com.videomeeting.service.impl.AuthServiceImpl;
import com.videomeeting.service.impl.UserServiceImpl;
import com.videomeeting.utils.IdGeneratorUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class VideomeetingApplicationTests {

	@Autowired
	private UserServiceImpl userService;
	@Test
	void contextLoads() {
		RegisterRequest request = new RegisterRequest();
		request.setUsername("testuser1111");
		request.setEmail("test111@example.com");
		request.setPassword("password123");

		userService.register(request);
	}

	@Autowired
	private AuthServiceImpl authService;
	@Test
	void login() {
		LoginRequest request = new LoginRequest();
		request.setUsername("HKU01");
		request.setPassword("!1234Abcde000");
		authService.login(request.getUsername(), request.getPassword());
	}

	private IdGeneratorUtil idGeneratorUtil = new IdGeneratorUtil();
	@Test
	void generateor() {
		System.out.println(idGeneratorUtil.generateCustomId());
	}


}
