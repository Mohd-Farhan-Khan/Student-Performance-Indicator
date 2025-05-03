import streamlit as st
import numpy as np
import pandas as pd
import logging

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Configure page
st.set_page_config(
    page_title="Student Exam Performance Predictor",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="📚"
)

# Set up logging
logging.basicConfig(level=logging.ERROR)

# Remove all custom styling to use default light theme
# No custom CSS here to ensure default Streamlit styling is used

def main():
    # Create tabs for home and prediction
    tab1, tab2 = st.tabs(["Home", "Make Prediction"])
    
    with tab1:
        st.title("Welcome to the Student Exam Performance Predictor")
        st.write("This application predicts math scores based on various student factors.")
        st.write("Click on the 'Make Prediction' tab to get started!")
        
        # Add some information about the model
        st.subheader("About this Model")
        st.write("""
        This application uses machine learning to predict student math scores based on:
        """)
        
        # Use bullet points as shown in the image
        st.markdown("""
        * Gender
        * Race/Ethnicity
        * Parental Education
        * Lunch Type
        * Test Preparation
        * Reading and Writing Scores
        """)
    
    with tab2:
        st.title("Student Exam Performance Indicator")
        st.subheader("Enter student information to predict their math score")
        
        # Create form layout with columns for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            # Fix the dropdowns by removing placeholder parameter and using index
            gender = st.selectbox(
                "Gender",
                options=["Select your Gender", "male", "female"],
                index=0
            )
            
            ethnicity = st.selectbox(
                "Race or Ethnicity",
                options=["Select Ethnicity", "group A", "group B", "group C", "group D", "group E"],
                index=0
            )
            
            parental_level_of_education = st.selectbox(
                "Parental Level of Education",
                options=["Select Parent Education", "associate's degree", "bachelor's degree", 
                         "high school", "master's degree", "some college", "some high school"],
                index=0
            )
        
        with col2:
            lunch = st.selectbox(
                "Lunch Type",
                options=["Select Lunch Type", "free/reduced", "standard"],
                index=0
            )
            
            test_preparation_course = st.selectbox(
                "Test Preparation Course",
                options=["Select Test Course", "none", "completed"],
                index=0
            )
            
            reading_score = st.number_input(
                "Reading Score out of 100",
                min_value=0,
                max_value=100
            )
            
            writing_score = st.number_input(
                "Writing Score out of 100",
                min_value=0,
                max_value=100
            )
        
        # Prediction button
        predict_button = st.button("Predict Math Score")
        
        # Display result section
        result_placeholder = st.empty()
        
        # Make prediction when button is clicked
        if predict_button:
            # Validate form inputs - check that default options aren't selected
            if (gender != "Select your Gender" and ethnicity != "Select Ethnicity" and 
                parental_level_of_education != "Select Parent Education" and 
                lunch != "Select Lunch Type" and test_preparation_course != "Select Test Course" and
                reading_score >= 0 and writing_score >= 0):
                
                try:
                    # Create CustomData object with form inputs
                    data = CustomData(
                        gender=gender,
                        race_ethnicity=ethnicity,
                        parental_level_of_education=parental_level_of_education,
                        lunch=lunch,
                        test_preparation_course=test_preparation_course,
                        reading_score=float(writing_score),  # Keeping the same field mapping as in original code
                        writing_score=float(reading_score)   # Keeping the same field mapping as in original code
                    )
                    
                    # Get data as dataframe
                    pred_df = data.get_data_as_data_frame()
                    
                    # Make prediction
                    predict_pipeline = PredictPipeline()
                    results = predict_pipeline.predict(pred_df)
                    
                    # Display result
                    result_placeholder.success(f"Predicted Math Score: {results[0]:.2f}")
                    
                except Exception as e:
                    logging.error("Error occurred: %s", e, exc_info=True)
                    result_placeholder.error("An error occurred during prediction. Please try again.")
            else:
                result_placeholder.warning("Please fill in all the fields before making a prediction.")

if __name__ == "__main__":
    main()
