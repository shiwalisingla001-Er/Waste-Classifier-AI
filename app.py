import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Page UI setup
st.set_page_config(page_title="AI Waste Classifier", page_icon="♻️")
st.title("♻️ Real-Time Waste Classification")
st.write("Upload a photo to detect if it's Biodegradable or Non-Biodegradable.")

# Model load (MobileNetV2)
@st.cache_resource
def get_model():
    return tf.keras.applications.MobileNetV2(weights="imagenet")

model = get_model()

# Classification Logic
def check_waste(label):
    bio = ['banana', 'apple', 'orange', 'lemon', 'corn', 'broccoli', 'leaf', 'wood', 'paper', 'cardboard']
    label = label.lower()
    if any(x in label for x in bio):
        return "BIODEGRADABLE", "Natural waste, safe for environment. ✅"
    else:
        return "NON-BIODEGRADABLE", "Recyclable or hazardous waste. ⚠️"

# Upload Button
file = st.file_uploader("Upload Waste Photo", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    # Process image for AI
    img_resized = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
    img_array = np.asarray(img_resized)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(img_batch)

    # Predict
    preds = model.predict(img_preprocessed)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0]
    name = decoded[1].replace('_', ' ')
    
    result, tip = check_waste(name)
    
    # Result Display
    st.success(f"Detected: {name.upper()}")
    if "NON" in result:
        st.error(f"Category: {result}")
    else:
        st.success(f"Category: {result}")
    st.info(f"Note: {tip}")
