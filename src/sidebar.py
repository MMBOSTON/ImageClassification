"""
This module is responsible for displaying the application's sidebar, which includes options for users to upload images, select models, and fetch images from Unsplash or Pexels.
It provides functionality to handle user interactions through the sidebar.
"""

import streamlit as st
from instructions import instructions

def display_sidebar():
    """
    Displays the application's sidebar with instructions and options for users.

    Returns:
    - A tuple containing the user's selections and inputs from the sidebar.
    """
    st.sidebar.markdown(instructions(), unsafe_allow_html=True)
    image_files = st.sidebar.file_uploader("Upload Images", type=['jpg', 'png', 'jpeg', 'PNG', 'GIF'], accept_multiple_files=True)
    model_name_upload = st.sidebar.selectbox('Select Model for Uploaded Images', ['ResNet50', 'VGG16', 'InceptionV3', 'Other'])
    classify = st.sidebar.button('Classify', key='classify_user_images')
    reset = st.sidebar.button('Reset', key='reset_user_images')
    num_images = max(st.sidebar.slider('Number of Images (Slider)', 0, 200, 0), st.sidebar.number_input('Number of Images (Input)', 0, 200, 0))
    site = st.sidebar.selectbox('Select the site to fetch images from:', ['Unsplash', 'Pexels', 'Both'])
    model_name_fetch = st.sidebar.selectbox('Select Model for Fetched Images', ['ResNet50', 'VGG16', 'InceptionV3', 'Other'])
    fetch_classify = st.sidebar.button('Fetch & Classify', key='fetch_classify_images')
    reset_images = st.sidebar.button('Reset', key='reset_fetched_images')
    return (image_files, model_name_upload, classify, reset, num_images, site, model_name_fetch, fetch_classify, reset_images, None, None, None)