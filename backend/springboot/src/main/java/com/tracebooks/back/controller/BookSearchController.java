package com.tracebooks.back.controller;


import com.github.pagehelper.PageInfo;
import com.tracebooks.back.entity.Book;
import com.tracebooks.back.service.BookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/book")
public class BookSearchController {
    @Autowired
    private BookService BookService;

    @GetMapping("/search")
    public ResponseEntity<PageInfo<Book>> search(
            @RequestParam int pagenum,
            @RequestParam int pagesize,
            @RequestParam String bookinfo) {
        System.out.println("pagenum: " + pagenum + " pagesize: " + pagesize + " bookinfo: " + bookinfo);
        PageInfo<Book> pageInfo = BookService.searchByName(bookinfo, pagenum, pagesize);
        return ResponseEntity.ok(pageInfo);
    }
    @GetMapping("/searchByRegion")
    public ResponseEntity<PageInfo<Book>> searchByRegion(
            @RequestParam int pagenum,
            @RequestParam int pagesize,
            @RequestParam String region,
            @RequestParam String bookinfo) {
        System.out.println("pagenum: " + pagenum + " pagesize: " + pagesize + " region: " + region + " bookinfo: " + bookinfo);
        PageInfo<Book> pageInfo = BookService.searchByRegion(region, bookinfo, pagenum, pagesize);
        return ResponseEntity.ok(pageInfo);
    }
}
