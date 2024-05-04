"""
This module handles the fetching and classifying of images from Unsplash and Pexels.
It uses the `fetch_images` function to fetch images from the selected site, save them locally, and then classify them using the specified model.
The `fetch_and_classify_unsplash_images` and `fetch_and_classify_pexels_images` functions are specifically designed for fetching and classifying images from Unsplash and Pexels, respectively.
"""
import streamlit as st
from io import BytesIO
import requests
import os
from PIL import Image
from file_operations import save_fetched_image, create_directory, delete_uploaded_images
from image_processing import classify_images
from api import check_api_usage, load_api_access_key
import time
import random

# Check if Streamlit's session state is available
if 'session_state' not in st.__dict__:
    import SessionState
    st.session_state = SessionState.get(reset_fetched_images=False)

def reset_fetched_images_state():
    """
    Resets the state related to fetched images.
    This function should be called before any widgets that depend on the session state are instantiated.
    """
    # Logic to reset the state of fetched images
    # For example, clearing directories or resetting specific session state variables
    delete_uploaded_images('unsplash_images') # Delete images fetched from Unsplash
    delete_uploaded_images('pexels_images') # Delete images fetched from Pexels
    st.session_state['reset_fetched_images'] = False # Reset the flag after handling

def fetch_images(directory, filename, num_images, site, model_name, fetch_classify):
    api_key = load_api_access_key(site)
    if api_key is None:
        return []
    create_directory(directory)
    image_paths = []
    page = 1
    progress_bar = st.progress(0)
    if not fetch_classify:
        return []
    
    for i in range(num_images):
        if not check_api_usage(site):
            print(f"API usage limit reached for {site}. Please wait or reset the API usage.")
            return image_paths
        try:
            if site == 'Unsplash':
                response = requests.get(f'https://api.unsplash.com/photos/random', headers={'Authorization': f'Client-ID {api_key}'})
                url = response.json()['urls']['full']
            elif site == 'Pexels':
                response = requests.get(
                    'https://api.pexels.com/v1/search',
                    headers={'Authorization': api_key},
                    params={'query': 'nature', 'per_page': 1, 'page': page}
                )
                if response.status_code == 200:
                    if 'photos' in response.json() and len(response.json()['photos']) > 0:
                        url = response.json()['photos'][0]['src']['original']
                        page += 1
                    else:
                        print(f"No photos found in Pexels response. Response: {response.json()}")
                        continue
                else:
                    print(f"Failed to fetch image from {site}. Status code: {response.status_code}")
                    print(f"Response: {response.json()}")
                    continue
            image_response = requests.get(url)
            timestamp = int(time.time())
            unique_filename = f"{filename}_{timestamp}.jpg"
            image_path = os.path.join(directory, unique_filename)
            save_fetched_image(image_response.content, image_path)
            image_paths.append(image_path)
            image = Image.open(BytesIO(image_response.content))
            col1, col2 = st.columns(2)
            col1.image(image, use_column_width=True)
            classification_data = classify_images(image, model_name)
            col2.markdown("###### Classification Data")
            col2.dataframe(classification_data)
            progress_bar.progress((i + 1) / num_images)
        except Exception as e:
            print(f"An error occurred while fetching images from {site}: {e}")
            return image_paths
    progress_bar.progress(1.0)
    st.success(f"All {site} images have been classified!")
    return image_paths

def fetch_and_classify_unsplash_images(num_images, model_name, fetch_classify):
    if 'reset_fetched_images' in st.session_state and st.session_state.reset_fetched_images:
        reset_fetched_images_state()
    return fetch_images('unsplash_images', 'unsplash', num_images, 'Unsplash', model_name, fetch_classify)
    # Only display the success message if not resetting
    if not is_resetting:
        st.success("All Unsplash images have been classified!")
        
def fetch_and_classify_pexels_images(num_images, model_name, fetch_classify):
    if 'reset_fetched_images' in st.session_state and st.session_state.reset_fetched_images:
        reset_fetched_images_state()
    return fetch_images('pexels_images', 'pexels', num_images, 'Pexels', model_name, fetch_classify)

def fetch_alternating_images(num_images, model_name, fetch_classify):
    # Check if the reset_fetched_images attribute exists in st.session_state and if it's True
    if 'reset_fetched_images' in st.session_state and st.session_state.reset_fetched_images:
        reset_fetched_images_state()
    results = []
    for i in range(num_images):
        if fetch_classify:
            if random.choice([True, False]):
                result = fetch_and_classify_unsplash_images(1, model_name, fetch_classify)
            else:
                result = fetch_and_classify_pexels_images(1, model_name, fetch_classify)
            results.append(result)
    return results