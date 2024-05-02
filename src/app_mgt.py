import os
from io import BytesIO

import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from api import check_api_usage, load_api_access_key, reset_api_usage_count
from file_operations import save_fetched_image, create_directory
from image_processing import classify_images

import time
import random

load_dotenv()

def fetch_images(directory, filename, num_images, site, model_name):
    api_key = load_api_access_key(site)
    if api_key is None:
        return []

    create_directory(directory)
    image_paths = []
    page = 1  # Initialize page number for Pexels

    # Create a progress bar
    progress_bar = st.progress(0)

    for i in range(num_images):
        print(f"Fetching image {i+1} of {num_images} from {site}...")
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
                        page += 1  # Increment the page number for the next request
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

            try:
                Image.open(image_path)
            except FileNotFoundError:
                print(f"Failed to open image at: {image_path}")

            image = Image.open(BytesIO(image_response.content))
            col1, col2 = st.columns(2)
            col1.image(image, use_column_width=True)
            classification_data = classify_images(image, model_name)
            col2.markdown("###### Classification Data")  # This line adds the title
            col2.dataframe(classification_data)        

            # Update the progress bar
            progress_bar.progress((i + 1) / num_images)
        except Exception as e:
            print(f"An error occurred while fetching images from {site}: {e}")
            return image_paths

    return image_paths

def fetch_and_classify_unsplash_images(num_images, model_name):
    return fetch_images('unsplash_images', 'unsplash', num_images, 'Unsplash', model_name)

def fetch_and_classify_pexels_images(num_images, model_name):
    return fetch_images('pexels_images', 'pexels', num_images, 'Pexels', model_name)


def fetch_alternating_images(num_images, model_name):
    results = []
    for i in range(num_images):
        if random.choice([True, False]):
            result = fetch_and_classify_unsplash_images(1, model_name)
        else:
            result = fetch_and_classify_pexels_images(1, model_name)
        results.append(result)
    return results