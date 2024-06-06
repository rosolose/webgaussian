<script>
import * as GaussianSplats3D from '@mkkellogg/gaussian-splats-3d';

export default {
	name: "ViewerPage",
	data: () => ({

	}),
	created(){
		// 获取当前页面的 URL
		const currentURL = window.location.href
		// 解析 URL 中的查询参数
		const urlParams = new URLSearchParams(currentURL.split('?')[1])

		// 获取参数 id 和 local 的值
		const id = urlParams.get('id')
		const local = urlParams.get('local')

		let modelPath = ""
		if (local==1) {
			modelPath = "src/assets/model/" + id + ".ksplat";
			const position = urlParams.get('position').split(',').map(parseFloat)
			const lookAt = urlParams.get('lookAt').split(',').map(parseFloat)
			this.startViewer(modelPath, position, lookAt)
		}
		else {
			modelPath = id
			this.startViewer(modelPath)
		}
		console.log(modelPath)
	},
	methods: {
		startViewer(path, position=[-1,-4,6], lookAt=[0,4,4]) {
			const viewer = new GaussianSplats3D.Viewer({
				'cameraUp': [0, -1, -0.6],
				'initialCameraPosition': position,
				'initialCameraLookAt': lookAt
			});
			viewer.addSplatScene(path, {
				'splatAlphaRemovalThreshold': 5,
				'showLoadingUI': true,
				'position': [0, 1, 0],
				'rotation': [0, 0, 0, 1],
				'scale': [1.5, 1.5, 1.5]
			})
			.then(() => {
				viewer.start();
			});
		}
	},
}
</script>
<template>
	<h1>Viewer</h1>
</template>