package com.tracebooks.back.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.tracebooks.back.entity.User;
import com.tracebooks.back.mapper.UserMapper;
import com.tracebooks.back.service.UserService;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    @Resource
    private UserMapper userMapper;
    @Override
    public User isVerified(String username, String password) {
        User user = userMapper.findUserByUsername(username);
        if(user != null && user.getPassword().equals(password)) {
            return user;
        } else {
            return null;
        }
    }
    @Override
    public User findUserByUsername(String username) {
        return userMapper.findUserByUsername(username);
    }

}
