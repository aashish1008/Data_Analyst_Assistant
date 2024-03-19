import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text


def read_csv_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df


def extract_queries(uploaded_files):
    file_names = []
    features = []
    for uploaded_file in uploaded_files:
        dataframe = read_csv_file(uploaded_file)
        file_names.append(uploaded_file.name)
        features.append(dataframe.columns)
    return file_names, features


def get_prompts(uploaded_files):
    file_names, features = extract_queries(uploaded_files)
    prompts = [f"""
        Welcome to the CSV Analysis Assistant! You've provided CSV files with the following information:

        - File Names: {', '.join(file_names)}
        - Features: {', '.join(map(str, features))}

        How can I assist you with the analysis of this data? Feel free to ask questions or request specific analyses. For example:

        - "Summarize the dataset and highlight any trends or outliers."
        - "Can you provide insights into the sales performance based on the available data?"
        - "Identify correlations between different variables in the dataset."
        - "Generate visualizations for better understanding."
        - "Help me analyze social media sentiment in the context of the provided CSV files."
        - "Suggest the Machine Learning model for the provided CSV files."

        Ask anything related to data analysis, trends, or visualizations, and I'll do my best to assist you!
    """]
    return prompts


def main():
    st.set_page_config(page_title="Analysis Assistant")

    with st.sidebar:
        st.header("Gathers All details from your dataset")
        uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            st.write("filename:", uploaded_file.name)
            show_df = st.button(f"Proceed DataFrame for {uploaded_file.name}")
            if show_df:
                st.write(read_csv_file(uploaded_file))

    col1, col2 = st.columns([1, 7])

    col1.image("/images/assistant.svg", width=70)

    col2.header("Data Analyst Assistant")

    question = st.text_input("Write your prompt : ", key="input", placeholder=" Type here ....")

    submit = st.button("Ask the question")

    # if submit is clicked
    if submit:
        prompts = get_prompts(uploaded_files)
        with st.spinner("Processing..."):
            for prompt in prompts:
                response = get_gemini_response(question, prompt)
                st.write(response)


if __name__ == "__main__":
    main()
