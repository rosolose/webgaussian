<script>
export default {
	name: "Header"
}
</script>

<template>
	<div>
		<div class="uploader">
			<a href="#/imageuploader">上传图片</a>
			<br>
			<p>或者</p>
			<a href="#/videouploader">上传视频</a>
		</div>
		<div>
			<router-view></router-view>
		</div>
	</div>
</template>

<style scoped>
@import '../assets/css/uploader.css'
</style>