<template>
	<view>
		<text>拍照搜索如下</text>
		<view>
			<uni-section title="摆放位置错误" type="line">
				<image class="img" v-for="(url, index) in FalseimageUrls" :key="index" :src="url" mode="widthFix" />
			</uni-section>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				FalseimageUrls: [] ,// 用于存储错误图片的URL
			}
		},
		 onLoad() {
		     // 页面加载时请求后端获取图片URL
		     uni.request({
		         url: 'http://192.168.35.154:5000/getFalseImages', // Flask API 地址
		         method: 'GET',
		         success: (res) => {
		             if (res.statusCode === 200) {
		                 if (res.data.image_urls.length === 0) { // 如果没有错误图片
		                     uni.request({
		                         url: 'http://192.168.35.154:5000/getPos', // Flask API 地址
		                         method: 'GET',
		                         success: (posRes) => {
		                             if (posRes.statusCode === 200) {
		                                 const position = posRes.data.pos;
		                                 if (position === '五楼南区三十五排一架一行') {
		                                     uni.showToast({
		                                         title: "没有错误图片",
		                                         icon: 'success'
		                                     });
		                                 } else {
											 uni.showToast({
											     title: "错误过多，请手动检查位置信息！",
											     icon: 'none'

											 });
		                                 }	 
		                                 // 等待两秒后返回上一页
		                                 setTimeout(() => {
		                                     uni.navigateBack({
		                                         delta: 1
		                                     });
		                                 }, 2000);
		                             } else {
		                                 console.error('请求失败:', posRes.statusCode);
		                             }
		                         },
		                         fail: (err) => {
		                             console.error('请求错误:', err);
		                         }
		                     });
		                 } else {
		                     // 成功获取图片URL并存储，只取前三张图片
		                     this.FalseimageUrls = res.data.image_urls.slice(0, 2);
		                 }
		             } else {
		                 console.error('请求失败:', res.statusCode);
		             }
		         },
		         fail: (err) => {
		             console.error('请求错误:', err);
		         }
		     });
		 },

		methods: {
			
		}
	}
</script>

<style>
	.img {
		/* 添加边框*/
		border: 1px solid #ccc;
		width: 100%;
	}
</style>
