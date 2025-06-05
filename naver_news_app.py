"""Streamlit app to visualize crawled Naver News data."""

import pandas as pd
import streamlit as st


def load_data(path: str) -> pd.DataFrame:
    """Load article data from a CSV file."""
    return pd.read_csv(path)


def main() -> None:
    st.title("Naver News Articles")
    data = load_data("articles.csv")
    st.dataframe(data)
    if "content" in data.columns:
        data["content_length"] = data["content"].str.len()
        st.bar_chart(data["content_length"])


if __name__ == "__main__":
    main()
