#Importing all the necessary libraries
import streamlit as st # Web application framework
from phi.agent import Agent # AI Agent framework
from phi.model.google import Gemini # Google Gemini model
from phi.tools.duckduckgo import DuckDuckGo 
from google.generativeai import upload_file, get_file
import google.generativeai as genai
#Importing googletrans for translation feature
from deep_translator import GoogleTranslator

import time #For handling time delays during processing
from pathlib import Path

#Creating a temporary directory for file uploads
import tempfile

#Loading environment variables to get API keys
from dotenv import load_dotenv
load_dotenv()

import os

#Get the API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

#Setup the page configuration
st.set_page_config(
    page_title="Multimodal AI Agent- Video Summarizer",
    page_icon="🎥",
    layout="wide"
)
#Setting the title and header of the app
st.title("Phidata Video AI Summarizer Agent 🎥🎤🖬")
st.header("Powered by Gemini 2.0 Flash Exp")

# Initialize session state for storing the summary
if 'original_summary' not in st.session_state:
    st.session_state.original_summary = None

#Creating the agent
@st.cache_resource
def initialize_agent(): #function to initialize the agent
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],  #integrating DuckDuckGo for web search
        markdown=True,
    )

#Initializing the agent
multimodal_Agent = initialize_agent()

#Function to translate text using Google Translate 
def translate_text(text, dest_language):
    try:
        translator = GoogleTranslator(source='auto', target=dest_language)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as error:
        return f"Translation error: {str(error)}"


#File uploader for video files
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
)

if video_file:
    #Creating a temporary file to store the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    #Displays the uploaded video
    st.video(video_path, format="video/mp4", start_time=0)
    
    #Text area for user input, queries about the video
    user_query = st.text_area(
        "What insights are you seeking from the video?",
        placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
        help="Provide a specific question or topic you want the AI to focus on.",
    )

    #Button to trigger the analysis of the video
    if st.button("Analyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                #Use the agent to analyze the video and answer the user's query
                with st.spinner("Processing video and gathering insights..."):
                    #Upload and process video file
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    #Prompt generation for analysis
                    analysis_prompt = (
                        f"""
                        Analyze the uploaded video for content and context.
                        Respond to the following query using video insights and supplementary web research:
                        {user_query}

                        Provide a detailed, user-friendly, and actionable response
                        """
                    )

                    #AI agent processing to get the response
                    response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])
                
                #Store the original summary in session state
                st.session_state.original_summary = response.content
                
                #Display the analysis result
                st.subheader("Analysis Result")
                st.markdown(response.content)

            except Exception as error:
                st.error(f"An error occurred: {error}")
            finally:
                #Clean up temporary video file
                Path(video_path).unlink(missing_ok=True)
    
    #Language selection dropdown for translation
    if st.session_state.original_summary:
        st.subheader("Translate Summary")
        #Get available languages from deep_translator
        available_languages = GoogleTranslator().get_supported_languages()
        language_dict = {lang.capitalize(): lang for lang in available_languages}

        selected_language = st.selectbox(
            "Select a language for translation",
            options=list(language_dict.keys()),
            index=list(language_dict.keys()).index("English") if "English" in language_dict else 0,
            key="language_selector"
        )

    #Button to trigger the translation of the video
    if st.button("Translate Summary", key="translate_button"):
        try:
                # Translate the original summary to the selected language
                dest_language_code = language_dict[selected_language]
                translated_text = translate_text(st.session_state.original_summary, dest_language_code)

                #Displayiing the tranlated summary
                st.subheader("Translated Summary")
                st.markdown(translated_text)
        except Exception as error:
                st.error(f"An error occurred during translation: {str(error)}")
else:
    if video_file:  #Only show this message if a video was uploaded but not analyzed
        st.info("Please analyze the video to generate a summary for translation.")
    else:
        st.info("Please upload a video file to get started.")


#Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea{
        height: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

                

