package com.recruitment.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.recruitment.config.JwtUtils;
import com.recruitment.dto.LoginRequest;
import com.recruitment.dto.LoginResponse;
import com.recruitment.dto.RegisterRequest;
import com.recruitment.entity.User;
import com.recruitment.repository.UserMapper;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtils jwtUtils;

    public UserService(UserMapper userMapper, PasswordEncoder passwordEncoder, JwtUtils jwtUtils) {
        this.userMapper = userMapper;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtils = jwtUtils;
    }

    public LoginResponse login(LoginRequest req) {
        User user = userMapper.selectOne(
                new LambdaQueryWrapper<User>().eq(User::getUsername, req.getUsername()));
        if (user == null || !passwordEncoder.matches(req.getPassword(), user.getPassword())) {
            throw new RuntimeException("用户名或密码错误");
        }
        if (user.getStatus() == 0) {
            throw new RuntimeException("账户已被禁用");
        }

        String token = jwtUtils.generateToken(user.getId(), user.getUsername(), user.getRole());
        LoginResponse resp = new LoginResponse();
        resp.setToken(token);
        resp.setUsername(user.getUsername());
        resp.setRole(user.getRole());
        return resp;
    }

    public void register(RegisterRequest req) {
        Long count = userMapper.selectCount(
                new LambdaQueryWrapper<User>().eq(User::getUsername, req.getUsername()));
        if (count > 0) {
            throw new RuntimeException("用户名已存在");
        }

        User user = new User();
        user.setUsername(req.getUsername());
        user.setPassword(passwordEncoder.encode(req.getPassword()));
        user.setEmail(req.getEmail());
        user.setRole("user");
        user.setStatus(1);
        userMapper.insert(user);
    }
}
