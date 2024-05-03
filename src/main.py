''' TODO: Update/Fix needed for MVP. 
TODO:Saving to Excel needs improving/formatting.
TODO:Add run id counter to be able to track individual run per user sessions
TODO:Local Time Stamp/Day/Session tagging vs Global Time Stamp/AllSessions tagging. Maybe use Unix timestamp
TODO:UPdate Reset Button to prompt user "Remove all Images and Output? Yes/No"
TODO:

'''

import streamlit as st
from PIL import Image
from io import BytesIO
from sidebar import display_sidebar
from image_processing import classify_images
from app_mgt import fetch_and_classify_unsplash_images, fetch_and_classify_pexels_images, fetch_alternating_images
from file_operations import save_image_to_local
from results import process_and_save_results
from instructions import instructions

def main():
    st.markdown('<style>h1{font-size: 35px;}</style>', unsafe_allow_html=True)
    st.title('Image Classification with Pre-trained Models')
    st.sidebar.markdown(instructions(), unsafe_allow_html=True)

    image_files, model_name, classify, reset, num_images, site, fetch_classify, reset_images, _, _, _, _ = display_sidebar()

    # If the user has uploaded any files
    if image_files is not None:
        for uploaded_file in image_files:
            # Open the image file
            image = Image.open(BytesIO(uploaded_file.read()))

            # Save the image to the local_images directory
            save_image_to_local(image)

            # When the Classify button is clicked
            if classify:
                # Classify the image
                classification_data = classify_images(image, model_name)  # Call the classify_images function

                # Create two columns
                col1, col2 = st.columns(2)

                # Display the uploaded image in the first column
                col1.image(image, caption='Uploaded Image.', use_column_width=True)

                # Display the classification results in the second column
                col2.markdown("###### Classification Data")  # This line adds the title
                col2.dataframe(classification_data)

                # Save the classification results to an Excel file
                process_and_save_results(image, model_name, classification_data)

    # If the Fetch & Classify button is clicked
    if fetch_classify:
        # Fetch and classify images from the selected site
        if site == 'Unsplash':
            results = fetch_and_classify_unsplash_images(num_images, model_name)
        elif site == 'Pexels':
            results = fetch_and_classify_pexels_images(num_images, model_name)
        elif site == 'Both':
            results = fetch_alternating_images(num_images, model_name)
        else:
            results = []
            
        # Display the classification results
        st.dataframe(results)

if __name__ == "__main__":
    main()