"""
This module handles file operations, including creating directories, deleting directories, saving uploaded images, and saving fetched images.
It provides functionality to manage the file system for the application, ensuring that images are saved in the appropriate locations.
"""

import glob
import io
import os
import shutil
import time
import pandas as pd
import streamlit as st

# Define the output directory
output_dir = os.path.abspath('output')

def create_directory(directory):
    """
    Creates a directory if it does not exist.

    Parameters:
    - directory (str): The path to the directory to be created.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def delete_directory(directory):
    """
    Deletes a directory and all its contents.

    Parameters:
    - directory (str): The path to the directory to be deleted.
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)

def reset_directory(directory):
    """
    Resets a directory by deleting and recreating it.

    Parameters:
    - directory (str): The path to the directory to be reset.
    """
    delete_directory(directory)
    create_directory(directory)

def save_uploaded_image(image, image_path):
    """
    Saves the uploaded image file to the specified path.

    Parameters:
    - image (PIL.Image): The image to be saved.
    - image_path (str): The path where the image will be saved.
    """
    # Ensure the directory of the image path exists
    create_directory(os.path.dirname(image_path))
    
    # Save the uploaded image file
    with open(image_path, 'wb') as f:
        if isinstance(image, io.BytesIO): # If image is an uploaded file
            f.write(image.getvalue())

def save_fetched_image(content, image_path):
    """
    Saves the fetched image content to the specified path.

    Parameters:
    - content (bytes): The content of the fetched image.
    - image_path (str): The path where the image will be saved.
    """
    # Ensure the directory of the image path exists
    create_directory(os.path.dirname(image_path))
    
    # Save the fetched image content
    with open(image_path, 'wb') as f:
        f.write(content)

def check_directory_exists(directory):
    """
    Checks if a directory exists.

    Parameters:
    - directory (str): The path to the directory to check.

    Returns:
    - bool: True if the directory exists, False otherwise.
    """
    return os.path.exists(directory)

def check_write_permissions(directory):
    """
    Checks if you have write permissions to a directory.

    Parameters:
    - directory (str): The path to the directory to check.

    Returns:
    - bool: True if write permissions are granted, False otherwise.
    """
    return os.access(directory, os.W_OK)

def reset_app(directory):
    """
    Resets the application by deleting all output files and displaying a message in the sidebar.

    Parameters:
    - directory (str): The path to the directory to be reset.
    """
    # Delete all output files
    for file in glob.glob("output/*"):
        os.remove(file)

    # Display a message in the sidebar
    st.sidebar.text('Please manually remove the uploaded\nfiles due to a Streamlit limitation.')

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_image_to_local(image, directory='local_images'):
    """
    Saves an image to the local file system.

    Parameters:
    - image (PIL.Image): The image to be saved.
    - directory (str): The directory where the image will be saved. Default is 'local_images'.
    """
    # Ensure the directory exists
    create_directory(directory)
    
    # Generate a unique filename using the current time
    filename = f'{time.time()}.png'
    image_path = os.path.join(directory, filename)
    
    # Save the image
    image.save(image_path)

def delete_uploaded_images(directory='local_images'):
    """
    Deletes all uploaded images from the specified directory.
    """
    for file in glob.glob(f"{directory}/*"):
        os.remove(file)
