<script>
import axios from 'axios';

export default {
	name: "UploadVideo",
	data: () => ({
		dragCount: 0,
		isDragging : false,
		file: null,
		video: null,
	}),
	methods: {
		// 处理鼠标拖动
		onDragEnter(e) {
			e.preventDefault();
			this.dragCount++;
			this.isDragging = true;
		},
		OnDragLeave(e) {
			e.preventDefault();
			this.dragCount--;
			if (this.dragCount<=0)
				this.isDragging = false;
		},
		onInputVideo(e){
			const file = e.target.files[0]
			this.addVideo(file)
		},
		onDrop(e) {
			e.preventDefault();
			e.stopPropagation();

			this.isDragging = false;

			const files = e.dataTransfer.files;

			Array.from(files).forEach(file => this.addVideo(file));
		},
		
		addVideo(file) {
			if(!file.type.startsWith('video/')) {
				console.log('${file.name} is not a video');
				return;
			}
			this.file = file
			console.log(file)
			console.log(URL.createObjectURL(file))
			const videoUrl = URL.createObjectURL(file)
			const videoPlayer = this.$refs.videoPlayer
			videoPlayer.src = videoUrl
		},
		upload() {
			const formData = new FormData();
			formData.append('video', this.file, this.file.name);
			console.log(this.file)
			console.log(formData.getAll("video"))

			axios.post('http://127.0.0.1:8000/ply/upload_videos/', formData)
				.then(response =>{
					alert("视频上传成功");
					console.log(response);
					this.video = null;
					this.file = null;
				})
				.catch(error => {
					console.error(error);
				})
		}
	},
}

</script>
<template>
	<div class="uploader"
		@dragenter="OnDragEnter"
		@dragleave="OnDragLeave"
		@dragover.prevent
		@drop="onDrop"
		:class="{ dragging: isDragging}">
		
		<div class="upload-control" v-show="file">
			<button @click="upload">上传</button>
		</div>
		<div v-show="!file">
			<p>将视频文件拖拽到此处</p>
			<div>或者</div>
			<div class="file-input">
				<label for="file">选择文件上传</label>
				<input type="file" id="file" @change="onInputVideo">
			</div>
		</div>

		<div class="video-preview" v-show="file">
			<video ref="videoPlayer" controls autoplay="false" muted width="500px" height="300px">
				您的浏览器不支持视频播放
			</video>
			<div class="details" v-if="file">
				<span class="name" v-text="file.name"></span>
				<span class="size" v-text="parseFloat(file.size/(1024*1024)).toFixed(2)+'MB'"></span>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
@import '../assets/css/uploader.css'
</style>