import streamlit as st
from streamlit_chat import message
import requests
import pandas as pd
from mdtable import MDTable
from io import StringIO
from pathlib import Path
from PDF import PDFapp

def CSVapp():

    st.header("ChatCSV")
    st.caption("Transform the way you analyze data with our AI-powered chatbot")
    AI21_API_KEY = st.secrets["AI21_API_KEY"]

    uploaded_file = st.file_uploader('Upload a csv file', type='csv', accept_multiple_files=False)

    if uploaded_file:
        
        some_bytes = uploaded_file.getvalue()
        with open("my_file.csv", "wb") as binary_file:
            binary_file.write(some_bytes)
            base = Path.cwd()
            PATH_TO_FILE = f"{base}/my_file.csv"
            #st.write(PATH_TO_FILE)

        markdown = MDTable(PATH_TO_FILE)
        markdown_string_table = markdown.get_table()
        with st.expander("Input Table", expanded=False):
            st.write(markdown_string_table)
        markdown.save_table('out.csv')

        def get_answer(user_input):
            response = requests.post("https://api.ai21.com/studio/v1/experimental/j1-grande-instruct/complete",
            headers={"Authorization": "Bearer " + AI21_API_KEY},
            json={
            "prompt": markdown_string_table + "\nQ: " + user_input + "\nA:",
            "numResults": 1,
            "maxTokens": 10,
            "temperature": 0,
            "topKReturn": 0,
            "topP":1,
            "countPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
            },
            "frequencyPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
            },
            "presencePenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
            },
            "stopSequences":["↵↵"]
            }
        )

            return response.json()

        def get_text():
            input_text = st.text_input("You: ","What does the given table is all about?")
            return input_text 

        user_input = get_text()

        if user_input:
            res = get_answer(user_input)
            # st.write(res)
            answer = res["completions"][0]["data"]["text"]
            message(user_input, is_user=True)
            message(answer) 