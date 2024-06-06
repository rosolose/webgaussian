<script>
export default {
	name: "HomePage",
	data() {
		return {
			jsonData: [
				// 首页demo合适的相机位置
				{
					id : "forklift",
					position : [-0.97, -2.68, 6.96],
					lookAt : [-0.06, 5.65, 1.40]
				},
				{
					id : "inkbox",
					position : [-0.42, 8.64, -8.90],
					lookAt : [ 0.00, 4.00, 0.00]
				},
				{
					id : "bonsai",
					position : [1.73, -3.57, 5.34],
					lookAt : [-0.03, 5.63, 1.69]
				}
			]
		}
	},
	methods: {
		openViewer:function(id) {
			const obj = this.jsonData.find(item => item.id === id)
			return '#/viewer?id='+id+'&local=1'+"&position="+obj.position+"&lookAt="+obj.lookAt
		}
	},
}
</script>
<template>
	<div>
		<div class="title">
			<h2>效果演示</h2>
		</div>
		<div class="scenes">
			<a :href="openViewer('forklift')" target="_blank" class="scene-pannel">
				<img src="../assets/image/forklift.png"><br>
				<span class="pannel-title">铲车</span>
			</a>
			<a :href="openViewer('inkbox')" target="_blank" class="scene-pannel">
				<img src="../assets/image/inkbox.png"><br>
				<span class="pannel-title">墨水盒</span>
			</a>
			<a :href="openViewer('bonsai')" target="_blank" class="scene-pannel">
				<img src="../assets/image/bonsai.png"><br>
				<span class="pannel-title">盆景</span>
			</a>
		</div>
	</div>
</template>
<style scoped>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}
a {
	text-decoration: none;
	color: #315f8a;
}
img {
	width:300px;
	height:200px;
	border-radius:10px;
}
.scenes {
	margin: 10px auto;
	width: 100%;
	height: auto;
	border-radius: 10px;
	display: flex;
	flex-wrap: wrap;
	padding: 10px;
}
.scene-pannel {
	flex:1;
	font-size: 20px;
	text-align: center;
	cursor: pointer;
}
h2 {
	text-align: center;
}
</style>