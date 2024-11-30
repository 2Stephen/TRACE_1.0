package com.tracebooks.back.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.tracebooks.back.entity.User;

public interface UserService extends IService<User> {
    User isVerified(String username, String password);

    User findUserByUsername(String username);
}
