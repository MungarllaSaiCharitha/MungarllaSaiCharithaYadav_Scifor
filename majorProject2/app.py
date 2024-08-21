import streamlit as st
import requests
import os
from PIL import Image, ImageDraw
import io
import numpy as np

api_key = "229fc1b7aeab4523b7562e6c698f009f"
# Function to call the Microsoft Azure Face API
def recognize_faces(image_data, api_key, endpoint):
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/octet-stream"
    }
    
    params = {
        "returnFaceId": "true",
        "returnFaceLandmarks": "false",
        "returnFaceAttributes": "age,gender,smile,facialHair,glasses,emotion"
    }
    
    response = requests.post(endpoint, params=params, headers=headers, data=image_data)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    
    return response.json()

# Streamlit app
st.title("Face Recognition App with Azure Face API")

st.sidebar.title("Options")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Add Face", "Identify Face"])

# Sidebar for API key and endpoint input
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("API Key", type="password")
endpoint = st.sidebar.text_input("Endpoint URL")

if app_mode == "Add Face":
    st.header("Add a new face")
    name = st.text_input("Enter the name of the person")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file and name:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded Image of {name}", use_column_width=True)

        # Save the face with the provided name locally
        if not os.path.exists('known_faces'):
            os.makedirs('known_faces')
        person_path = os.path.join('known_faces', f"{len(os.listdir('known_faces'))}_{name}")
        os.makedirs(person_path)
        image.convert("L").save(os.path.join(person_path, "1.jpg"))

        st.success(f"Face of {name} has been saved successfully!")

elif app_mode == "Identify Face":
    st.header("Identify faces from camera or uploaded image")
    mode = st.radio("Choose input method:", ("Webcam", "Upload Image"))

    if mode == "Webcam":
        run = st.checkbox("Run")
        FRAME_WINDOW = st.image([])

        camera = cv2.VideoCapture(0)
        while run:
            ret, frame = camera.read()
            if not ret:
                st.error("Failed to capture image")
                break

            # Convert frame to bytes for API call
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            # Call Azure Face API
            if api_key and endpoint:
                try:
                    faces = recognize_faces(img_bytes, api_key, endpoint)
                    for face in faces:
                        rect = face['faceRectangle']
                        cv2.rectangle(frame, (rect['left'], rect['top']),
                                      (rect['left'] + rect['width'], rect['top'] + rect['height']),
                                      (0, 255, 0), 2)
                except Exception as e:
                    st.error(f"Failed to process image: {e}")

            FRAME_WINDOW.image(frame[:, :, ::-1])
        camera.release()

    elif mode == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image to identify", type=["jpg", "png"])

        if uploaded_file and api_key and endpoint:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Convert image to bytes for API call
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="JPEG")
            img_bytes = img_bytes.getvalue()

            # Call Azure Face API
            try:
                faces = recognize_faces(img_bytes, api_key, endpoint)
                draw = ImageDraw.Draw(image)
                for face in faces:
                    rect = face['faceRectangle']
                    draw.rectangle([(rect['left'], rect['top']),
                                    (rect['left'] + rect['width'], rect['top'] + rect['height'])],
                                   outline="red", width=3)
                st.image(image, caption="Processed Image", use_column_width=True)
            except Exception as e:
                st.error(f"Failed to process image: {e}")
        else:
            st.write("Please upload an image and configure the API.")
