import os
import pandas as pd
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="Housing AI Reporting Assistant", layout="wide")

st.title("Housing AI Reporting Assistant")
st.write(
    "Upload a CSV file and generate a stakeholder-friendly summary using data analysis and Claude AI."
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

def generate_ai_summary(data_preview, stats_summary, user_question):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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

Do not invent facts that are not supported by the data.
"""

    message = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Overview")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")

    st.subheader("Columns")
    st.write(list(df.columns))

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    if numeric_columns:
        st.subheader("Basic Statistics")
        st.dataframe(df[numeric_columns].describe())
        stats_summary = df[numeric_columns].describe().to_string()
    else:
        stats_summary = "No numeric columns found."

    user_question = st.text_area(
        "What do you want the AI assistant to analyze?",
        "Summarize the key trends and potential concerns in this dataset."
    )

    if st.button("Generate AI Summary"):
        data_preview = df.head(10).to_string()

    try:
        with st.spinner("Generating summary with Claude..."):
            summary = generate_ai_summary(data_preview, stats_summary, user_question)

        st.subheader("AI-Generated Executive Summary")
        st.write(summary)

    except Exception as e:
        st.warning(
            "Claude API could not generate a live response. Showing demo output instead. "
            "To enable live AI summaries, add a valid Anthropic API key with available credits."
        )

        demo_summary = """
### Executive Summary

This sample housing dataset shows eviction-related records across multiple Los Angeles ZIP codes. 
The most common notice type in the sample is Nonpayment of Rent, which appears several times across different months and neighborhoods.

### Key Findings

- Nonpayment of Rent appears as a recurring issue in the dataset.
- ZIP codes 90064 and 90034 appear more than once, suggesting repeated activity in those areas.
- Rent Owed is the most frequent eviction cause in this sample.
- The dataset includes cases across January, February, and March, allowing basic month-to-month review.

### Potential Concerns

- Rent-related eviction activity may indicate financial stress among tenants.
- Repeated activity in specific ZIP codes may require closer monitoring or targeted support.
- A small dataset can show patterns, but larger datasets are needed before making policy decisions.

### Recommended Next Steps

- Review larger historical eviction datasets to confirm whether these patterns continue.
- Identify ZIP codes with repeated rent-related cases.
- Share plain-language summaries with housing program staff and community stakeholders.
- Add visual charts and downloadable reports in a future version of this tool.
"""
        st.subheader("Demo AI-Generated Executive Summary")
        st.markdown(demo_summary)

        with st.expander("Technical note"):
            st.write(str(e))
else:
    st.info("Upload a CSV file to begin.")