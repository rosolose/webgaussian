<template>
	<div>
		<!-- 导航栏 -->
		<nav class="header" v-show="!$route.meta.hideHeader">
			<div class="logo">Web 3DGS</div>
			<ul class="menu">
				<li><a href="#/">首  页</a></li>
				<li><a href="#/train">三维重建</a></li>
				<li><a href="#/results">查阅结果</a></li>
			</ul>
		</nav>
		<!-- 内容栏 -->
		<div class='content'>
			<router-view></router-view>
		</div>
	</div>
</template>

<script>
export default {
	name: "Header",
}
</script>

<style scoped>
@import '../assets/css/header.css'
</style>
