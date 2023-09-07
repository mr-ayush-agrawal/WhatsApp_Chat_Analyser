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
        heads = ["Total Messages","Total Words Typed",'Media Files Shared','Links Shared']
        cols = st.columns(len(heads))
        for i in range(len(heads)) :
            with cols[i] :
                st.header(heads[i])
                st.title(stats[i])