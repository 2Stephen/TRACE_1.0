<template>
	<view>
		<scroll-view scroll-y="true" style="height: 100vh;">
			<view class="title">协议与条款</view>
			<view class="content">
				<view class="section">
				<text>欢迎使用我们的服务。在使用本服务前，请仔细阅读以下协议条款。</text>
				</view>

				<view class="section">
					<text class="section-title">1. 服务说明</text>
					<text>本平台为用户提供包括但不限于图书纠错、信息查询等功能。用户在使用过程中应遵守相关法律法规，不得利用本服务从事非法活动。</text>
				</view>

				<view class="section">
					<text class="section-title">2. 用户行为</text>
					<text>用户应妥善保管账户信息，严禁将账户用于未经授权的用途。如账户出现异常情况，用户应及时联系平台方。</text>
				</view>

				<view class="section">
					<text class="section-title">3. 责任限制</text>
					<text>平台尽力确保服务的稳定性与安全性，但不对因不可抗力或其他非平台原因导致的服务中断或数据丢失负责。</text>
				</view>

				<view class="section">
					<text class="section-title">4. 隐私政策</text>
					<text>平台承诺保护用户的隐私信息，未经用户同意不会向第三方披露用户的个人信息，除非法律要求。</text>
				</view>

				<view class="section">
					<text class="section-title">5. 修改与终止</text>
					<text>平台保留在任何时间修改、暂停或终止服务的权利，相关变更将提前通知用户。</text>
				</view>

				<view class="section">
					<text class="section-title">6. 法律适用</text>
					<text>本协议受当地法律法规管辖，若出现争议，应优先协商解决，协商不成的，由平台所在地法院管辖。</text>
				</view>

				<view class="section">
					<text class="section-title">7. 联系我们</text>
					<text>如有任何问题，请通过客服渠道与我们联系。</text>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 可以在此添加其他逻辑
			}
		},
		methods: {
			// 其他功能可放置在此处
		}
	}
</script>

<style>
	.title {
		margin-top: 20px;
		font-size: 20px;
		font-weight: bold;
		text-align: center;
		margin-bottom: 10px;
	}

	.content {
		padding: 10px;
	}

	.section {
		margin-bottom: 15px;
	}

	.section-title {
		font-size: 18px;
		font-weight: bold;
		margin-bottom: 5px;
	}
</style>
