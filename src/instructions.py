def instructions():
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
    """  # Add closing triple quote here

def classification_data_title():
    return "#### Classification Data"