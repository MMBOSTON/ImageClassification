import glob
import io
import os
import shutil
import time
import pandas as pd
import streamlit as st

##from sidebar import update_progress_bar

# Define the output directory
output_dir = os.path.abspath('output')

# Create a directory if it does not exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Delete a directory and all its contents
def delete_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

# Reset a directory (delete and recreate it)
def reset_directory(directory):
    delete_directory(directory)
    create_directory(directory)

# Save the uploaded image file
def save_uploaded_image(image, image_path):
    # Ensure the directory of the image path exists
    create_directory(os.path.dirname(image_path))

    # Save the uploaded image file
    with open(image_path, 'wb') as f:
        if isinstance(image, io.BytesIO):  # If image is an uploaded file
            f.write(image.getvalue())

# Save the fetched image content
def save_fetched_image(content, image_path):
    # Ensure the directory of the image path exists
    create_directory(os.path.dirname(image_path))

    # Save the fetched image content
    with open(image_path, 'wb') as f:
        f.write(content)

# Check if a directory exists
def check_directory_exists(directory):
    return os.path.exists(directory)

# Check if you have write permissions to a directory
def check_write_permissions(directory):
    return os.access(directory, os.W_OK)

def reset_app(directory):
    # Delete all output files
    for file in glob.glob("output/*"):
        os.remove(file)

    # Display a message in the sidebar
    st.sidebar.text('Please manually remove the uploaded\nfiles due to a Streamlit limitation.')

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_image_to_local(image, directory='local_images'):
    # Ensure the directory exists
    create_directory(directory)

    # Generate a unique filename using the current time
    filename = f'{time.time()}.png'
    image_path = os.path.join(directory, filename)

    # Save the image
    image.save(image_path)