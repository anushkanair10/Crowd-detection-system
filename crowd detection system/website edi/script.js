// Set up the webcam stream
let video = document.createElement('video');
let canvas = document.createElement('canvas');
let ctx = canvas.getContext('2d');
let stream = null;

async function captureImage() {
    try {
        // Start webcam if not already started
        if (!stream) {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.play();
        }

        // Set canvas size to video dimensions
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Capture the image from the webcam
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        let base64Image = canvas.toDataURL('image/jpeg');

        // Send the captured image to the server for crowd detection
        let response = await fetch('/detect_crowd', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: base64Image })
        });

        if (response.ok) {
            let result = await response.json();
            document.getElementById('detectionMessage').textContent = result.crowd_detected ? "Crowd detected!" : "No crowd detected.";
            document.getElementById('count').textContent = result.num_faces;
        } else {
            throw new Error("Failed to process image: " + response.statusText);
        }

    } catch (error) {
        console.error("Error capturing image:", error);
        document.getElementById('detectionMessage').textContent = "An error occurred while processing the image.";
    }
}
