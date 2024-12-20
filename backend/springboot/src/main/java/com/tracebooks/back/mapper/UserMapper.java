package com.tracebooks.back.mapper;


import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.tracebooks.back.entity.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserMapper extends BaseMapper<User> {
    User findUserByUsername(String username);
}
