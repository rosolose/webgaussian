<script>

export default{
	name: "TestPage",
	methods: {
		openViewer:function() {
			return '#/viewer?id=1&local=0'
		}
	}
}
</script>

<template>
	<div>
		<a :href="openViewer()" target="_blank">START!</a>
	</div>
</template>
<style scoped>
a {
	margin: 80px;
	font-size: 80px;
}
</style>