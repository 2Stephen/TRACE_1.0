<template>

	<view>
		<view class="main">
			<uni-card>
				<view class="horView">
					<image src="../../static/logo.png" class="avatar"></image>
					<view class="verView">
						<text
							style="font-size: 40rpx;color: #000;margin-left: 40rpx;margin-bottom: 3rpx;">{{userInfo.usrName}}</text>
						<text style="font-size: 20rpx;color: #818181;margin-left: 40rpx;">{{userInfo.usrLibrary}}</text>
					</view>
				</view>
			</uni-card>
			<view class="container">
				<uni-section title="常用功能" type="line">
					<uni-list>
						<uni-list-item :show-extra-icon="true" showArrow :extra-icon="gearIcon" title="修改信息" clickable @click="changeinfo"/>
						<uni-list-item :show-extra-icon="true" showArrow :extra-icon="infoIcon" title="常见问题" clickable @click="problem"/>
						<uni-list-item :show-extra-icon="true" showArrow :extra-icon="helpIcon" title="问题反馈" clickable @click="feedback"/>
						<uni-list-item :show-extra-icon="true" :show-arrow="true" :extra-icon="listIcon" title="协议与条款" clickable @click="agreement" />

					</uni-list>
				</uni-section>
				<button type="primary" style="margin-top: 100rpx;margin-left: 40rpx;margin-right: 40rpx;" @click="logout">退出登录</button>
			</view>
		</view>
	</view>
</template>

<script>
	import store from '@/store/index.js';
	export default {
		components: {},
		data() {
			return {
				cover: 'https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/shuijiao.jpg',
				avatar: 'https://qiniu-web-assets.dcloud.net.cn/unidoc/zh/unicloudlogo.png',
				gearIcon: {
					color: '#686868',
					size: '22',
					type: 'gear-filled'
				},
				helpIcon: {
					color: '#686868',
					size: '22',
					type: 'help-filled'
				},
				infoIcon: {
					color: '#686868',
					size: '22',
					type: 'info-filled'
				},
				listIcon: {
					color: '#686868',
					size: '22',
					type: 'list'
				},
				userInfo: {
					usrName: '',
					usrLibrary: ''
				}
			}
		},
		onLoad() {
			this.getUserInfo()
		},
		methods: {
			changeinfo() {
				uni.navigateTo({
					url: '/subpages/changeInfo/changeInfo'
				})
			},
			problem() {
				uni.navigateTo({
					url: '/subpages/problem/problem'
				})
			},
			feedback() {
				uni.navigateTo({
					url: '/subpages/fedback/fedback'
				})
			},
			agreement() {
				console.log("agreement");
				uni.navigateTo({
					url: '/subpages/agreement/agreement'
					})
			},
			logout() {
				store.commit('logout')
				uni.reLaunch({
					url: '/pages/loginPage/loginPage'
				})
			},
			getUserInfo() {
				this.userInfo = {
					usrName: store.state.usrName,
					usrLibrary: store.state.usrLibrary
				}
			},
			onClick(e) {
				console.log(e)
			},
			actionsClick(text) {
				uni.showToast({
					title: text,
					icon: 'none'
				})
			}
		}
	}
</script>

<style>
	.slot-box {
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: row;
		align-items: center;
	}

	.slot-image {
		/* #ifndef APP-NVUE */
		display: block;
		/* #endif */
		margin-right: 10px;
		width: 30px;
		height: 30px;
	}

	.slot-text {
		flex: 1;
		font-size: 14px;
		color: #4cd964;
		margin-right: 10px;
	}

	.horView {
		display: flex;
		flex-direction: row;
	}

	.verView {
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.avatar {
		width: 100rpx;
		height: 100rpx;
		border-radius: 20%;
	}

	.container {
		overflow: hidden;
	}

	.custom-cover {
		flex: 1;
		flex-direction: row;
		position: relative;
	}

	.cover-content {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 40px;
		background-color: rgba($color: #000000, $alpha: 0.4);
		display: flex;
		flex-direction: row;
		align-items: center;
		padding-left: 15px;
		font-size: 14px;
		color: #fff;
	}

	.card-actions {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
		align-items: center;
		height: 45px;
		border-top: 1px #eee solid;
	}

	.card-actions-item {
		display: flex;
		flex-direction: row;
		align-items: center;
	}

	.card-actions-item-text {
		font-size: 12px;
		color: #666;
		margin-left: 5px;
	}

	.cover-image {
		flex: 1;
		height: 150px;
	}

	.no-border {
		border-width: 0;
	}
</style>