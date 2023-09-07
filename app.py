import streamlit as st
import matplotlib.pyplot as plt
import preprocess
from helper import fetch_stats, busyUsers, create_wordCloud

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

        # Most Active users -> Only for group Chat
        if selected == 'Overall' :
            st.title('Top Chatist Users :')
            chart_data, tabel_data = busyUsers(Chats)
            # Making 2 Section -> For chart and Table
            chart_col, table_col = st.columns(2)
            with chart_col :
                fig, ax = plt.subplots()
                ax.bar(chart_data.index, chart_data.values)
                plt.xticks(rotation=60)
                st.pyplot(fig)
            with table_col :
                st.dataframe(tabel_data)

        st.title("Word Cloud :")
        wrdcld = create_wordCloud(Chats, selected)
        fig, ax = plt.subplots()
        ax.imshow(wrdcld)
        st.pyplot(fig)
