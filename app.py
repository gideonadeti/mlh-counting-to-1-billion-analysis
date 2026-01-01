import streamlit as st

from csv_validator import process_csv_file

# Main Streamlit app
st.title("MLH Counting to 1 Billion Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    process_csv_file(uploaded_file)
else:
    st.info("Please upload a CSV file to get started.")
