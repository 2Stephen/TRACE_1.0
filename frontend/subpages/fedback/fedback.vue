<template>
	<view class="main">
			<view class="example">
				<!-- 基础表单校验 -->
				<uni-forms ref="valiForm" :rules="rules" :modelValue="valiFormData" class="myForm" label-position="top">
					<uni-forms-item label="标题" required name="title" style="margin-bottom: 25px;" >
						<uni-easyinput v-model="valiFormData.title" placeholder="请输入标题" placeholder-style="font-size:16px;" class="input"/>
					</uni-forms-item>
					
					<uni-forms-item label="问题描述" required name="introduction" label-width="100px" style="margin-bottom: 25px;">
						<uni-easyinput type="textarea" v-model="valiFormData.introduction" placeholder="请输入详细的问题描述,最多500字" placeholder-style="font-size:16px;" class="input" maxlength='600'/>
					</uni-forms-item>
					
					<uni-forms-item label="联系方式" name="phone" label-width="100px" style="margin-bottom: 20px;">
						<uni-easyinput v-model="phone" placeholder="请留下您的联系方式" placeholder-style="font-size:16px;" class="input"/>
					</uni-forms-item>
					
					<uni-forms-item label="上传附件" name="file" label-width="100px" style="margin-bottom: 20px;">
						<button class="inputArea" style="color:rgb(153,153,153);height:40px;font-size: 16px;line-height: 60rpx;border-style: dashed;border-color: rgb(153,153,153);margin-bottom: 10px;" plain="true" @click="uploadfile">
							<uni-icons type="cloud-upload" size="24" ></uni-icons>
							上传附件
						</button>
					</uni-forms-item>
				</uni-forms>
				<button type="primary" @click="submit('valiForm')">提交</button>
				
			</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 校验表单数据
				valiFormData: {
					title: '',
					introduction: '',
					phone: '',
					file: '',
				},
				// 校验规则
				rules: {
					title: {
						rules: [{
							required: true,
							minLength:0,
							errorMessage: '标题不能为空'
						}]
					},
					introduction: {
						rules: [{
							required: true,
							errorMessage: '问题描述不能为空'
						},{
							maxLength: 500,
							errorMessage: '描述不能超过500字'
						}]
					}
				}
				
			}
		},
		methods: {
			submit(ref) {
				this.$refs[ref].validate().then(res => {
					console.log('success', res);
					uni.showToast({
						title: `提交成功`,
						duration: 2000
					});
					setTimeout(() => {
					    uni.navigateBack({
					        delta: 1
					    });
					}, 1000);
				}).catch(err => {
					console.log('err', err);
				})
			},
			
		}
	}
</script>

<style>
	.example {
		padding: 15px;
		background-color: #fff;
	}
	.element.style {
	    width: 140px;
	    justify-content: flex-start;
	}

</style>

<style scoped>
.myForm /deep/ .uni-forms-item__label {
    font-size: 18px;
	font-weight: bold;
}
</style>