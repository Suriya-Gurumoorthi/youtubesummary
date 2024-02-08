import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt1="""Act as you are the youtube query responder. 
You will be given with the transcript below along with the query in the last line. 
Your job is to analyse the transcript and return back the answer for the query. 
Your transcript as follows: """

prompt2="""Act as you are the youtube summarizer.
You will be given with the transcript below. Your task is to summarize 
the transcript and return back the summary precisely pointwise by not missing any important terms.
try to bold the keywords you found in the video. Your transcript is as follows:
"""

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


def query_generate(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt1+transcript_text+"\n Query: "+question)
    return response.text

def summary_generate(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt2+transcript_text)
    return response.text

st.title("Youtube Learner")
youtube_link = st.text_input("Paste link to video")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    
question = st.text_input("Enter your query. If not go for Summary ",key="query")

    
if st.button("Query"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        ans=query_generate(transcript_text,prompt1)
        st.markdown("# Answer")
        st.write(ans)


if st.button("Summarize"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        ans=summary_generate(transcript_text,prompt2)
        st.markdown("# Answer")
        st.write(ans)




