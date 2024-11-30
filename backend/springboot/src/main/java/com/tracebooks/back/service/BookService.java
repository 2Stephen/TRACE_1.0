package com.tracebooks.back.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.github.pagehelper.PageInfo;
import com.tracebooks.back.entity.Book;

public interface BookService extends IService<Book> {

    PageInfo<Book> searchByRegion(String region, String bookinfo, int pagenum, int pagesize);

    PageInfo<Book> searchByName(String bookinfo, int pagenum, int pagesize);
}
