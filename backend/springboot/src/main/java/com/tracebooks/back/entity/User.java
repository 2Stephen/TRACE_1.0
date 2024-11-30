package com.tracebooks.back.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

@Data
public class User {
    @TableField("id")
    private Integer id;
    @TableField("username")
    private String username;
    @JsonIgnore
    @TableField("password")
    private String password;
    @TableField("role")
    private String role;
    @TableField("library")
    private String library;
}
