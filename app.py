import streamlit as st
import pandas as pd

st.title("MLH Counting to 1 Billion Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Show a preview of the data
    st.subheader("Data Preview")
    st.dataframe(df.head())
else:
    st.info("Please upload a CSV file to get started.")
