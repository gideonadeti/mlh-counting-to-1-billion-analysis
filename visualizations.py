import streamlit as st
import pandas as pd
import altair as alt


def create_progress_chart(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Create a line chart showing cumulative progress over time.

    Args:
        df: The validated dataframe
        column_mapping: Dictionary mapping expected column names to actual column names

    Returns:
        altair.Chart: The progress chart
    """
    # Get column names
    date_col = column_mapping["date"]
    to_col = column_mapping["to"]

    # Create a copy for charting
    chart_df = df.copy()

    # Convert date to datetime and to to numeric
    chart_df["date_parsed"] = pd.to_datetime(chart_df[date_col])
    chart_df["count_value"] = pd.to_numeric(chart_df[to_col])

    # Sort by date to ensure proper line connection
    chart_df = chart_df.sort_values("date_parsed")

    # Create the chart
    chart = (
        alt.Chart(chart_df)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "date_parsed:T",
                title="Date",
                axis=alt.Axis(format="%Y-%m-%d", labelAngle=-45),
            ),
            y=alt.Y(
                "count_value:Q",
                title="Count",
                axis=alt.Axis(format=",d"),  # Format with commas for thousands
            ),
            tooltip=[
                alt.Tooltip("date_parsed:T", title="Date", format="%B %d, %Y"),
                alt.Tooltip("count_value:Q", title="Count", format=",d"),
            ],
        )
        .configure_axis(
            grid=True,
        )
        .configure_title(
            fontSize=16,
            fontWeight="bold",
        )
    )

    return chart


def display_progress_chart(df: pd.DataFrame, column_mapping: dict[str, str]):
    """
    Display the progress over time chart in Streamlit.

    Args:
        df: The validated dataframe
        column_mapping: Dictionary mapping expected column names to actual column names
    """
    st.subheader("Progress Over Time")
    chart = create_progress_chart(df, column_mapping)
    st.altair_chart(chart, use_container_width=True)
