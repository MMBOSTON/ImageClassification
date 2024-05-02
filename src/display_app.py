import pandas as pd
import streamlit as st
from PIL import Image


def display_app(image_path, results):
    # Display the image
    st.image(image_path, use_column_width=True)
    
    # Display the classification results
    st.markdown("### Classification Results")
    
    # Convert results to a DataFrame for display
    df = pd.DataFrame(results, columns=['Class ID', 'Class Name', 'Class Rating'])
    
    # Round the 'Class Rating' column to 3 decimal points
    df['Class Rating'] = df['Class Rating'].round(3)
    
    # Display the DataFrame
    st.table(df)
    
def display_progress_bar(num_steps, current_step):
    """Display a progress bar in the Streamlit app."""

    # Create a progress bar
    progress_bar = st.progress(0)

    # Update the progress bar
    progress_bar.progress(current_step / num_steps)

    # Return the progress bar so it can be updated outside the function
    return progress_bar