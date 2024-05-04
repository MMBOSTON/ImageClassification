"""
This module contains functions for displaying the application's UI, including the image and its classification results.
It provides functionality to display the uploaded image and the classification results in a user-friendly format.
"""

import pandas as pd
import streamlit as st
from PIL import Image

def display_app(image_path, results):
    """
    Displays the uploaded image and its classification results in the Streamlit app.

    Parameters:
    - image_path (str): The path to the uploaded image.
    - results (pd.DataFrame): The DataFrame containing the classification results.
    """
    # Display the image
    st.image(image_path, use_column_width=True)
    
    # Display the classification results
    st.markdown("### Classification Results")
    df = pd.DataFrame(results, columns=['Class ID', 'Class Name', 'Class Rating'])
    df['Class Rating'] = df['Class Rating'].round(3)
    st.table(df)

def display_progress_bar(num_steps, current_step):
    """
    Displays a progress bar in the Streamlit app.

    Parameters:
    - num_steps (int): The total number of steps.
    - current_step (int): The current step number.

    Returns:
    - progress_bar: The progress bar object.
    """
    progress_bar = st.progress(0)