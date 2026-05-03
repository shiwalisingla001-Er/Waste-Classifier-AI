import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Page UI
st.set_page_config(page_title="Smart Waste AI", page_icon="♻️")
st.title("♻️ Automated Waste Classification")
st.write("### Project by: Shiwali Singla")
st.write("---")

# Load Brain (MobileNetV2 AI Model)
@st.cache_resource
def load_my_model():
    # 'imagenet' weights use karke model ko pehle se hi lakho cheezein pata hain
    return tf.keras.applications.MobileNetV2(weights="imagenet")

model = load_my_model()

# Classification Function
def classify_waste(img, model):
    size = (224, 224)    
    image = ImageOps.fit(img, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    preds = model.predict(data)
    # AI se top 3 predictions nikalna
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
    return decoded

# Upload Section
file = st.file_uploader("Show me the waste material...", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption='Scanned Image', use_column_width=True)
    
    with st.spinner('AI Neural Network is analyzing...'):
        results = classify_waste(img, model)
        top_item = results[0][1].lower()

    st.info(f"**AI thinks this is:** {top_item.replace('_', ' ')}")

    # ---------------------------------------------------------
    # SOLID LOGIC FOR BIO vs NON-BIO
    # ---------------------------------------------------------
    bio_list = [
        'apple', 'banana', 'orange', 'lemon', 'corn', 'pineapple', 'fruit',
        'paper', 'notebook', 'envelope', 'carton', 'packet', 'tissue', 'book',
        'leaf', 'wood', 'tree', 'bread', 'food', 'vegetable', 'meat', 'grass'
    ]
    
    # Check if the AI detection matches any Bio items
    is_bio = any(word in top_item for word in bio_list)

    if is_bio:
        st.success("🎯 **Result: BIODEGRADABLE**")
        st.write("♻️ **Recommendation:** Can be composted or recycled as paper waste.")
    else:
        st.error("🎯 **Result: NON-BIODEGRADABLE**")
        st.write("🚫 **Recommendation:** Must be sent for industrial recycling (Plastic/Metal/Glass).")

    # Extra Details for Marks
    with st.expander("See AI Confidence Score"):
        for i, res in enumerate(results):
            st.write(f"{i+1}. {res[1]}: {round(res[2]*100, 2)}%")

st.write("---")
st.caption("Developed for College Project Submission - Shiwali Singla")
