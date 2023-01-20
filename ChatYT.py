from deepgram import Deepgram
import json
import youtube_dl
import streamlit as st
from languages import languages
from itranslate import itranslate as itrans
from pathlib import Path
from fpdf import FPDF
import base64
from streamlit_chat import message
import requests

def YTapp():

    st.header("CogniTube")
    st.caption("Cognitive + YouTube")
        
    DEEPGRAM_API_KEY =  st.secrets["DEEPGRAM_API_KEY"]
    AI21_API_KEY = st.secrets["AI21_API_KEY"]

    PATH_TO_FILE = ''
    

    def get_questions(transcript):
        
        questions_response = requests.post("https://api.ai21.com/studio/v1/experimental/j1-grande-instruct/complete",
            headers={"Authorization": "Bearer " + AI21_API_KEY},
            json={
                "prompt": "Create a list of questions from the given context\nContext: " + transcript + "\nQuestions:",
                "numResults": 1,
                "maxTokens": 200,
                "temperature": 0.7,
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
            "stopSequences":[]
            }
        )
        return questions_response.json()

    def get_summary(transcript):

        summary_response = requests.post("https://api.ai21.com/studio/v1/experimental/summarize",
            headers={"Authorization": "Bearer "+ AI21_API_KEY},
            json={
                "text": transcript,
            }
        )
        return summary_response.json()

    def get_answer(transcript, user_input):
        response = requests.post("https://api.ai21.com/studio/v1/experimental/j1-grande-instruct/complete",
        headers={"Authorization": "Bearer " + AI21_API_KEY },
        json={
        "prompt": transcript + "\nQ: " + user_input + "\nA:",
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


    @st.cache
    def download_video(link):

        videoinfo = youtube_dl.YoutubeDL().extract_info(url = link, download=False)
        filename = f"{videoinfo['id']}.mp3"

        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([videoinfo['webpage_url']])

        base = Path.cwd()
        PATH_TO_FILE = f"{base}/{filename}"

        return PATH_TO_FILE

    @st.cache
    def transcribe(PATH_TO_FILE):
        # Initializes the Deepgram SDK
        deepgram = Deepgram(DEEPGRAM_API_KEY)
        # Open the audio file
        with open(PATH_TO_FILE, 'rb') as audio:
            # ...or replace mimetype as appropriate
            source = {'buffer': audio, 'mimetype': 'audio/wav'}
            response = deepgram.transcription.sync_prerecorded(source, {'summarize': True, 'punctuate': True, "diarize": True, "utterances": True, "detect_topics": True, "numerals": True})
            # response_result = json.dumps(response, indent=4)
        
        return response

    @st.cache
    def translate(text, to_lang):
        return itrans(text, to_lang = to_lang)

    link = st.text_input("Enter the YT URL", value="https://youtu.be/JYs_94znYy0")
    st.video(link)

    PATH_TO_FILE = download_video(link)
    response = transcribe(PATH_TO_FILE)

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Chat", "Translate", "Questions"])
    
    with tab1:

        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        summary_response = get_summary(transcript)
        summary = summary_response["summaries"][0]["text"]

        with st.expander("TL;DW"):
            st.write(summary, expanded=True)

        with st.expander("Transcript", expanded=False):
            st.write(transcript)

    with tab2:

        user_input = st.text_input("You: ","What does the context conveys?")

        if user_input:
            res = get_answer(transcript, user_input)
            # st.write(res)
            answer = res["completions"][0]["data"]["text"]
            message(user_input, is_user=True)
            message(answer) 

    with tab3:
        to_lang = st.selectbox("Select the language", languages.values())
        dest = list(languages.keys())[list(languages.values()).index(to_lang)]
        st.write("language: ", dest)
        st.write(translate(transcript, dest)) 

    with tab4:
        questions_response = get_questions(transcript)
        # st.write(questions_response)
        st.markdown(questions_response["completions"][0]["data"]["text"])