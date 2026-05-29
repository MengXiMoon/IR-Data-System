package com.recruitment.controller;

import com.recruitment.common.Result;
import com.recruitment.dto.LoginRequest;
import com.recruitment.dto.LoginResponse;
import com.recruitment.dto.RegisterRequest;
import com.recruitment.service.UserService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/login")
    public Result<LoginResponse> login(@Valid @RequestBody LoginRequest req) {
        return Result.ok(userService.login(req));
    }

    @PostMapping("/register")
    public Result<Void> register(@Valid @RequestBody RegisterRequest req) {
        userService.register(req);
        return Result.ok();
    }
}
