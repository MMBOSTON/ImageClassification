import numpy as np
import pandas as pd
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from tensorflow.keras.applications import VGG16, InceptionV3
from tensorflow.keras.preprocessing import image as image_utils
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def select_model(model_name):
    if model_name == 'ResNet50':
        return ResNet50(weights='imagenet')
    elif model_name == 'VGG16':
        return VGG16(weights='imagenet')
    elif model_name == 'InceptionV3':
        return InceptionV3(weights='imagenet')
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def process_image(image, model_name):
    # Resize the image to the format the model requires
    target_size = (224, 224) if model_name != 'InceptionV3' else (299, 299)
    image = image.resize(target_size)
    
    # Convert the image to a numpy array with a dtype of 'uint8'
    image = np.array(image, dtype='uint8')

    # If the image is grayscale, replicate it into 3 color channels
    if len(image.shape) == 2:
        image = np.stack((image,) * 3, axis=-1)
    
    # Add an extra dimension to the image
    image = np.expand_dims(image, axis=0)
    
    # Preprocess the image
    image = preprocess_input(image)
    
    return image

def classify_images(img, model_name):
    # Preprocess the image
    img = process_image(img, model_name)

    # Load the appropriate model
    model = select_model(model_name)
    
    # Use the model to classify the image
    preds = model.predict(img)

    # Decode the predictions
    results = decode_predictions(preds, top=5)[0] # Get the top 5 predictions

    # Convert the results to a DataFrame
    results_df = pd.DataFrame(results, columns=['Class ID', 'Class Name', 'Class Rating'])

    # Convert 'Class Rating' to percentage and round to 2 decimal points
    results_df['Class Rating'] = (results_df['Class Rating'] * 100).round(2)

    return results_df