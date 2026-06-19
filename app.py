import os

import pandas as pd
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(
    page_title="Housing AI Reporting Assistant",
    page_icon="🏠",
    layout="wide"
)


def get_api_key():
    """Return the Anthropic API key from environment variables."""
    return os.getenv("ANTHROPIC_API_KEY")


def generate_ai_summary(data_preview, stats_summary, user_question):
    """Generate a stakeholder-friendly summary using Claude."""
    api_key = get_api_key()

    if not api_key:
        raise ValueError("Anthropic API key is missing.")

    client = Anthropic(api_key=api_key)

    prompt = f"""
You are an AI reporting assistant helping a public-sector or nonprofit stakeholder understand a dataset.

Dataset preview:
{data_preview}

Basic statistics:
{stats_summary}

User question:
{user_question}

Write a clear, professional executive summary that includes:
1. Key findings
2. Possible risks or concerns
3. Recommended next steps
4. A plain-English explanation for non-technical stakeholders

Rules:
- Do not invent facts that are not supported by the data.
- Use a professional but accessible tone.
- Keep the summary concise and useful for decision-makers.
"""

    message = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def get_demo_summary():
    """Return a sample AI-style summary when live API access is unavailable."""
    return """
### Executive Summary

This sample housing dataset shows eviction-related records across multiple Los Angeles ZIP codes. The most common notice type in the sample is Nonpayment of Rent, which appears several times across different months and neighborhoods.

### Key Findings

- Nonpayment of Rent appears as a recurring issue in the dataset.
- ZIP codes 90064 and 90034 appear more than once, suggesting repeated activity in those areas.
- Rent Owed is the most frequent eviction cause in this sample.
- The dataset includes cases across January, February, and March, allowing a basic month-to-month review.

### Potential Concerns

- Rent-related eviction activity may indicate financial stress among tenants.
- Repeated activity in specific ZIP codes may require closer monitoring or targeted support.
- A small sample dataset can show patterns, but larger datasets are needed before making policy decisions.

### Recommended Next Steps

- Review larger historical eviction datasets to confirm whether these patterns continue.
- Identify ZIP codes with repeated rent-related cases.
- Share plain-language summaries with housing program staff and community stakeholders.
- Add visual charts and downloadable reports in a future version of this tool.
"""


def render_dataset_overview(df):
    """Display basic dataset information."""
    st.subheader("Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Dataset Overview")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    st.subheader("Columns")
    st.write(list(df.columns))

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    if numeric_columns:
        st.subheader("Basic Statistics")
        st.dataframe(df[numeric_columns].describe(), use_container_width=True)
        return df[numeric_columns].describe().to_string()

    st.info("No numeric columns found for statistical summary.")
    return "No numeric columns found."


def main():
    """Run the Streamlit application."""
    st.title("Housing AI Reporting Assistant")
    st.write(
        "Upload a CSV file and generate a stakeholder-friendly summary using "
        "data analysis and Claude AI."
    )

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if not uploaded_file:
        st.info("Upload a CSV file to begin.")
        return

    df = pd.read_csv(uploaded_file)
    stats_summary = render_dataset_overview(df)

    user_question = st.text_area(
        "What do you want the AI assistant to analyze?",
        "Summarize the key trends and potential concerns in this dataset."
    )

    if st.button("Generate AI Summary"):
        data_preview = df.head(10).to_string()

        try:
            with st.spinner("Generating summary with Claude..."):
                summary = generate_ai_summary(
                    data_preview,
                    stats_summary,
                    user_question
                )

            st.subheader("AI-Generated Executive Summary")
            st.markdown(summary)

        except Exception as error:
            st.warning(
                "Claude API could not generate a live response. Showing demo "
                "output instead. To enable live AI summaries, add a valid "
                "Anthropic API key with available credits."
            )

            st.subheader("Demo AI-Generated Executive Summary")
            st.markdown(get_demo_summary())

            with st.expander("Technical note"):
                st.write(str(error))


if __name__ == "__main__":
    main()