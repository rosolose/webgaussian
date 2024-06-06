import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		{
			name: "configure-response-headers",
			configureServer: (server) => {
				server.middlewares.use((_req, res, next) => {
					res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
					res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
					next();
				});
			},
		},
	],
	server: {
		// host: '0.0.0.0',
		// port: 5173,
		// https: false,
		// proxy: {
		// 	'/api': {
		// 		target: 'http://localhost:8000/', // 后端接口的地址
		// 		changeOrigin: true,
		// 		rewrite: (path) => path.replace(/^\/api/, '')
		// 	}
		// }
	}
});
