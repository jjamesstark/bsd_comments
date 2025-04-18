from datetime import datetime, date
import json
from collections import Counter

import pandas as pd
import streamlit as st


# Page Config

st.set_page_config(
    page_title="BSD Submitted Written Comments",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

commentsdf = pd.read_json("comments.json")


def flatten_listolist(listolist):
    return [x for xs in listolist for x in xs]

topics = set(flatten_listolist(commentsdf['topics']))
associations_with_bsd = set(commentsdf['association_with_bsd'])
exploded_by_topics_df = commentsdf.explode('topics')
topics_occurances = exploded_by_topics_df.groupby('topics')['topics'].value_counts().sort_values(ascending=False)


with st.sidebar:
    topics = []

    for topic in topics_occurances.items():
        topics.append(topic[0])

    selected_topics = st.multiselect(
        "Topics", topics
    )

    selected_assoc = st.multiselect(
        "Association with SD", associations_with_bsd, [None, 'Other Community Member', 'Student', 'Staff Member', 'Parent/Guardian']
    )

    

selected_by_topics_ids = exploded_by_topics_df[exploded_by_topics_df['topics'].isin(selected_topics)]
    

selected_commentsdf  = commentsdf[commentsdf['association_with_bsd'].isin(selected_assoc)]

selected_commentsdf = selected_commentsdf[selected_commentsdf['id'].isin(list(set(selected_by_topics_ids['id'].values)))]

selected_comments_dict = selected_commentsdf.to_dict('records')

st.title("Selected Comments")
for comment in selected_comments_dict:

    date_string = comment['date'].strftime("%B %d, %Y")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{comment['first_name']}: {comment['association_with_bsd']}")
        for topic in comment['topics']:
            st.badge(f"{topic}")

    with col2:
        st.text(f"{comment['comment']}")
        st.caption(date_string)
    
    st.divider()


