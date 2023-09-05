import streamlit as st
import preprocess

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

    st.sidebar.selectbox("Analysis wrt", users)
    st.sidebar.button("Analyse")