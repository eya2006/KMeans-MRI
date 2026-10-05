import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from PIL import Image
import io

st.set_page_config(
    page_title="MRI K-Means Segmentation",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MRI Image Segmentation")
st.write(
    "Segment an MRI image using the K-Means clustering algorithm."
)

# Sidebar
st.sidebar.header("Settings")

k = st.sidebar.slider(
    "Number of clusters (K)",
    min_value=2,
    max_value=6,
    value=3
)

uploaded_file = st.file_uploader(
    "Upload an MRI image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Read uploaded image
    image = Image.open(uploaded_file).convert("L")
    image_array = np.array(image)

    # Prepare pixels for K-Means
    pixels = image_array.reshape((-1, 1))

    # Apply K-Means
    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(pixels)

    # Create segmented image
    centers = np.uint8(kmeans.cluster_centers_)
    segmented = centers[labels.flatten()]
    segmented = segmented.reshape(image_array.shape)

    # Display results
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original MRI")
        st.image(image_array, use_container_width=True)

    with col2:
        st.subheader(f"K-Means Segmentation (K={k})")
        st.image(segmented, use_container_width=True)

    # Download result
    result_image = Image.fromarray(segmented)

    buffer = io.BytesIO()
    result_image.save(buffer, format="PNG")

    st.download_button(
        label="⬇️ Download Segmented Image",
        data=buffer.getvalue(),
        file_name=f"segmented_k{k}.png",
        mime="image/png"
    )

else:
    st.info("👆 Upload an MRI image to start segmentation.")
