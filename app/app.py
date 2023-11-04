import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

from analyze_conversation import *



st.set_page_config(
    page_title="Perspect Conversational Performance Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Perspect Conversational Performance Dashboard")

# uploaded_file = st.file_uploader("Choose a file")
uploaded_file = open("meeting-transcripts/all_hands.json")
if uploaded_file is not None:
    
    conversation = ConversationAnalyzer(uploaded_file)

    kpi_dict = conversation.get_conversation_kpi()

    # create three columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    
    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Number of Speakers 🧑👧",
        value=int(kpi_dict["Number of Speakers"]),
    )

    kpi2.metric(
        label="Total Conversation Time ⏳",
        value=f"{round(kpi_dict['Total Conversation Time'], 2)} seconds",
    )

    kpi3.metric(
        label = "Average Pause Between Speakers",
        value=f"{round(kpi_dict['Average Pause Between Speakers'], 2)} seconds"
    )

    kpi4.metric(
        label = "Average Sentence Length",
        value=f"{round(kpi_dict['Average Sentence Length'], 2)} seconds"
    )

    st.markdown("### Break down of speaker time")
    speaker_times = conversation.get_speaker_dist()
    fig = px.pie(pd.DataFrame(data={"speaker": list(speaker_times.keys()), 
                                    "time": list(speaker_times.values())}),
                    names="speaker",
                    values="time")
    st.plotly_chart(fig)

    # top-level filters
    job_filter = st.selectbox("Select the Speaker", list(conversation.speakers))


    # with st.sidebar:
    #     add_radio = st.radio(
    #         "Choose a shipping method",
    #         ("Standard (5-15 days)", "Express (2-5 days)")
    #     )
