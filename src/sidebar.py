"""
This module is responsible for displaying the application's sidebar, which includes options for users to upload images, select models, and fetch images from Unsplash or Pexels.
It provides functionality to handle user interactions through the sidebar.
"""

import streamlit as st
from instructions import instructions

def display_sidebar():
    """
    Displays the application's sidebar with instructions and options for users.
    """
    
    st.sidebar.markdown(instructions(), unsafe_allow_html=True)
    image_files = st.sidebar.file_uploader("Upload Images", type=['jpg', 'png', 'jpeg', 'PNG', 'GIF'], accept_multiple_files=True)
    model_name_upload = st.sidebar.selectbox('Select Model for Uploaded Images', ['ResNet50', 'VGG16', 'InceptionV3', 'Other'])

    # Create two columns for the buttons
    col1, col2 = st.sidebar.columns(2)

    # Place the "Classify" button in the first column
    classify = col1.button('Classify', key='classify_button')

    # Place the "Reset" button in the second column
    reset = col2.button('Reset', key='reset_button')

    # Add a horizontal line to separate sections
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Load Images from websites", unsafe_allow_html=True)

    num_images = max(st.sidebar.slider('Number of Images (Slider)', 0, 200, 0), st.sidebar.number_input('Number of Images (Input)', 0, 200, 0))
    site = st.sidebar.selectbox('Select the site to fetch images from:', ['Unsplash', 'Pexels', 'Both'])
    model_name_fetch = st.sidebar.selectbox('Select Model for Fetched Images', ['ResNet50', 'VGG16', 'InceptionV3', 'Other'])

    # Create two columns for the fetch and reset buttons
    col3, col4 = st.sidebar.columns(2)

    # Place the "Fetch & Classify" button in the first column with a unique key
    fetch_classify = col3.button('Fetch & Classify', key='fetch_classify_button')

    # Place the "Reset" button in the second column with a unique key
    reset_images = col4.button('Reset', key='reset_images_button')

    return image_files, model_name_upload, classify, reset, num_images, site, model_name_fetch, fetch_classify, reset_images
