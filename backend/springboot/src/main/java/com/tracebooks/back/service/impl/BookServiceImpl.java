package com.tracebooks.back.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.tracebooks.back.entity.Book;
import com.tracebooks.back.mapper.BookMapper;
import com.tracebooks.back.service.BookService;
import jakarta.annotation.Resource;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class BookServiceImpl extends ServiceImpl<BookMapper,Book> implements BookService {
    @Resource
    private BookMapper bookMapper;

    @Override
    public PageInfo<Book> searchByName(String bookinfo, int pagenum, int pagesize) {
        // 开始分页
        PageHelper.startPage(pagenum, pagesize);
        // 执行查询
        List<Book> bookList = bookMapper.search(bookinfo);
        // 将查询结果封装到PageInfo对象中
        return new PageInfo<>(bookList);
    }
    @Override
    public PageInfo<Book> searchByRegion(String region, String bookinfo, int pagenum, int pagesize) {
        // 开始分页
        PageHelper.startPage(pagenum, pagesize);
        char cat = region.charAt(0);
        List<Book> bookList = bookMapper.searchByRegion(cat, bookinfo);
        return new PageInfo<>(bookList);
    }
}
