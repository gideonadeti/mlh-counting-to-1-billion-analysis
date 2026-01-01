import streamlit as st
import pandas as pd


def validate_columns(df: pd.DataFrame, required_columns: list[str]):
    """
    Validate that all required columns exist in the dataframe (case-insensitive).

    Returns:
        tuple: (column_mapping, missing_columns)
    """
    # Create a lookup dictionary: lowercase column name -> actual column name
    column_lookup = {col.strip().lower(): col for col in df.columns}
    missing_columns = []
    column_mapping = {}

    for req_col in required_columns:
        req_col_lower = req_col.lower()

        if req_col_lower in column_lookup:
            column_mapping[req_col] = column_lookup[req_col_lower]
        else:
            missing_columns.append(req_col)

    return column_mapping, missing_columns


def validate_data_types(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Validate that the data types are correct for the required columns.

    Returns:
        list: List of validation error messages (empty if all validations pass)
    """
    validation_errors = []

    # Validate date column
    date_col = column_mapping["date"]

    try:
        pd.to_datetime(df[date_col])
    except (ValueError, TypeError):
        validation_errors.append(f"Date column '{date_col}' contains invalid dates")

    # Validate count column (numeric)
    count_col = column_mapping["count"]

    if not pd.api.types.is_numeric_dtype(df[count_col]):
        try:
            pd.to_numeric(df[count_col], errors="raise")
        except (ValueError, TypeError):
            validation_errors.append(
                f"Column '{count_col}' (expected 'count') must contain numeric values"
            )

    return validation_errors


def display_data(df: pd.DataFrame) -> None:
    """Display the CSV headers and a preview of the data."""

    st.subheader("Data Preview")
    st.dataframe(df.head())


def process_csv_file(file):
    """
    Process and validate the uploaded CSV file.

    Args:
        file: The uploaded file object from Streamlit
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file)

        # Expected required columns
        required_columns = ["date", "count"]

        # Validate columns
        column_mapping, missing_columns = validate_columns(df, required_columns)

        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            st.info(f"Found columns: {', '.join(df.columns.tolist())}")
            st.stop()

        # Validate data types
        validation_errors = validate_data_types(df, column_mapping)

        if validation_errors:
            for error in validation_errors:
                st.error(f"{error}")
            st.stop()

        # All validations passed
        st.success("CSV file is valid!")

        # Display the data
        display_data(df)

    except pd.errors.EmptyDataError:
        st.error("The CSV file is empty")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {str(e)}")
    except (OSError, ValueError, TypeError) as e:
        st.error(f"Unexpected error: {str(e)}")
