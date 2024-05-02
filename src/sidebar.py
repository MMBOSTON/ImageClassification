import streamlit as st
from instructions import instructions

def display_sidebar():
    st.sidebar.title('Options')
    image_files = st.sidebar.file_uploader("Upload Images", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
    
    # Add a dropdown for model selection for uploaded images
    model_name_upload = st.sidebar.selectbox('Select Model for Uploaded Images', ['ResNet50', 'VGG16', 'InceptionV3', 'Other'])

    col1, col2 = st.sidebar.columns(2)  # Create two columns

    with col1:
        classify = st.button('Classify', key='classify_user_images')  # Classify button

    with col2:
        reset = st.button('Reset', key='reset_user_images')  # Reset button

    st.sidebar.markdown('---')  # Horizontal bar

    num_images_slider = st.sidebar.slider('Number of Images (Slider)', 0, 200, 0)
    num_images_input = st.sidebar.number_input('Number of Images (Input)', 0, 200, 0)

    num_images = max(num_images_slider, num_images_input)

    site = st.sidebar.selectbox('Select the site to fetch images from:', ['Unsplash', 'Pexels', 'Both'])

    model_name_fetch = st.sidebar.selectbox('Select Model for Fetched Images', ['ResNet50', 'VGG16', 'InceptionV3', 'Other'])

    col4, col5 = st.sidebar.columns(2)  

    with col4:
        fetch_classify = st.button('Fetch & Classify', key='fetch_classify_images')  
    
    with col5:
        reset_images = st.button('Reset', key='reset_fetched_images')  
    
    return (
        image_files, model_name_upload, classify, reset, num_images, site, 
        model_name_fetch, fetch_classify, reset_images, None, None, None 
    )