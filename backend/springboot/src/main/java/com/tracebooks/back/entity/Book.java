package com.tracebooks.back.entity;


import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

@Data
public class Book {
    @TableId(value = "id",type = IdType.AUTO)
    private Integer id;
    @TableField(value = "name")
    private String name;
    @TableField(value = "author")
    private String author;
    @TableField(value = "publisher")
    private String publisher;
    @TableField(value = "key_word")
    private String keyWord;
    @TableField(value = "abstracts")
    private String abstracts;
    @TableField(value = "UDC")
    private String UDC;
    @TableField(value = "publication_date")
    private String publicationDate;
    @TableField(value = "location")
    private String location;
}
