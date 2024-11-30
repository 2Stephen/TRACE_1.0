package com.tracebooks.back.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import com.tracebooks.back.entity.Book;

import java.util.List;


@Mapper
public interface BookMapper extends BaseMapper<Book> {
    List<Book> searchByRegion(char reg,String words);
    List<Book> search(String words);
}
