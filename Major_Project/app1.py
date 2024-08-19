import cv2  # Importing the OpenCV library for computer vision tasks
import streamlit as st  # Importing Streamlit for building interactive web applications
import numpy as np  # Importing NumPy for numerical computing
from PIL import Image  # Importing the Python Imaging Library for image processing
import time  # Importing time module to manage frame updates

# Initialize session state for the camera status
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

# Function to detect faces in live camera stream
def detect_faces():
    # Create the haar cascade for face detection using a pre-trained XML file
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Open the default camera (0) for capturing video
    cap = cv2.VideoCapture(0)

    # Create a placeholder in Streamlit to display frames
    frame_placeholder = st.empty()

    # Infinite loop to continuously capture frames from the camera
    while st.session_state.camera_active:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            st.error("Failed to capture image from camera.")
            break

        # Convert the captured frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert the frame from BGR to RGB for display in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame in the Streamlit app
        frame_placeholder.image(frame_rgb, channels="RGB")

        # Add a small delay to simulate frame rate control (optional)
        time.sleep(0.05)

    # Release the camera capture
    cap.release()

# Function to detect faces in an uploaded image
def detect_faces_in_image(uploaded_image):
    # Convert the uploaded image file to a NumPy array
    img_array = np.array(Image.open(uploaded_image))

    # Create the haar cascade for face detection using a pre-trained XML file
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # Detect faces in the grayscale image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw a rectangle around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(img_array, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting image with face detection
    st.image(img_array, channels="RGB", use_column_width=True)

# Streamlit UI
st.title("Face Detection")
st.subheader("Either Open Camera And Detect Faces Or Upload An Image And Detect Faces")

# Handle the camera stream logic
if not st.session_state.camera_active:
    if st.button("Open Camera"):
        st.session_state.camera_active = True
        detect_faces()  # Start face detection in camera
else:
    if st.button("Stop Camera"):
        st.session_state.camera_active = False

# File uploader for detecting faces in an uploaded image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    detect_faces_in_image(uploaded_image)
