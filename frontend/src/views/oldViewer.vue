<!-- 已经弃用！！！！！仅参考代码用 -->
<!-- 已经弃用！！！！！仅参考代码用 -->
<!-- 已经弃用！！！！！仅参考代码用 -->
<!-- 已经弃用！！！！！仅参考代码用 -->
<!-- 已经弃用！！！！！仅参考代码用 -->
<script>
import * as GaussianSplats3D from '@mkkellogg/gaussian-splats-3d';
window.onFileChange = function(arg, fileNameLabelID) {
	const fileNameLabel = document.getElementById(fileNameLabelID);
	const url = arg.value;
	let lastForwardSlash = url.lastIndexOf('/');
	let lastBackwardSlash = url.lastIndexOf('\\');
	const lastSlash = Math.max(lastForwardSlash, lastBackwardSlash);
	fileNameLabel.innerHTML = url.substring(lastSlash + 1);
}

window.viewsplat = function() {
	const viewFile = document.getElementById("viewFile");
	const alphaRemovalThreshold = 5;

	let cameraUpArray = [0, -1, -0.6];
	let cameraPositionArray = [-1, -4, 6];
	let cameraLookAtArray = [0, 4, 0];
	// let antialiased = document.getElementById("antialiased").checked;

	// cameraUpArray = cameraUpArray.split(',');
	// cameraPositionArray = cameraPositionArray.split(',');
	// cameraLookAtArray = cameraLookAtArray.split(',');

	// if (!viewFile.files[0]) {
	// setViewError("Please choose a file to view.");
	// return;
	// } else if (isNaN(alphaRemovalThreshold) || alphaRemovalThreshold < 0 || alphaRemovalThreshold > 255) {
	// setViewError("Invalid alpha remval threshold.");
	// return;
	// }

	// if (cameraUpArray.length !== 3) {
	// setViewError("Camera up must contain 3 elements.");
	// return;
	// }

	// if (cameraPositionArray.length !== 3) {
	// setViewError("Camera position must contain 3 elements.");
	// return;
	// }

	// if (cameraLookAtArray.length !== 3) {
	// setViewError("Camera look-at must contain 3 elements.");
	// return;
	// }

	// for (let i = 0; i < 3; i++) {
	// 	cameraUpArray[i] = parseFloat(cameraUpArray[i]);
	// 	cameraPositionArray[i] = parseFloat(cameraPositionArray[i]);
	// 	cameraLookAtArray[i] = parseFloat(cameraLookAtArray[i]);

	// 	if (isNaN(cameraUpArray[i])) {
	// 		setViewError("Invalid camera up.");
	// 		return;
	// 	}

	// 	if (isNaN(cameraPositionArray[i])) {
	// 		setViewError("Invalid camera position.");
	// 		return;
	// 	}

	// 	if (isNaN(cameraLookAtArray[i])) {
	// 		setViewError("Invalid camera look-at.");
	// 		return;
	// 	}
	// }

	const viewFileName = viewFile.files[0].name.trim();
	const format = GaussianSplats3D.LoaderUtils.sceneFormatFromPath(viewFileName);

	// currentAlphaRemovalThreshold = alphaRemovalThreshold;
	// currentCameraUpArray = cameraUpArray;
	// currentCameraPositionArray = cameraPositionArray;
	// currentCameraLookAtArray = cameraLookAtArray;
	// currentAntialiased = antialiased;

	try {
		const fileReader = new FileReader();
		fileReader.onload = function(){
			try {
				runViewer(fileReader.result, format, alphaRemovalThreshold, cameraUpArray, cameraPositionArray, cameraLookAtArray, false);
			} catch (e) {
				console.error(e);
				// setViewError("Could not view scene.");
			}
		}
		// setViewStatus("Loading scene...");
		fileReader.readAsArrayBuffer(viewFile.files[0]);
	} catch (e) {
		console.error(e);
		// setViewError("Could not view scene.");
	}
}
function runViewer(splatBufferData, format, alphaRemovalThreshold, cameraUpArray, cameraPositionArray, cameraLookAtArray, antialiased) {
	const viewerOptions = {
		'cameraUp': cameraUpArray,
		'initialCameraPosition': cameraPositionArray,
		'initialCameraLookAt': cameraLookAtArray,
		'halfPrecisionCovariancesOnGPU': false,
		'antialiased': antialiased || false
	};
	const splatBufferOptions = {
		'splatAlphaRemovalThreshold': alphaRemovalThreshold
	};
	const splatBufferPromise = fileBufferToSplatBuffer({data: splatBufferData}, format, alphaRemovalThreshold, 0);
	splatBufferPromise.then((splatBuffer) => {
		// document.getElementById("demo-content").style.display = 'none';
		document.body.style.backgroundColor = "#000000";
		history.pushState("ViewSplat", null);
		const viewer = new GaussianSplats3D.Viewer(viewerOptions);
		viewer.addSplatBuffers([splatBuffer], [splatBufferOptions])
		.then(() => {
			viewer.start();
		});
	});
	}

function fileBufferToSplatBuffer(fileBufferData, format, alphaRemovalThreshold, compressionLevel, sectionSize, sceneCenter, blockSize, bucketSize) {
	if (format === GaussianSplats3D.SceneFormat.Ply) {
		return GaussianSplats3D.PlyLoader.loadFromFileData(fileBufferData.data, alphaRemovalThreshold, compressionLevel, sectionSize, sceneCenter, blockSize, bucketSize);
	} else {
		if (format === GaussianSplats3D.SceneFormat.Splat) {
			return GaussianSplats3D.SplatLoader.loadFromFileData(fileBufferData.data, alphaRemovalThreshold, compressionLevel, sectionSize, sceneCenter, blockSize, bucketSize);
		} else {
			return GaussianSplats3D.KSplatLoader.loadFromFileData(fileBufferData.data);
		}
	}
}

export default {
	name: "ViewerPage"
}
</script>

<template>
	<div class="content">
		<div class="viewer">
			<label for="viewFile">
				<span class="glyphicon glyphicon-folder-open" aria-hidden="true">
					<span class="button">Choose File</span>
				</span>
				<input type="file" id="viewFile" style="display:none" onchange="window.onFileChange(this, 'viewFileName')">
			</label>
			<span id="viewFileName" style="padding-left: 15px; color: #333333">(No file chosen)</span>
			<span class="button" onclick="window.viewsplat()">View</span>
			<span class="button" onclick="reset()">Reset</span>
		</div>
	</div>
</template>

<style scoped>
@import '../style.css'
</style>
