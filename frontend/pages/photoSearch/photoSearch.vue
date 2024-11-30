<template>
	<view>
		<view class="searchArea">
			<view class="uni-list">
				<view class="uni-list-cell">
					<view class="uni-list-cell-left">
						区域选择：
					</view>
					<view class="uni-list-cell-db">
						<picker mode="multiSelector" @columnchange="bindMultiPickerColumnChange" :value="multiIndex" :range="multiArray">
							<view class="uni-input">{{multiArray[0][multiIndex[0]]}}，{{multiArray[1][multiIndex[1]]}}，{{multiArray[2][multiIndex[2]]}}，{{multiArray[3][multiIndex[3]]}}</view>
						</picker>
					</view>
				</view>
			</view>
			<view class="imageArea" @click="takePhoto">
				<image src="@/static/indexCamera.png" class="touchImage"></image>
				<text>拍照上传</text>
			</view>
			<view v-if="status === 'loading'" style="margin-left: 100rpx;margin-right: 100rpx;margin-top: 30rpx;">
				<progress  :percent="loadPercent" show-info stroke-width="3" />
			</view>
			
			<view class="show-howArea">
				<uni-section title="示例说明" type="line" padding>
					<view class="horizontalArea">
					<image v-for="(url, index) in ExampleimageUrls" :key="index" :src="url" class="show-howImg"/>
					</view>
				
				</uni-section>
				
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				multiArray: [
					['一楼中庭', '二楼东区','二楼西区','三楼东区', '三楼西区', '三楼南区','三楼北区','四楼南区', '四楼北区', '五楼南区', '五楼北区'],
					["一排", "二排", "三排", "四排", "五排", "六排", "七排", "八排", "九排", "十排", "十一排", "十二排", "十三排", "十四排", "十五排", "十六排", "十七排", "十八排", "十九排", "二十排", "二十一排", "二十二排", "二十三排", "二十四排", "二十五排", "二十六排", "二十七排", "二十八排", "二十九排", "三十排", "三十一排", "三十二排", "三十三排", "三十四排", "三十五排","三十六排","三十七排","三十八排","三十九排","四十排"],
					
					
					['一架', '二架', '三架','四架','五架','六架','七架','八架'],
					['一行', '二行', '三行','四行','五行','六行']
				],
				multiIndex: [9, 34, 0, 0],
				status: 'unload',
				loadPercent: 0,
				ExampleimageUrls: [] // 用于存储示例图片的URL
			}
		},
		onShow() {
			this.status = 'unload';
			this.loadPercent = 0;
		},
		onLoad() {
			// 加载示例图片
			uni.request({
			  url: 'http://192.168.35.154:5000/getExampleImages', // Flask API 地址
			  method: 'GET',
			  success: (res) => {
			    if (res.statusCode === 200) {
			      // 成功获取图片URL并存储
			      this.ExampleimageUrls = res.data.image_urls;
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
			bindMultiPickerColumnChange(e) {
				console.log('修改的列为', e.detail.column, '，值为', e.detail.value);
				this.multiIndex[e.detail.column] = e.detail.value
				switch (e.detail.column) {
					case 0: //拖动第1列
						this.multiIndex.splice(1, 1, 0)
						this.multiIndex.splice(2, 1, 0)
						this.multiIndex.splice(3, 1, 0)
						break
					case 1: //拖动第2列
						this.multiIndex.splice(2, 1, 0)
						this.multiIndex.splice(3, 1, 0)
						break
					case 2: //拖动第3列
						this.multiIndex.splice(3, 1, 0)
						break
				}
				this.$forceUpdate()
			},
			//上传位置
			uploadLocation() {
				// 获取区域选择
				var sectionData = this.multiArray[0][this.multiIndex[0]] + this.multiArray[1][this.multiIndex[1]] + this.multiArray[2][this.multiIndex[2]] + this.multiArray[3][this.multiIndex[3]];
				console.log(sectionData);
				uni.request({
					url: 'http://192.168.35.154:5000/uploadLocation',
					data: {
						sectionData: sectionData
					},
					method: 'POST',
					success: function(res) {
						console.log(res.data);
					}
				})
			},
			loadPercentPP() {
			  const targetPercent = 90;
			  const duration = 4000; // 总持续时间 10 秒
			  const intervalTime = 700; // 每 1 秒更新一次
			  const baseIncrement = (targetPercent / (duration / intervalTime)); // 基础增加的百分比
			
			  const interval = setInterval(() => {
			    // 添加随机扰动：增量会在 baseIncrement 的 -30% 到 +30% 范围内变化
			    const randomFactor = Math.random() * 1.6 + 0.2; // 随机范围是 0.7 到 1.3
			    const increment = baseIncrement * randomFactor; 
			
			    this.loadPercent += parseInt(increment);
			
			    if (this.loadPercent >= targetPercent) {
			      this.loadPercent = targetPercent;
			      clearInterval(interval); // 达到 90% 停止更新
			    }
			
			    console.log(`Loading: ${this.loadPercent.toFixed(2)}%`); // 输出百分比（用于调试）
			  }, intervalTime); // 每 1 秒执行一次
			},
			takePhoto() {
				console.log("take photo");
				this.uploadLocation();
				uni.chooseImage({
					count: 1,
					sourceType: ['album','camera'],
					sizeType: ['original'],
					camera: 'back',
					success: (res) => {
						console.log(res);
						this.status = 'loading';
						this.loadPercentPP();
						uni.uploadFile({
							url: 'http://192.168.35.154:5000/upload',
							filePath: res.tempFilePaths[0],
							name: 'file',
							method: 'POST',
							success: (uploadFileRes) => {
								console.log(uploadFileRes.data);
								this.loadPercent = 100;
								this.status = 'unload';
								this.loadPercent = 0;
								uni.navigateTo({
									url: '/subpages/cameraSearchResult/cameraSearchResult'
								})
							}
						})
					}
				})
			}
		}
	}
</script>

<style>
	.horizontalArea {
		display: flex;
		flex-direction: row
	}
	.imageArea {
		margin-top: 40rpx;
		margin-bottom: 20rpx;
		height: 400rpx;
		width: 400rpx;
		border-radius: 400rpx;
		background-color: #a7feff;
		align-items: center;
		display: flex;
		align-self: center;
		box-shadow: 0px 0px 10px gray;
		flex-direction: column;
	}

	.touchImage {
		height: 250rpx;
		width: 270rpx;
		/* border-radius: 100rpx; */
		margin-top: 65rpx;
	}
	.show-howArea {
		margin-top: 200rpx;
		
	}
	.searchArea {
		margin-top: 30rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.show-howImg {
		height: 200rpx;
		width: 30%;
		margin-right: 20rpx;
	}
	.uni-picker {
	    position: relative;
	    display: block;
	    cursor: pointer;
	}
	.uni-input {
	    height: 1.5625rem;
	    padding: 0.46875rem 0.78125rem;
	    line-height: 1.5625rem;
	    font-size: 0.875rem;
	    background: #FFF;
	    flex: 1;
	}

	.uni-title {
		font-size:0.9375rem;
		font-weight:500;
		padding:0.625rem 0;
		line-height:1.5;
	}
	.uni-common-pl{
		padding-left:0.9375rem;
	}
	.uni-input {
		height: 1.5625rem;
		padding: 0.46875rem 0.78125rem;
		line-height:1.5625rem;
		font-size:0.875rem;
		background:#FFF;
		flex: 1;
	}

	/* 列表 */
	.uni-list {
		background-color: #FFFFFF;
		position: relative;
		width: 100%;
		display: flex;
		flex-direction: column;
	}
	.uni-list:after {
		position: absolute;
		z-index: 10;
		right: 0;
		bottom: 0;
		left: 0;
		height: 1px;
		content: '';
		transform: scaleY(.5);
		background-color: #c8c7cc;
	}
	.uni-list:before {
	    position: absolute;
	    z-index: 10;
	    right: 0;
	    top: 0; /* Position it at the top */
	    left: 0;
	    height: 1px;
	    content: '';
	    transform: scaleY(.5); /* Same scale effect as for the bottom line */
	    background-color: #c8c7cc;
	}
	.uni-list-cell {
		position: relative;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}
	.uni-list-cell-left {
	    white-space: nowrap;
		font-size:0.875rem;
		padding: 0 0.9375rem;
	}
	.uni-list-cell-db,
	.uni-list-cell-right {
		flex: 1;
	}
</style>