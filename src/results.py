import os
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter
from image_processing import classify_images
from PIL import Image
from io import BytesIO
import uuid

from file_operations import create_directory, output_dir
import streamlit as st

def save_results_to_excel(df_new, image_file_name=None):
    try:
        # Ensure the output directory exists
        create_directory(output_dir)

        excel_file = os.path.join(output_dir, 'Classification_Results.xlsx')
        print(f"Image file name: {image_file_name}")
        print(f"df_new columns: {df_new.columns}")
        print(f"df_new shape: {df_new.shape}")

        df_new.loc[df_new.shape[0]-1, 'Filename'] = image_file_name # Add the image file name

        if os.path.exists(excel_file):
            df_old = pd.read_excel(excel_file)
            # Remove any rows in df_new that already exist in df_old
            df_new = df_new[~df_new.isin(df_old)].dropna()
            df = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df = df_new

        # Insert an empty row after each row of data
        df = pd.concat([df, pd.DataFrame([pd.Series()], columns=df.columns)], ignore_index=True)

        # Save the DataFrame to the Excel file
        df.to_excel(excel_file, index=False)

    except Exception as e:
        print(f"Error saving results to Excel: {e}")

        # Auto update the column width to fit better for visibility
        book = openpyxl.load_workbook(excel_file)
        sheet = book.active

        for column in sheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[get_column_letter(column[0].column)].width = adjusted_width

        book.save(excel_file)
    except Exception as e:
        print(f"An error occurred while saving results to Excel file: {e}")

def process_and_save_results(image, model_name, classification_data):
    # Classify the image
    results = classify_images(image, model_name)

    # Save the classification results to an Excel file in the output directory
    if results.empty:
        print(f"No results to save for {image}") # Debug print statement
    else:
        try:
            print(f"Saving results for {image} to Excel file") # Debug print statement
            # Get the image file name from the image file path
            image_file_name = str(uuid.uuid4())
            ###image_file_name = image.name

            save_results_to_excel(results, image_file_name)
        except PermissionError:
            message = "Classification_Results.xlsx is currently opened by the user. Please, close it for the program to write out the classification results."
            print(message)
            st.error(message)