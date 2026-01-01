import streamlit as st

from csv_validator import process_csv_file
from metrics import calculate_metrics, display_metrics
from visualizations import display_progress_chart, display_daily_activity_chart

# Main Streamlit app
st.title("MLH Counting to 1 Billion Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    result = process_csv_file(uploaded_file)

    if result is not None:
        df, column_mapping = result

        # Display data preview
        st.subheader("Data Preview")
        st.dataframe(df)

        # Calculate and display metrics
        metrics = calculate_metrics(df, column_mapping)

        display_metrics(metrics)

        # Display progress chart
        display_progress_chart(df, column_mapping)

        # Display daily activity chart
        display_daily_activity_chart(df, column_mapping)
else:
    st.info("Please upload a CSV file to get started.")
