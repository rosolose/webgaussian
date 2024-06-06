<script>
import axios from 'axios';

export default {
	name: "UploadImage",
	data: () => ({
		dragCount : 0,
		isDragging : false,
		files : [],
		images : [],
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
		  onInputImage(e){
			const files = e.target.files;
			Array.from(files).forEach(file => this.addImage(file));
		},
		onDrop(e) {
			e.preventDefault();
			e.stopPropagation();

			this.isDragging = false;

			const files = e.dataTransfer.files;

			Array.from(files).forEach(file => this.addImage(file));
		},
		
		addImage(file) {
			if(!file.type.match('image.*')) {
				console.log('${file.name} is not an image');
				return;
			}
			this.files.push(file);

			const img = new Image();
			const reader = new FileReader();
			
			reader.onload = (e) => {
				this.images.push(e.target.result);
			};
			reader.readAsDataURL(file);
		},	
		upload() {
			const formData = new FormData();
			this.files.forEach(file => {
				formData.append('images', file, file.name);
			});
			console.log(this.files)
			console.log(formData.getAll("images"))

			axios.post('http://127.0.0.1:8000/ply/upload_images/', formData)
				.then(response =>{
					alert("图片上传成功");
					console.log(response);
					this.images = [];
					this.files = [];
				})
				.catch(error => {
					console.error(error);
				})
		}
	}
}
</script>

<template>
	<div class="uploader"
		@dragenter="OnDragEnter"
		@dragleave="OnDragLeave"
		@dragover.prevent
		@drop="onDrop"
		:class="{ dragging: isDragging}">

		<div class="upload-control" v-show="images.length">
			<label for="file">添加图片</label>
			<button @click="upload">上传</button>
		</div>

		<div v-show="!images.length">
			<p>将图片文件拖拽到此处</p>
			<div>或者</div>
			<div class="file-input">
				<label for="file">选择文件上传</label>
				<input type="file" id="file" @change="onInputImage" multiple>
			</div>
		</div>

		<div class="images-preview" v-show="images.length">
			<div class="img-wrapper" v-for="(image, index) in images" :key="index">
				<img :src="image" :alt="'Image Uploader ${index}'">
				<div class="details">
					<span class="name" v-text="files[index].name"></span>
					<span class="size" v-text="parseFloat(files[index].size/1024).toFixed(2)+'KB'"></span>
				</div>
			</div>
		</div>
	</div>
</template>
<style lang="scss" scoped>
@import '../assets/css/uploader.css';
</style>