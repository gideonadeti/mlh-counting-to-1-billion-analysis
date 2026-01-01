import streamlit as st
import pandas as pd
import arrow


def calculate_metrics(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Calculate key metrics from the counting data.

    Args:
        df: The validated dataframe
        column_mapping: Dictionary mapping expected column names to actual column names

    Returns:
        dict: Dictionary containing calculated metrics
    """
    # Get column names
    date_col = column_mapping["date"]
    to_col = column_mapping["to"]
    count_col = column_mapping["count"]

    # Convert to numeric (should already be numeric, but ensure)
    to_values = pd.to_numeric(df[to_col])
    count_values = pd.to_numeric(df[count_col])

    # Calculate metrics
    current_standing = to_values.max()  # Highest number reached
    completion_percentage = (
        current_standing / 1_000_000_000
    ) * 100  # Percentage toward 1 billion

    daily_throughput = count_values.mean()  # Average numbers per day
    peak_performance = count_values.max()  # Maximum count in a single day

    # Find the date of peak performance
    peak_performance_idx = count_values.idxmax()
    peak_performance_date = pd.to_datetime(df.loc[peak_performance_idx, date_col])

    # Calculate estimated completion time in years
    # Calculate remaining numbers to count
    remaining = 1_000_000_000 - current_standing

    # Calculate years remaining (based on average daily throughput)
    if daily_throughput > 0:
        days_remaining = remaining / daily_throughput
        years_remaining = days_remaining / 365.25  # Account for leap years
        estimated_completion_years = years_remaining
    else:
        estimated_completion_years = None  # Can't estimate if no throughput

    return {
        "current_standing": current_standing,
        "completion_percentage": completion_percentage,
        "daily_throughput": daily_throughput,
        "peak_performance": peak_performance,
        "peak_performance_date": peak_performance_date,
        "estimated_completion_years": estimated_completion_years,
    }


def display_metrics(metrics: dict[str, float]):
    """
    Display the calculated metrics in the Streamlit app.

    Args:
        metrics: Dictionary containing the calculated metrics
    """
    st.subheader("Metrics")

    # Create columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Current Standing",
            value=f"{metrics['current_standing']:,.0f}",
            help="The highest number reached so far",
        )

        st.metric(
            label="Daily Throughput",
            value=f"{metrics['daily_throughput']:,.2f}",
            help="Average numbers counted per day",
        )

    with col2:
        st.metric(
            label="Completion Percentage",
            value=f"{metrics['completion_percentage']:.6f}%",
            help="Progress toward 1 billion",
        )

        # Format date in human-friendly format using arrow (similar to date-fns)
        peak_date = arrow.get(metrics["peak_performance_date"])
        peak_date_str = peak_date.format("MMMM D, YYYY")  # e.g., "January 15, 2024"

        st.metric(
            label=f"Peak Performance ({peak_date_str})",
            value=f"{metrics['peak_performance']:,.0f}",
            help="Maximum numbers counted in a single day",
        )

    # Estimated Completion Time
    st.divider()

    if metrics.get("estimated_completion_years") is not None:
        years = metrics["estimated_completion_years"]

        if years >= 1000:
            # For very large values, show in thousands of years
            years_str = f"~{years / 1000:.1f} thousand years"
        elif years >= 100:
            # For large values, show with one decimal
            years_str = f"~{years:.1f} years"
        else:
            # For smaller values, show with one decimal
            years_str = f"~{years:.1f} years"

        st.metric(
            label="Estimated Completion Time",
            value=years_str,
            help="Projected time to reach 1 billion based on average daily throughput",
        )
    else:
        st.metric(
            label="Estimated Completion Time",
            value="N/A",
            help="Cannot estimate: no daily throughput data",
        )

    st.divider()
