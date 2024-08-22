import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image

# Function to create a face recognizer and train it with known faces
def train_recognizer(data_path):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, labels = [], []

    for name in os.listdir(data_path):
        person_path = os.path.join(data_path, name)
        if os.path.isdir(person_path):
            label = int(name.split('_')[0])
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces.append(image)
                labels.append(label)
    
    face_recognizer.train(faces, np.array(labels))
    return face_recognizer

# Function to save a new face with a unique label
def save_face(image, name):
    if not os.path.exists('known_faces'):
        os.makedirs('known_faces')
    person_path = os.path.join('known_faces', f"{len(os.listdir('known_faces'))}_{name}")
    os.makedirs(person_path)
    image.save(os.path.join(person_path, "1.jpg"))

# Load known faces on start
data_path = 'known_faces'
if os.path.exists(data_path):
    face_recognizer = train_recognizer(data_path)
else:
    face_recognizer = None

# Streamlit app
st.title("Face Recognition App")

st.sidebar.title("Options")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Add Face", "Identify Face"])

if app_mode == "Add Face":
    st.header("Add a new face")
    name = st.text_input("Enter the name of the person")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file and name:
        image = Image.open(uploaded_file).convert("L")
        st.image(image, caption=f"Uploaded Image of {name}", use_column_width=True)
        save_face(image, name)
        st.success(f"Face of {name} has been saved successfully!")
        face_recognizer = train_recognizer(data_path)  # Retrain recognizer with new face

elif app_mode == "Identify Face":
    st.header("Identify faces from camera or uploaded image")
    mode = st.radio("Choose input method:", ("Webcam", "Upload Image"))

    if mode == "Webcam":
        st.subheader("Take a picture")
        img_file_buffer = st.camera_input("Capture an image")

        if img_file_buffer is not None:
            # To read image file buffer as a PIL Image:
            img = Image.open(img_file_buffer)

            # To convert PIL Image to numpy array:
            img_array = np.array(img)

            # Process the image for face detection and recognition
            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0 and face_recognizer:
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    label, confidence = face_recognizer.predict(face_roi)
                    name = "Unknown"
                    if confidence is not None and confidence < 100:
                        name = [name for name in os.listdir(data_path) if name.startswith(f"{label}_")][0].split('_')[1]

                    cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img_array, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                st.image(img_array, caption="Processed Image", use_column_width=True)
            else:
                st.write("No faces detected or face recognizer is not trained.")

    elif mode == "Upload Image":
        uploaded_file = st.file_uploader("Upload an image to identify", type=["jpg", "png"])

        if uploaded_file:
            image = Image.open(uploaded_file).convert("L")
            st.image(image, caption="Uploaded Image", use_column_width=True)
            image_np = np.array(image)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(image_np, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0 and face_recognizer:
                for (x, y, w, h) in faces:
                    face_roi = image_np[y:y+h, x:x+w]
                    label, confidence = face_recognizer.predict(face_roi)
                    name = "Unknown"
                    if confidence is not None and confidence < 100:
                        name = [name for name in os.listdir(data_path) if name.startswith(f"{label}_")][0].split('_')[1]

                    cv2.rectangle(image_np, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(image_np, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                st.image(image_np, caption="Processed Image", use_column_width=True)
            else:
                st.write("No faces detected or face recognizer is not trained.")
