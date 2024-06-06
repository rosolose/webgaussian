<script>
import axios from 'axios'

export default {
	name: "ResultsPage",
	data: () => ({
		imgPath: [],
		uploadTime: [],
		plyPath: [],
		plyTime: [],
		isFinished: [],
		isImg: [],
		jsonData: [
			{
				"img_path": "storage/upload_images/forklift.png",
				"upload_time": "2024-05-10 8:16:34.34",
				"ply_path": "storage/output/forklift.ksplat",
				"ply_time": "2024-05-11 16:22:02",
				"is_finished": 1
			},
			{
				"img_path": "storage/upload_images/inkbox.png",
				"upload_time": "2024-05-10 08:24:09.24",
				"ply_path": "storage/output/inkbox.ksplat",
				"ply_time":"2024-05-10 08:54:09",
				"is_finished": 1
			},
			{
				"img_path": "storage/upload_images/bonsai.png",
				"upload_time": "2024-05-10 10:41:15",
				"ply_path": null,
				"ply_time": null,
				"is_finished": 0
			}
		],
		// videoData: {
		// 	"img_path": "storage/upload_videos/4.mp4",
		// 	"upload_time": "2024-05-10 8:16:34.34",
		// 	"ply_path": null,
		// 	"ply_time": null,
		// 	"is_finished": 0
		// }
	}),
	created() {
		this.getModels()
	},
	methods: {
		getModels() {
			console.log("getting the models")
			this.imgList = []
			// 1.从后端服务器获取数据
			// 2.将后端服务器返回的图片和模型文件添加至变量中
			const prefix = "http://127.0.0.1:8000/"
			axios.get(prefix+'ply/list_img/')
				.then(response => {
					const objArray = response.data["data"]
					objArray.forEach(obj => {
						this.imgPath.push(prefix+obj["img_path"])
						this.uploadTime.push(obj["upload_time"])
						this.plyPath.push(prefix+obj["ply_path"])
						this.plyTime.push(obj["ply_time"])
						this.isFinished.push(obj["is_finished"])
						this.isImg.push(1)
					});
				})
			// // 3.将后端服务器返回的视频链接和模型文件添加至变量中
			// axios.get(prefix+'ply/list_video/')
			// 	.then(response => {
			// 		const objArray2 = response.data["data"]
			// 		objArray2.forEach(obj => {
			// 			this.imgPath.push(this.captureFirstFrame(prefix+obj["img_path"]))
			// 			this.uploadTime.push(obj["upload_time"])
			// 			this.plyPath.push(prefix+obj["ply_path"])
			// 			this.plyTime.push(obj["ply_time"])
			// 			this.isFinished.push(obj["is_finished"])
			// 			this.isImg.push(0)
			// 		});
			// 	})
			//本地测试
			// const objArray = this.jsonData
			// const prefix = "src/assets/"
			// objArray.forEach(obj => {
			// 	this.imgPath.push(prefix+obj["img_path"])
			// 	this.uploadTime.push(obj["upload_time"])
			// 	this.plyPath.push(prefix+obj["ply_path"])
			// 	this.plyTime.push(obj["ply_time"])
			// 	this.isFinished.push(obj["is_finished"])
			// 	this.isImg.push(1)
			// })
			// this.imgPath.push(this.captureFirstFrame(prefix+this.videoData["img_path"]))
			// this.uploadTime.push(this.videoData["upload_time"])
			// this.plyPath.push(prefix+this.videoData["ply_path"])
			// this.plyTime.push(this.videoData["ply_time"])
			// this.isFinished.push(this.videoData["is_finished"])
			// this.isImg.push(0)
		},
		refresh() {
			location.reload()
		},
		openViewer:function(val) {
			return '#/viewer?local=0&id='+val
		},
		captureFirstFrame(videoPath) {
			// 创建一个 video 元素
			const video = document.createElement('video')
			video.src = videoPath
			console.log(videoPath)
			// 在 loadedmetadata 事件触发后获取视频第一帧的图片
			video.addEventListener('loadedmetadata', () => {
				video.currentTime = 1
				const canvas = document.createElement('canvas')
				canvas.width = video.videoWidth
				canvas.height = video.videoHeight
				const ctx = canvas.getContext('2d')
				ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
				video.remove()
				// 将 Canvas 转换为图片 URL
				console.log(canvas.toDataURL())
				return canvas.toDataURL()
			})
		},
	}
}
</script>

<template>
	<div class="result">
		<div class="control">
			<button @click="refresh">刷新</button>
		</div>
		<br>
		<div v-show="!imgPath.length">
			<p class="msg">暂时没有模型</p>
		</div>
		<div class="scenes-preview" v-show="imgPath.length">
			<div class="scene-wrapper" v-for="(img, index) in imgPath" :key="index">
				<div class = "preview" v-if="isFinished[index]!=0">
					<a :href="openViewer(plyPath[index])" target="_blank" class="scene-pannel">
						<img crossorigin="anonymous" :src="img" v-if="isImg[index]">
						<div class="videopath" v-else></div>
						<div class="details">
							上传时间：<span class="upload-time" v-text="uploadTime[index]"></span><br>
							生成时间：<span class="ply-time" v-text="plyTime[index]"></span>
						</div>
					</a>
				</div>
				<div class="preview" v-else>
					<img crossorigin="anonymous" :src="img" v-if="isImg[index]">
					<div class="videopath" v-else></div>
					<div class="details">
						上传时间：<span class="upload-time" v-text="uploadTime[index]"></span><br>
						生成状态：<span class="ply-time">模型正在生成中</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
.result {
	margin: 10px auto;
	width: 75vw;
	background: #76a3b7;
	color: #fff;
	padding: 40px 15px;
	text-align: center;
	border-radius: 10px;
	border: 3px dashed #fff;
	font-size: 20px;
	position: relative;

	.control {
		position: absolute;
		width: 100%;
		background: #fff;
		top: 0;
		left: 0;
		border-top-left-radius: 7px;
		border-top-right-radius: 7px;
		padding: 10px;
		padding-bottom: 4px;
		text-align: right;

		button, label {
			float: left;
			background: #6C7FBE;
			border: 2px solid #6C7FBE;
			border-radius: 3px;
			color: #fff;
			font-size: 18px;
			cursor: pointer;
			padding: 2px;
			margin: 5px;
		}
	}

	.msg {
		width: 200px;
		margin: auto;
		height: 68px;
		position: relative;
	}

	.scenes-preview {
		display: flex;
		margin: 10px auto;
		width: 100%;
		height: auto;
		border-radius: 10px;
		flex-wrap: wrap;
		padding: 10px;
		.scene-wrapper {
			margin: 10px auto;
		}
		.scene-pannel {
			flex:1;
			font-size: 20px;
			text-align: center;
			cursor: pointer;
		}
		img {
			width:300px;
			height:200px;
			border-radius:10px;
		}
	}
	.details {
		font-size: 12px;
		background: #fff;
		color: #000;
		display: flex;
		flex-direction: column;
		align-items: self-start;
		padding: 3px 6px;

		.name {
			overflow: hidden;
			height: 18px;
		}
	}
}
img {
	width: 80px;
	height: 40px;
}
a {
	text-decoration: none;
}
</style>