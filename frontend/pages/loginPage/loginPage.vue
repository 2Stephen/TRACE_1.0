<template>
	<view class="background">
<!-- 		<view class="upper-area">
			<text style="font-size: 50rpx;">{{currentTime}}好，欢迎使用TRACE!</text>
		</view> -->
		<view class="form-position">
			<uni-card class="form" v-if="recentMode === 'login'">
				<uni-easyinput class="inputArea" v-model="usrName" placeholder="请输入用户名"
					@input="inputUsrName"></uni-easyinput>
				<uni-easyinput class="inputArea" type="password" v-model="usrPwd" @input="inputPwd"
					placeholder="请输入密码"></uni-easyinput>
				<view class="code-img-wrapper">
					<uni-easyinput class="inputArea" v-model="form.graphicVerifyCode"
						placeholder="请输入图形验证码"></uni-easyinput>
					<view class="code-img-pos">
						<canvas style="width:220rpx;height:86rpx;" canvas-id="canvas" @click="updateImageCode"></canvas>
					</view>
				</view>
				<view class="submitArea">
					<button type="primary" @click="submitTable">登录</button>
				</view>
				<view class="forgotOrRegisterArea">
					<text style="text-decoration: underline;" @click="forgotPwd">忘记密码</text>
					<text style="text-decoration: underline;" @click="register">注册</text>
				</view>
			</uni-card>
			
			
			<uni-card v-if="recentMode === 'forgotPwd'">
				<uni-easyinput class="inputArea" type="number" v-model="phoneNum" @input="inputPhoneNum"
					placeholder="请输入手机号"></uni-easyinput>
				<uni-easyinput class="inputArea" type="number" v-model="phoneNum" @input="inputPhoneNum"
					placeholder="请输入验证码">
					<template #right>
						<view style="margin-right: 20rpx;color: rgb(41,121,255);font-size: 16rpx;" @click="getCAPTCHA" v-if="!showTime">获取验证码</view>
						<view style="margin-right: 40rpx;color: rgb(153,153,153);font-size: 16rpx;" v-else>{{ getTime }}秒</view>
					</template>
				</uni-easyinput>
				<uni-easyinput class="inputArea" type="password" v-model="form.usrPwd" @input="inputPwd"
					placeholder="请输入密码"></uni-easyinput>
				<uni-easyinput class="inputArea" type="password" v-model="form.validatePwd" @input="inputPwd2"
					placeholder="请再次输入密码"></uni-easyinput>
				<view class="submitArea">
					<button type="primary" @click="forgetsubmit">确定</button>
				</view>
				<view class="forgotOrRegisterArea">
					<text style="text-decoration: underline;" @click="login">返回登录</text>
					<text style="text-decoration: underline;" @click="register">注册</text>
				</view>
			</uni-card>
			
			
			<uni-card class="form" v-if="recentMode === 'register'">
				<uni-easyinput class="inputArea" v-model="form.usrName" placeholder="请输入用户名"
					@input="inputUsrName"></uni-easyinput>
					
				<view class="inputArea">
					<radio-group @change="radioChange">
						&nbsp选择身份:
						<label class="uni-list-cell uni-list-cell-pd" v-for="(item, index) in items" :key="item.value">
							&nbsp&nbsp&nbsp&nbsp<radio :value="item.value" v-model="form.userRole"/>
							{{item.name}}
						</label>
					</radio-group>
				</view>
				
				<button v-if="form.userRole === 'librarian'" class="inputArea" style="color:rgb(106,106,106);height: 60rpx;font-size: 30rpx;line-height: 60rpx;border-style: dashed;border-color: rgb(153,153,153);" plain="true" @click="uploadLicense">上传证件</button>

				<uni-easyinput class="inputArea" type="password" v-model="form.usrPwd" @input="inputPwd"
					placeholder="请输入密码"></uni-easyinput>
				<uni-easyinput class="inputArea" type="password" v-model="form.validatePwd" @input="inputPwd2"
					placeholder="请再次输入密码"></uni-easyinput>
				<view class="code-img-wrapper">
					<uni-easyinput class="inputArea" v-model="form.graphicVerifyCode"
						placeholder="请输入图形验证码"></uni-easyinput>
					<view class="code-img-pos">
						<canvas style="width:220rpx;height:86rpx;" canvas-id="canvas" @click="updateImageCode"></canvas>
					</view>
				</view>
				
				<view class="submitArea">
					<button type="primary" @click="registerSubmit">注册</button>
				</view>
				<view class="forgotOrRegisterArea">
					<text style="text-decoration: underline;" @click="forgotPwd">忘记密码</text>
					<text style="text-decoration: underline;" @click="login">返回登录</text>
				</view>
			</uni-card>
		</view>
	</view>
</template>

<script>
	import axios from 'axios';
	import {
		Mcaptcha
	} from '@/utils/mcaptcha';
	import store from '@/store/index.js';
	export default {
		data() {
			return {
				getTime: 60,
				showTime: false,
				form: {
					userRole:'',
					usrName: '',
					usrPwd: '',
					validatePwd:'',
					graphicVerifyCode: ''
				},
				mcaptcha: null,
				currentTime: "你",
				recentMode: 'login',
				phoneNum: '',
				items: [
							{
								value: 'reader',
								name: '读者',
							},
							{
								value: 'librarian',
								name: '图书管理员'
							}
						],
				
			}
		},
		onReady() {
			this.mcaptcha = new Mcaptcha({
				el: 'canvas',
				width: 80,
				height: 35,
				createCodeImg: ""
			});
		},
		onLoad() {},
		onShow() {
			this.getTimePeriod();
		},
		methods: {
			getCAPTCHA(){
				let timer = setInterval(() => {
				        this.getTime -= 1;
				        if (this.getTime <= 0) {
				          clearInterval(timer);
				          this.showTime = false;
				          this.getTime = 60;
				        }
				      }, 1000);
				 
				      this.showTime = true;
			},
			forgetsubmit(){
				this.login();
			},
			radioChange(evt){
				this.form.userRole = evt.detail.value;
			},
			uploadLicense(){
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
							url: 'http://192.168.35.154:8080/api/uploadLicense',
							filePath: res.tempFilePaths[0],
							name: 'file',
							method: 'POST',
							success: (uploadFileRes) => {
								console.log(uploadFileRes.data);
							}
						})
					}
				})
			},
			//注册
			registerSubmit(){
				if (!this.form.usrName) {
					this.updateImageCode();
					return uni.showToast({
						title: '请输入用户名',
						icon: 'error'
					})
				} else if (!this.form.userRole) {
					this.updateImageCode();
					return uni.showToast({
						title: '请选择身份',
						icon: 'error'
					})
				}else if (!this.form.usrPwd) {
					this.updateImageCode();
					return uni.showToast({
						title: '请输入密码',
						icon: 'error'
					})
				} else if (!this.form.validatePwd) {
					this.updateImageCode();
					return uni.showToast({
						title: '请再次输入密码',
						icon: 'error'
					})
				} else if (!this.form.graphicVerifyCode) {
					return uni.showToast({
						title: '请输入图形验证码',
						icon: 'error'
					})
				}
				// 校验图形验证码
				else if (!this.mcaptcha.validate(this.form.graphicVerifyCode)) {
					this.updateImageCode();
					this.form.graphicVerifyCode = '';
					return uni.showToast({
						title: '图形验证码错误',
						icon: 'error'
					})
				}else if (!(this.form.usrPwd === this.form.validatePwd)) {
					this.updateImageCode();
					this.form.graphicVerifyCode = '';
					return uni.showToast({
						title: '两次密码不一致',
						icon: 'error'
					})
				}
				uni.request({
					url: 'http://192.168.35.154:8080/api/register',
					data: {
						username: this.form.usrName,
						password: this.form.usrPwd,
						userrole: this.form.userRole
					},
					method: "POST",
					success: (res) => {
						if(res.statusCode === 200){
							uni.showToast({
								title: '注册成功',
								icon: 'success',
								duration: 500
							});
							this.login();
						}
						else{
							this.updateImageCode();
							this.form.graphicVerifyCode='';
							uni.showToast({
								title: "用户名重复",
								icon: 'error'
							})
						}
					},
					fail: (err) => {
						console.log(err);
						
					},
				})
			},
			
			// 登录
			login() {
				this.recentMode = 'login';
				this.form.graphicVerifyCode = '';
				this.$nextTick(() => {
				  this.updateImageCode(); // 切换模式后立即刷新验证码
				});
				this.$forceUpdate();
			},
			// 忘记密码
			forgotPwd() {
			  this.recentMode = 'forgotPwd';
			  this.$nextTick(() => {
			    this.updateImageCode(); // 切换模式后立即刷新验证码
			  });
			  this.$forceUpdate();
			},

			// 注册
			register() {
				this.recentMode = 'register';
				this.$nextTick(() => {
				  this.updateImageCode(); // 切换模式后立即刷新验证码
				});
				this.$forceUpdate();
			},
			// 获取当前时间段
			getTimePeriod() {
				const h = new Date().getHours();
				if (h < 12) {
					this.$data.currentTime = '上午';
				} else if (h < 13) {
					this.$data.currentTime = '中午';
				} else if (h < 18) {
					this.$data.currentTime = '下午';
				} else {
					this.$data.currentTime = '晚上';
				}
			},
			// 刷新验证码
			updateImageCode() {
				this.mcaptcha.refresh()
			},
			// 输入框输入用户名
			inputUsrName(e) {
				this.form.usrName = e
			},
			// 输入框输入密码
			inputPwd(e) {
				this.form.usrPwd = e
			},
			inputPwd2(e) {
				this.form.validatePwd = e
			},
			// 提交前校验图形验证码
			submitTable() {
				if (!this.form.usrName) {
					this.updateImageCode();
					return uni.showToast({
						title: '请输入用户名',
						icon: 'error'
					})
				} else if (!this.form.usrPwd) {
					this.updateImageCode();
					return uni.showToast({
						title: '请输入密码',
						icon: 'error'
					})
				} else if (!this.form.graphicVerifyCode) {
					return uni.showToast({
						title: '请输入图形验证码',
						icon: 'error'
					})
				}
				// 校验图形验证码
				else if (!this.mcaptcha.validate(this.form.graphicVerifyCode)) {
					this.updateImageCode();
					this.form.graphicVerifyCode = '';
					return uni.showToast({
						title: '图形验证码错误',
						icon: 'error'
					})
				}
				uni.request({
					url: 'http://192.168.35.154:8080/api/login',
					data: {
						username: this.form.usrName,
						password: this.form.usrPwd,
					},
					method: "POST",
					success: (res) => {
						if(res.statusCode === 200){
							//将token存入vuex
							store.state.usrName = res.data.username;
							store.state.usrRole = res.data.role;
							store.state.usrLibrary = res.data.library;
							uni.showToast({
								title: '登录成功',
								icon: 'success',
								duration: 500
							});
							uni.switchTab({
								url: '/pages/index/index'
							})
						}
						else{
							this.updateImageCode();
							this.form.graphicVerifyCode='';
							uni.showToast({
								title: "用户名或密码错误",
								icon: 'error'
							})
						}
						
					},
					fail: (err) => {
						console.log(err);
					},
				})
			},
		}
	}
</script>

<style>
	.background {
	    background-image: url('@/static/login.png');
	    background-size: cover;
	    background-position: center;
	    /* 确保背景覆盖整个页面 */
	    height: 100vh; 
	    margin: 0;
	    padding: 0;
		
	}

	.uni-card[data-v-ae4bee67] {
	    margin: 10px;
	    /* padding: 0 8px; */
	    border-radius: 4px;
	    overflow: hidden;
	    font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, SimSun, sans-serif;
	    background-color: #fff;
	    flex: 1;
	    background-color: rgba(255, 255, 255, 0.9);
	}
	.upper-area {
	  padding: 10px;
	  font-size: 16px;
	  color: #000; /* Ensure the text color is visible */
	}

	.forgotOrRegisterArea {
		display: flex;
		justify-content: space-between;
		margin-top: 20rpx;
		margin-left: 20rpx;
		margin-right: 20rpx;
	}

	.submitArea {
		margin-top: 20rpx;
	}
	.form-position {
	    /* 登录表单居中 */
	    z-index: 10; /* 提高表单的 z-index */
	    position: relative; /* 确保 z-index 生效 */
	    display: flex;
	    justify-content: center;
	    align-items: center;
	    height: 90vh;
	}

	.inputArea {
		margin-top: 20rpx;
	}
	
	

	.code-img-wrapper {
		display: flex;
		justify-content: space-between;
	}

	.code-img-pos {
		margin-top: 20rpx;
		margin-left: 20rpx;
		margin-right: -30rpx;
		position: relative;
	}
</style>