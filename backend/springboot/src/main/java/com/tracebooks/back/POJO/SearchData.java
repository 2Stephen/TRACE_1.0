package com.tracebooks.back.POJO;


import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SearchData {
    private String bookinfo;
    private int searchtype;
    public SearchData() {
    }
    public SearchData(String bookinfo, int searchtype) {
        this.bookinfo = bookinfo;
        this.searchtype = searchtype;
    }
    @Override
    public String toString() {
        return "SearchData{" +
                "bookinfo='" + bookinfo + '\'' +
                ", searchtype=" + searchtype +
                '}';
    }
}
