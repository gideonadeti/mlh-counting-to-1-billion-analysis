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

    # Validate numeric columns: from, to, and count
    numeric_columns = ["from", "to", "count"]

    for expected_name in numeric_columns:
        actual_col = column_mapping[expected_name]

        if not pd.api.types.is_numeric_dtype(df[actual_col]):
            try:
                pd.to_numeric(df[actual_col], errors="raise")
            except (ValueError, TypeError):
                validation_errors.append(
                    f"Column '{actual_col}' (expected '{expected_name}') must contain numeric values"
                )

    return validation_errors


def validate_date_duplicates(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Validate that there are no duplicate dates in the dataframe.

    Returns:
        list: List of validation error messages (empty if no duplicates found)
    """
    validation_errors = []
    date_col = column_mapping["date"]

    # Convert to datetime for comparison
    df_dates = pd.to_datetime(df[date_col])

    # Check for duplicate dates
    duplicates = df_dates[df_dates.duplicated()]

    if not duplicates.empty:
        duplicate_dates = pd.Series(duplicates.unique())
        duplicate_dates_str = duplicate_dates.dt.strftime("%Y-%m-%d").tolist()

        validation_errors.append(
            f"Found duplicate dates: {', '.join(duplicate_dates_str)}"
        )

    return validation_errors


def validate_date_ordering(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Validate that dates are in chronological order (ascending).

    Returns:
        list: List of validation error messages (empty if dates are in order)
    """
    validation_errors = []
    date_col = column_mapping["date"]

    # Convert to datetime for comparison
    df_dates = pd.to_datetime(df[date_col])

    # Check if dates are in chronological order (ascending)
    if not df_dates.is_monotonic_increasing:
        validation_errors.append("Dates are not in chronological order (ascending)")

    return validation_errors


def validate_numeric_rules(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Validate business logic rules for numeric columns:
    1. to >= from (ending number should be >= starting number)
    2. count = to - from + 1 (count should match calculated value)

    Returns:
        list: List of validation error messages (empty if all rules pass)
    """
    validation_errors = []

    # Get column names
    from_col = column_mapping["from"]
    to_col = column_mapping["to"]
    count_col = column_mapping["count"]

    # Convert to numeric (should already be validated, but ensure numeric types)
    from_values = pd.to_numeric(df[from_col], errors="coerce")
    to_values = pd.to_numeric(df[to_col], errors="coerce")
    count_values = pd.to_numeric(df[count_col], errors="coerce")

    # Check for any NaN values (shouldn't happen if data types validated, but check anyway)
    if from_values.isna().any() or to_values.isna().any() or count_values.isna().any():
        validation_errors.append(
            "Found invalid numeric values (NaN) in from, to, or count columns"
        )

        return validation_errors

    # Rule 1: to >= from
    invalid_ranges = df[to_values < from_values]

    if not invalid_ranges.empty:
        date_col = column_mapping["date"]
        invalid_dates = (
            pd.to_datetime(invalid_ranges[date_col]).dt.strftime("%Y-%m-%d").tolist()
        )

        validation_errors.append(
            f"Found rows where 'to' < 'from': {', '.join(invalid_dates)}"
        )

    # Rule 2: count = to - from + 1
    calculated_count = to_values - from_values + 1
    mismatched = df[count_values != calculated_count]

    if not mismatched.empty:
        date_col = column_mapping["date"]
        mismatched_dates = (
            pd.to_datetime(mismatched[date_col]).dt.strftime("%Y-%m-%d").tolist()
        )

        validation_errors.append(
            f"Found rows where 'count' ≠ 'to - from + 1': {', '.join(mismatched_dates)}"
        )

    return validation_errors


def display_data(df: pd.DataFrame):
    """Display the CSV headers and a preview of the data."""

    st.subheader("Data Preview")
    st.dataframe(df.head())


@st.cache_data
def read_csv_file(file):
    """
    Read and cache the CSV file to avoid re-reading on reruns.

    Args:
        file: The uploaded file object from Streamlit

    Returns:
        pd.DataFrame: The loaded dataframe
    """

    return pd.read_csv(file)


def process_csv_file(file):
    """
    Process and validate the uploaded CSV file.

    Args:
        file: The uploaded file object from Streamlit
    """
    try:
        # Read the CSV file
        df = read_csv_file(file)

        # Expected required columns
        required_columns = ["date", "from", "to", "count"]

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

        # Validate date duplicates
        duplicate_errors = validate_date_duplicates(df, column_mapping)

        if duplicate_errors:
            for error in duplicate_errors:
                st.error(f"{error}")
            st.stop()

        # Validate date ordering
        ordering_errors = validate_date_ordering(df, column_mapping)

        if ordering_errors:
            for error in ordering_errors:
                st.error(f"{error}")
            st.stop()

        # Validate numeric business logic rules
        numeric_rules_errors = validate_numeric_rules(df, column_mapping)

        if numeric_rules_errors:
            for error in numeric_rules_errors:
                st.error(f"{error}")
            st.stop()

        # Display the data
        display_data(df)

    except pd.errors.EmptyDataError:
        st.error("The CSV file is empty")
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {str(e)}")
    except (OSError, ValueError, TypeError) as e:
        st.error(f"Unexpected error: {str(e)}")
