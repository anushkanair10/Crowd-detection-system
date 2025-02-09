from flask import Flask, render_template, request, jsonify
import cv2
import base64
import numpy as np
import dlib
from flask_cors import CORS
import os

# Initialize the Flask app and set the current directory for templates
app = Flask(__name__, template_folder='.')  # Use the current directory as the template folder
CORS(app)  # Enable CORS for all routes in the app

# Initialize dlib's face detector
detector = dlib.get_frontal_face_detector()

@app.route('/')
def index():
    return render_template('index.html')  # index.html is in the current directory

@app.route('/detect_crowd', methods=['POST'])
def detect_crowd():
    try:
        data = request.get_json()
        image_data = data.get('image')

        # Decode the base64 image
        image_data = image_data.split(',')[1]  # Remove the "data:image/jpeg;base64," part
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Image could not be decoded'}), 400

        # Resize image for better processing
        resize_factor = 0.5
        resized_image = cv2.resize(image, (0, 0), fx=resize_factor, fy=resize_factor)
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = detector(gray_image, 1)  # Increase the second argument for better accuracy
        num_faces = len(faces)
        crowd_detected = num_faces >= 3  # Adjust the threshold as needed

        # Return results
        return jsonify({
            'crowd_detected': crowd_detected,
            'num_faces': num_faces
        })
    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({'error': 'Error processing the image'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
