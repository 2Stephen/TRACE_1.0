<template>
	<view>
		<view class="finderArea">
			<uni-data-picker :localdata="items" :placeholder="currentSelection" popup-title="请选择图书区域" @change="onchangeArea"
				@nodeclick="onnodeclick" :v-model="currentSelection"></uni-data-picker>

			<uni-search-bar class="uni-mt-10-s" radius="100" placeholder="请输入书名或关键词" clearButton="always"
				cancelButton="none" @confirm="search" :focus="false" v-model="bookInfo" />
			<uni-button class="uni-mt-10-b" type="primary" size="default" @click="search(bookInfo)">搜索</uni-button>
		</view>
		<view v-if="currentShowInfo==='search'">
			<image  class="imgArea" src="@/static/searchBG.png"></image>
			<text class="txtArea">请输入书名或关键词</text>
		</view>
		<view v-if="currentShowInfo==='result'">
			<text style="color: darkgrey;margin-left: 20rpx;font-size: 10rpx;">查询结果：共查到{{booksNum}}册</text>
			<!-- <uni-table stripe="true">
				<uni-th>
					<uni-th-cell>书名</uni-th-cell>
					<uni-th-cell>作者</uni-th-cell>
					<uni-th-cell>出版社</uni-th-cell>
					<uni-th-cell>关键词</uni-th-cell>
					<uni-th-cell>摘要</uni-th-cell>
					<uni-th-cell>出版时间</uni-th-cell>
					<uni-th-cell>中国图书分类号</uni-th-cell>
				</uni-th>
				<uni-tr v-for="(book,index) in bookResults" :key="index">
					<uni-td>{{ book.bookname }}</uni-td>
					<uni-td>{{ book.author }}</uni-td>
					<uni-td>{{ book.publisher }}</uni-td>
					<uni-td>{{ book.keyWord }}</uni-td>
					<uni-td>{{ book.abstracts }}</uni-td>
					<uni-td>{{ book.publicationDate }}</uni-td>
					<uni-td>{{ book.udc }}</uni-td>
				</uni-tr>
			</uni-table> -->
			<view>
				<view v-for="(book,index) in bookResults" :key="index">
					<uni-card :title="book.name" :extra="book.author">
						<view>位置信息：{{book.location}}</view>
						<view>出版社：{{book.publisher}}</view>
						<view>关键词：{{book.keyWord}}</view>
						<view>摘要：{{ book.abstracts.length > 50 ? book.abstracts.substring(0, 50) + '...' : book.abstracts }}</view>
						<view>出版时间：{{book.publicationDate}}</view>
						<view>中国图书分类号：{{book.udc}}</view>
					</uni-card>
				</view>
				<!-- 分页器 -->
				<view class="pageHelper">
					<uni-pagination :total="booksNum" :current="this.pageNum" :page-size="10" @change="changePage"></uni-pagination>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				booksNum: 0,
				currentSelectionId: -1,
				currentSelection: '',
				bookInfo: '',
				currentShowInfo: 'search',
				bookResults: [],
				etc: '...',
				pageSize: 10,
				pageNum: 1,
				
				items: [
					{
						text: "全部区域",
						value: "-1"
					},
					{
						text: "A 马列主义、毛泽东思想、邓小平理论 (7105)",
						value: "0"
					},
					{
						text: "B 哲学、宗教 (45829)",
						value: "1"
					},
					{
						text: "C 社会科学总论 (30576)",
						value: "2"
					},
					{
						text: "D 政治、法律 (94405)",
						value: "3"
					},
					{
						text: "E 军事 (4398)",
						value: "4"
					},
					{
						text: "F 经济 (198883)",
						value: "5"
					},
					{
						text: "G 文化、科学、教育、体育 (61929)",
						value: "6"
					},
					{
						text: "H 语言、文字 (67836)",
						value: "7"
					},
					{
						text: "I 文学 (93178)",
						value: "8"
					},
					{
						text: "J 艺术 (43444)",
						value: "9"
					},
					{
						text: "K 历史、地理 (53934)",
						value: "10"
					},
					{
						text: "N 自然科学总论 (7677)",
						value: "11"
					},
					{
						text: "O 数理科学与化学 (64285)",
						value: "12"
					},
					{
						text: "P 天文学、地球科学 (19306)",
						value: "13"
					},
					{
						text: "Q 生物科学 (26703)",
						value: "14"
					},
					{
						text: "R 医药、卫生 (18737)",
						value: "15"
					},
					{
						text: "S 农业科学 (4996)",
						value: "16"
					},
					{
						text: "T 工业技术 (342954)",
						value: "17"
					},
					{
						text: "U 交通运输 (43338)",
						value: "18"
					},
					{
						text: "V 航空、航天 (3713)",
						value: "19"
					},
					{
						text: "X 环境科学,安全科学 (17122)",
						value: "20"
					},
					{
						text: "Z 综合性图书 (5717)",
						value: "21"
					}
				]
			}
		},
		onLoad(options) {
			// 不要在load时直接赋值，这时候数据还没初始化
			this.loadData(options)
		},
		methods: {
			// 处理booksResults，如果为空则赋null
			handleResultsNull() {
				let bookResults = this.bookResults
				for (let i = 0; i < bookResults; i++) {
					// 遍历每个列表，查看每个元素是否为空
					for(let key in bookResults[i]){
						if(bookResults[i][key] === ''){
							bookResults[i][key] = 'null';
						}
					}
				}
			},
			loadData(options) {
				console.log(options);
				this.currentSelectionId = parseInt(options.index);
				if(this.currentSelectionId == -1){
					this.bookInfo = options.keywords;
					this.currentShowInfo = 'result';
				}
				this.currentSelection = options.bookClass;
				if(this.bookInfo != '' || this.currentSelectionId === -1){
					this.search(this.bookInfo)
				}
			},
			onchangeArea(e) {
				console.log(e.detail.value);
			},
			onnodeclick(node) {
				this.currentSelectionId = parseInt(node.value);
				this.currentSelection = node.text;
			},
			handleResults(res) {
				this.booksNum = res.data.total;
				this.bookResults = res.data.list;
			},
			search(e){
				this.pageNum = 1;
				if (e == '') {
					this.currentShowInfo = 'search';
					uni.showToast({
						title: '请输入搜索内容',
						icon: 'none'
					})
					return;
				}
				this.currentShowInfo = 'result';
				if(this.currentSelectionId != -1){
					uni.request({
						url: 'http://192.168.35.154:8080/book/searchByRegion',
						data: {
							pagenum: this.pageNum,
							pagesize: 10,
							region: this.currentSelection,
							bookinfo: this.bookInfo,
						},
						method: "GET",
						success: (res) => {
							this.handleResults(res);
							console.log(res);
						}
					})
				}else {
					uni.request({
						url: 'http://192.168.35.154:8080/book/search',
						data: {
							pagenum: this.pageNum,
							pagesize: 10,
							bookinfo: this.bookInfo,
						},
						method: "GET",
						success: (res) => {
							this.handleResults(res);
							console.log(res);
						},
					})
				}
				this.handleResultsNull();
			},
			changePage(e) {
				this.pageNum = e.current;
				console.log(this.pageNum);
				this.currentShowInfo = 'result';
				if(this.currentSelectionId != -1){
					uni.request({
						url: 'http://192.168.35.154:8080/book/searchByRegion',
						data: {
							pagenum: this.pageNum,
							pagesize: 10,
							region: this.currentSelection,
							bookinfo: this.bookInfo,
						},
						method: "GET",
						success: (res) => {
							this.handleResults(res);
							console.log(res);
						}
					})
				}else {
					uni.request({
						url: 'http://192.168.35.154:8080/book/search',
						data: {
							pagenum: this.pageNum,
							pagesize: 10,
							bookinfo: this.bookInfo,
						},
						method: "GET",
						success: (res) => {
							this.handleResults(res);
							console.log(res);
						},
					})
				}
				this.handleResultsNull();
				this.backTop();
			},
			//滚回顶部
			backTop() {
				uni.pageScrollTo({
						scrollTop: 0,
						duration: 100
					});
				}
		
		}
	}
</script>


<style>
	.pageHelper {
		display: flex;
		justify-content: center;
		margin-top: 20rpx;
	}
	.imgArea {
		width: 100%;
	}
	.txtArea {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		font-size: 30rpx;
		color: gray;
	}
	.finderArea {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}

	.uni-mt-10-p {
		width: 30%;
		display: inline-block;
	}

	.uni-mt-10-s {
		width: 50%;
		display: inline-block
	}

	.uni-mt-10-b {
		display: inline-block;
		width: 20%;
	}
</style>