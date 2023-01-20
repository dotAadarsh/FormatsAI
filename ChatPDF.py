import streamlit as st
from streamlit_chat import message
import docx2txt
import pdfplumber
import os 
import json
import requests

def PDFapp():
    st.title('Summarizer')
    st.subheader("Simplifying information, maximizing understanding - AI powered summarization")

    st.markdown("[Demo PDF file](https://github.com/dotAadarsh/FormatsAI/blob/main/assets/Blockchain.pdf)")

    AI21_API_KEY = st.secrets["AI21_API_KEY"]

    def get_answer(context, question):
        response = requests.post("https://api.ai21.com/studio/v1/experimental/j1-grande-instruct/complete",
        headers={"Authorization": "Bearer " + AI21_API_KEY},
        json={
            "prompt": context + "\nQ: " + question + "\nA:",
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

        input_text = st.text_input("You: ","Explain the context")
        return input_text 

    def bot_message(question, answer):
        message(question, is_user=True)
        message(answer) 

    def app():
        
        Option = st.selectbox("Choose the format", ('Text Input', 'Upload PDF'))

        if Option == 'Text Input':
            context = st.text_area('Text to summarize', '''Blockchain defined: Blockchain is a shared, immutable ledger that facilitates the process of recording transactions and tracking assets in a business network. An asset can be tangible (a house, car, cash, land) or intangible (intellectual property, patents, copyrights, branding). Virtually anything of value can be tracked and traded on a blockchain network, reducing risk and cutting costs for all involved.''')
            if context is not None:
                question = get_text()
                answer_response = get_answer(context, question)
                answer = answer_response["completions"][0]["data"]["text"]
                bot_message(question, answer)

        elif Option == 'Upload PDF':
            docx_file = st.file_uploader("Choose a file")

            if docx_file is not None:
                
                file_details = {"filename":docx_file.name, "filetype":docx_file.type,
                                "filesize":docx_file.size}
                
                with st.sidebar.expander("File Info"):
                    st.json(file_details)

                if docx_file.type == "text/plain":
                    # Read as string (decode bytes to string)
                    raw_text = str(docx_file.read(),"utf-8")
                    st.text_area("Extracted Text", raw_text)

                elif docx_file.type == "application/pdf":

                    try:
                        with pdfplumber.open(docx_file) as pdf:
                            pages = pdf.pages[0]
                            context = pages.extract_text()
                            st.text_area("Extracted Text", context)
                            if context is not None:
                                question = get_text()
                                answer_response = get_answer(context, question)
                                answer = answer_response["completions"][0]["data"]["text"]
                                bot_message(question, answer)

                    except:
                        st.write("None")

                else:   
                    raw_text = docx2txt.process(docx_file)
                    st.text_area("Extracted Text", raw_text)

    app()



