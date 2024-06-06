import { createApp } from 'vue';
import './style.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Train from './views/Train.vue'
import Results from './views/Results.vue'
import Test from './views/Test.vue'
import Viewer from './views/Viewer.vue'
import ImageUploader from './views/ImageUploader.vue'
import VideoUploader from './views/VideoUploader.vue';
import { createRouter, createWebHashHistory } from 'vue-router';

const router = createRouter({
	history: createWebHashHistory(),
	routes: [
		{
			path: '/',
			name: "Home",
			component: Home,
			meta: {
				hideHeader: false
			},
		},
		{
			path: '/train',
			name: "Train",
			component: Train,
			meta: {
				hideHeader: false
			},
		},
		{
			path: '/results',
			name: "Results",
			component: Results,
			meta: {
				hideHeader: false
			},
		},
		{
			path: '/test',
			name: "Test",
			component: Test,
			meta: {
				hideHeader: false
			},
		},
		{
			path: '/viewer',
			name: "Viewer",
			component: Viewer,
			meta: {
				hideHeader: true
			},
		},
		{
			path:'/imageuploader',
			name:"ImageUploader",
			component: ImageUploader,
			meta: {
				hideHeader: false
			}
		},
		{
			path:'/videouploader',
			name:"VideoUploader",
			component: VideoUploader,
			meta: {
				hideHeader: false
			}
		}
	]
});

const app = createApp(App);
app.use(router);
app.mount('#app');