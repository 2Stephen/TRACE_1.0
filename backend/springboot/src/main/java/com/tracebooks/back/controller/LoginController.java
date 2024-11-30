package com.tracebooks.back.controller;


import com.tracebooks.back.POJO.UserData;
import com.tracebooks.back.entity.User;
import com.tracebooks.back.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Map;

@Controller
@RequestMapping("/api")
public class LoginController {
    private final UserService userService;
    @Autowired
    public LoginController(UserService userService) {
        this.userService = userService;
    }
    @ResponseBody
    @PostMapping("/login")
    public ResponseEntity<User> isVerified(@RequestBody UserData data) {
        String username = data.getUsername();
        String password = data.getPassword();
        User user = userService.isVerified(username, password);
        if (user == null) {
            return ResponseEntity.badRequest().body(null);
        } else {
            System.out.println(user.toString());
            return ResponseEntity.ok(user);
        }
    }
}
