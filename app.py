import streamlit as st
import preprocess
from helper import fetch_stats

st.sidebar.title("WhatsApp Chat analyser")
ChatFile = st.sidebar.file_uploader("Select a chat", type='txt')
if ChatFile is not None:
    # The file would be in bytes stream we need to read it and convert it to string
    byte_data = ChatFile.getvalue()
    Chats = byte_data.decode('utf-8')
    # This is a kind of reading the file
    Chats = preprocess.PreProcess(Chats)
    st.dataframe(Chats)

    # Users List
    users = Chats['Sender'].unique().tolist()
    users.remove("Notification")
    users.sort()
    users.insert(0,"Overall")

    selected = st.sidebar.selectbox("Analysis wrt", users)

    stats = fetch_stats(selected, Chats)

    if st.sidebar.button("Analyse") :
        cols = st.columns(5)
        with cols[0] :
            st.header("Total Messages")
            st.title(stats[0])
        with cols[1] :
            st.header("Total Words Typed")
            st.title(stats[1])
        