"""
This is the main module of the image classification application.
It orchestrates the application's workflow, including handling user inputs, classifying images, and displaying results.
"""

import streamlit as st
from PIL import Image
from io import BytesIO
from sidebar import display_sidebar
from image_processing import classify_images
from file_operations import save_image_to_local, delete_uploaded_images
from results import process_and_save_results
from app_mgt import fetch_and_classify_unsplash_images, fetch_and_classify_pexels_images, reset_fetched_images_state, fetch_alternating_images

def main():
    # Initialize session state if it's not already initialized
    if 'reset_fetched_images' not in st.session_state:
        st.session_state.reset_fetched_images = False
    if 'first_run' not in st.session_state:
        st.session_state.first_run = True

    st.markdown('<style>h1{font-size: 35px;}</style>', unsafe_allow_html=True)
    st.title('Image Classification with Pre-Trained Models')

    # Display the sidebar and get the values of the buttons
    image_files, model_name, classify, reset, num_images, site, fetch_classify, reset_images, _ = display_sidebar()

    # Check if the reset button was clicked and reset the state accordingly
    if reset or reset_images:
        reset_fetched_images_state()
        st.session_state.reset_fetched_images = False # Reset the flag after handling

    if st.session_state.first_run:
        st.success("Read the instructions on the left side panel for detailed steps.")
        st.session_state.first_run = False
    else:
        # Add a button to reset the session state and simulate clearing the cache and rerunning the app
        if st.button('Reset Session State'):
            st.session_state.first_run = True
            st.rerun()

        if classify:
            if image_files:
                # Initialize a progress bar
                progress_bar = st.progress(0)
                total_images = len(image_files)

                for i, uploaded_file in enumerate(image_files):
                    image = Image.open(BytesIO(uploaded_file.read()))
                    save_image_to_local(image)

                    classification_data = classify_images(image, model_name)
                    col1, col2 = st.columns(2)
                    col1.image(image, caption='Uploaded Image.', use_column_width=True)
                    col2.markdown("###### Classification Data")
                    col2.dataframe(classification_data)
                    process_and_save_results(image, model_name, classification_data)

                    # Update the progress bar
                    progress = (i + 1) / total_images
                    progress_bar.progress(progress)

                # Complete the progress bar
                progress_bar.progress(1.0)
                st.success("All images have been classified!")
            else:
                st.warning("Please upload at least one image.")

        if fetch_classify:
            if site == 'Unsplash':
                results = fetch_and_classify_unsplash_images(num_images, model_name, fetch_classify)
            elif site == 'Pexels':
                results = fetch_and_classify_pexels_images(num_images, model_name, fetch_classify)
            elif site == 'Both':
                # Implement logic for fetching and classifying images from both sites alternatively
                results = fetch_alternating_images(num_images, model_name, fetch_classify)
            else:
                results = []
            
            # Display the results DataFrame
            st.dataframe(results)

if __name__ == "__main__":
    main()