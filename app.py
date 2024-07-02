import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import random
import os
import matplotlib.pyplot as plt

# Set the directory paths for normal and pneumonia training images
TRAIN_NORMAL = "chest_xray/train/NORMAL"
TRAIN_PNEUMONIA = "chest_xray/train/PNEUMONIA"

# Load your trained model
model_path = 'pneumoniaDetectLV17.h5'
model = tf.keras.models.load_model(model_path)

# Function to preprocess the uploaded image
def preprocess_image(image):
    img = Image.open(image)
    img = img.resize((128, 128))  # Resize image to match model's expected sizing
    
    # Check if image has 3 channels (RGB)
    if img.mode != 'RGB':
        img = img.convert('RGB')  # Convert to RGB if not already
    
    img = np.asarray(img)  # Convert image to numpy array
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to display a random normal and pneumonia image
def display_comparison_images(user_image_path):
    # Open user uploaded image
    user_image = Image.open(user_image_path)
    
    # Choose a random image from the normal and pneumonia directories
    random_normal_image = random.choice(os.listdir(TRAIN_NORMAL))
    random_pneumonia_image = random.choice(os.listdir(TRAIN_PNEUMONIA))

    # Open the selected images
    normal_image = Image.open(os.path.join(TRAIN_NORMAL, random_normal_image))
    pneumonia_image = Image.open(os.path.join(TRAIN_PNEUMONIA, random_pneumonia_image))

    # Create a figure for displaying the images
    figure = plt.figure(figsize=(20, 10))

    # Display the user uploaded image in the first subplot
    subplot1 = figure.add_subplot(1, 3, 1)
    plt.imshow(user_image)
    subplot1.set_title("Uploaded Image")

    # Display the normal image in the second subplot
    subplot2 = figure.add_subplot(1, 3, 2)
    plt.imshow(normal_image)
    subplot2.set_title("Normal")

    # Display the pneumonia image in the third subplot
    subplot3 = figure.add_subplot(1, 3, 3)
    plt.imshow(pneumonia_image)
    subplot3.set_title("Pneumonia")

    # Show the figure
    st.pyplot(figure)

# Function to predict pneumonia based on user-uploaded image
def predict_pneumonia(image):
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    pneumonia_probability = prediction[0][0]
    return pneumonia_probability

# Streamlit app
def main():
    st.title('Pneumonia Detection App')
    st.write('Upload a chest X-ray image for pneumonia detection')

    # File upload
    uploaded_file = st.file_uploader("Choose a chest X-ray image ...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Temporarily save the uploaded image
        user_image_path = './user_uploaded_image.png'
        with open(user_image_path, 'wb') as f:
            f.write(uploaded_file.read())

        # Display the uploaded image
        user_image = Image.open(user_image_path)
        st.image(user_image, caption='Uploaded Image', use_column_width=True)

        # Display normal and pneumonia images for comparison
        display_comparison_images(user_image_path)

        # Predict pneumonia based on the uploaded image
        pneumonia_probability = predict_pneumonia(user_image_path)

        # Determine and display prediction result
        if pneumonia_probability > 0.5:
            st.error('High probability of Pneumonia. Please consult a doctor for further evaluation.')
        else:
            st.success('Low probability of Pneumonia. Consider regular check-ups.')

        # Remove the temporarily saved uploaded image
        os.remove(user_image_path)

# Run the app
if __name__ == '__main__':
    main()
