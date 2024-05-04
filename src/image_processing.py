"""
This module contains functions for processing images, including selecting the appropriate model, preprocessing the image, and classifying the image using the selected model.
It provides functionality to classify images using pre-trained models and convert the classification results into a DataFrame for easy display and further processing.
"""

import numpy as np
import pandas as pd
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.applications import VGG16, InceptionV3
from tensorflow.keras.preprocessing import image as image_utils
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def select_model(model_name):
    """
    Selects the appropriate model based on the user's choice.

    Parameters:
    - model_name (str): The name of the model to use for classification.

    Returns:
    - model: The selected model.
    """
    if model_name == 'ResNet50':
        return ResNet50(weights='imagenet')
    elif model_name == 'VGG16':
        return VGG16(weights='imagenet')
    elif model_name == 'InceptionV3':
        return InceptionV3(weights='imagenet')
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def process_image(image, model_name):
    """
    Processes the image to match the model's requirements, including resizing, converting to a numpy array, and adding an extra dimension.

    Parameters:
    - image (PIL.Image): The image to be processed.
    - model_name (str): The name of the model to use for classification.

    Returns:
    - image (np.array): The processed image.
    """
    target_size = (224, 224) if model_name != 'InceptionV3' else (299, 299)
    image = image.resize(target_size)
    image = np.array(image, dtype='uint8')
    if len(image.shape) == 2:
        image = np.stack((image,) * 3, axis=-1)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    return image

def classify_images(img, model_name):
    """
    Classifies the given image using the specified model.

    Parameters:
    - img (PIL.Image): The image to be classified.
    - model_name (str): The name of the model to use for classification.

    Returns:
    - results_df (pd.DataFrame): The DataFrame containing the classification results.
    """
    img = process_image(img, model_name)
    model = select_model(model_name)
    preds = model.predict(img)
    results = decode_predictions(preds, top=5)[0]
    results_df = pd.DataFrame(results, columns=['Class ID', 'Class Name', 'Class Rating'])
    results_df['Class Rating'] = (results_df['Class Rating'] * 100).round(2)
    return results_df