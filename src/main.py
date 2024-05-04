"""
This is the main module of the image classification application.
It orchestrates the application's workflow, including handling user inputs, classifying images, and displaying results.
"""

import streamlit as st
from PIL import Image
from io import BytesIO
from sidebar import display_sidebar
from image_processing import classify_images
from app_mgt import fetch_and_classify_unsplash_images, fetch_and_classify_pexels_images, fetch_alternating_images
from file_operations import save_image_to_local
from results import process_and_save_results
#from instructions import instructions

def main():
    """
    The main function of the application.
    It sets up the Streamlit app, handles user inputs, classifies images, and displays the results.
    """
    st.markdown('<style>h1{font-size: 35px;}</style>', unsafe_allow_html=True)
    st.title('Image Classification with Pre-Trained Models')
    ##st.sidebar.markdown(instructions(), unsafe_allow_html=True)

    image_files, model_name, classify, reset, num_images, site, fetch_classify, reset_images, _, _, _, _ = display_sidebar()

    if image_files is not None:
        for uploaded_file in image_files:
            image = Image.open(BytesIO(uploaded_file.read()))
            save_image_to_local(image)
            if classify:
                classification_data = classify_images(image, model_name)
                col1, col2 = st.columns(2)
                col1.image(image, caption='Uploaded Image.', use_column_width=True)
                col2.markdown("###### Classification Data")
                col2.dataframe(classification_data)
                process_and_save_results(image, model_name, classification_data)

    if fetch_classify:
        if site == 'Unsplash':
            results = fetch_and_classify_unsplash_images(num_images, model_name)
        elif site == 'Pexels':
            results = fetch_and_classify_pexels_images(num_images, model_name)
        elif site == 'Both':
            results = fetch_alternating_images(num_images, model_name)
        else:
            results = []
        st.dataframe(results)

if __name__ == "__main__":
    main()