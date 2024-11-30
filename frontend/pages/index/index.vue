<template>
	<view class="content">
		<view class="finderArea">
			<uni-search-bar class="uni-mt-10-s" radius="100" placeholder="请输入书名或关键字" clearButton="always"
				cancelButton="none" @confirm="search" :focus="false" v-model="bookInfo" />
			<uni-button class="uni-mt-10-b" type="primary" size="default" @click="search(bookInfo)">搜索</uni-button>
		</view>
		<text style="color: darkgrey;margin-left: 20rpx;font-size: 10rpx;">当前图书馆书籍数量（已录入系统数量）：{{booksNum}}册</text>
		
		<!-- 图书分类 -->
		<uni-table stripe="true">
			<uni-th>
				<uni-th-cell>图书分类</uni-th-cell>
			</uni-th>
			<uni-tr v-for="(bookClass,index) in booksClass" :key="index" @click.native="gotoClassificationSearch(index)">
				<uni-td>{{ bookClass }}</uni-td>
			</uni-tr>
		</uni-table>
	</view>
</template>

<script>
	import store from '@/store/index.js';
	export default {
		data() {
			return {
				usrRole: "",
				currentTime: "你",
				bookInfo: '',
				booksNum: 1193528,
				booksClass: [
					'A 马列主义、毛泽东思想、邓小平理论 (7105)',
					'B 哲学、宗教 (45829)',
					'C 社会科学总论 (30576)',
					'D 政治、法律 (94405)',
					'E 军事 (4398)',
					'F 经济 (198883)',
					'G 文化、科学、教育、体育 (61929)',
					'H 语言、文字 (67836)',
					'I 文学 (93178)',
					'J 艺术 (43444)',
					'K 历史、地理 (53934)',
					'N 自然科学总论 (7677)',
					'O 数理科学与化学 (64285)',
					'P 天文学、地球科学 (19306)',
					'Q 生物科学 (26703)',
					'R 医药、卫生 (18737)',
					'S 农业科学 (4996)',
					'T 工业技术 (342954)',
					'U 交通运输 (43338)',
					'V 航空、航天 (3713)',
					'X 环境科学,安全科学 (17122)',
					'Z 综合性图书 (5717)'
				]
			}
		},
		computed: {},
		onShow() {
			this.getUsrInfo();
		},
		methods: {
			takePhoto() {
				uni.createCameraContext().takePhoto({
					quality: 'high',
					success: (res) => {
						console.log(res.tempImagePath);
					}
				});
			},
			getUsrInfo() {
				this.$data.usrRole = store.state.usrRole;
			},
			gotoClassificationSearch(index) {
				var bookClass = this.getBooksClass(index);
				uni.navigateTo({
					url: '/subpages/searchByRegion/searchByRegion?index=' + index + '&bookClass=' + bookClass
				})
			},
			getBooksClass(index) {
				return this.booksClass[index];
			},

			search(e) {
				if (e == '') {
					uni.showToast({
						title: '请输入搜索内容',
						icon: 'none'
					})
					return;
				}
				uni.navigateTo({
					url:'/subpages/searchByRegion/searchByRegion?index=-1'+ '&bookClass=' + '全部区域' + '&keywords=' + e
				})
			},
			input(res) {
				console.log('----input:', res)
			},
			clear(res) {
				uni.showToast({
					title: 'clear事件，清除值为：' + res.value,
					icon: 'none'
				})
			},
			blur(res) {
				uni.showToast({
					title: 'blur事件，输入值为：' + res.value,
					icon: 'none'
				})
			}
		},

	}
</script>

<style>
	.finderArea {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}

	.uni-mt-10-s {
		width: 72%;
		display: inline-block
	}

	.uni-mt-10-b {
		display: inline-block;
		width: 20%;
	}
	.content {
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.finderArea {
		height: 30%;
	}
</style>