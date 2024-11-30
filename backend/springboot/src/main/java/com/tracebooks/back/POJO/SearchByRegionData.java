package com.tracebooks.back.POJO;


import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SearchByRegionData {
    private String bookinfo;
    private int searchtype;
    private int region;
    public SearchByRegionData() {
    }
    public SearchByRegionData(String bookinfo, int searchtype, int region) {
        this.bookinfo = bookinfo;
        this.searchtype = searchtype;
        this.region = region;
    }
    @Override
    public String toString() {
        return "SearchByRegionData{" +
                "bookinfo='" + bookinfo + '\'' +
                ", searchtype=" + searchtype +
                ", region=" + region +
                '}';
    }
}
