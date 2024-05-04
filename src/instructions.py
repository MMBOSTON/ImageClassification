"""
This module provides instructions for using the application.
It contains a function that returns a markdown string with detailed instructions on how to use the application.
"""

def instructions():
    """
    Returns a markdown string containing instructions for using the application.

    Returns:
    - str: The markdown string with instructions.
    """
    return """
    ### Instructions:

    **Local Image Handling**
    - Upload an image from your local host or folder using the file uploader.
    - Choose a model for classification from the dropdown menu.
    - Click the "Classify" button
    - The uploaded image will be classified, and the results will be displayed and saved to an Excel file.

    **Online Image Handling**
    - Select the number of images to download from Unsplash.
    - Click "Fetch & Classify" button to download and display the images.
    - Choose a model for classification from the dropdown menu.
    - The images will be classified, and the results will be displayed and saved to an Excel file.

    --- 
    ### User Selected Images

    """