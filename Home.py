import streamlit as st
from ChatPDF import PDFapp
from ChatCSV import CSVapp
from ChatYT import YTapp

st.set_page_config(
    page_title="Formats.AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "",
        'Report a bug': "",
        'About': "Chat Intelligence for your data"
    }
)

st.header("Formats.AI")
st.caption("Transform the way you analyze data with our AI-powered chatbot")

with st.sidebar:
   st.info("Created for AI21 Labs Hackathon")
   with st.expander("CSV"):
      st.info("This is just a prototye for demonstration on how AI can be used to derive data from the CSV file")
      st.info("- Please upload the CSV with proper column names and values\n- Due to token limit, please upload the file with small size")

   with st.expander("PDF"):
      st.info("Upload file of lower size")

   with st.expander("Video"):
      st.info("Paste the Youtube URL with time limit <3min [More the time, more the amount]")

tab1, tab2, tab3 = st.tabs(["Video(YT)", "PDF", "CSV"])

with tab1:
   YTapp() 

with tab2:
   PDFapp()

with tab3:
   CSVapp()
