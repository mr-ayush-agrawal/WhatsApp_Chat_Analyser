import streamlit as st
import matplotlib.pyplot as plt
import preprocess
from pandas import DataFrame
from helper import fetch_stats, busyUsers, create_wordCloud,most_common,emoji_analysis, monthlyTimeline

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

        # Most Common Words 
        st.title('Most Common Words')
        word_count = most_common(Chats, selected)
        word_count = DataFrame(word_count.most_common(25))
        word_count.rename(columns={0:'Words', 1:'Frequency'}, inplace= True)

        fig,ax = plt.subplots()
        ax.barh(word_count['Words'],word_count['Frequency'])
        st.pyplot(fig)

        # Analysing emojis used
        emoji_df = emoji_analysis(Chats, selected)
        st.title("Emojis Used :")
        cols = st.columns(2)
        with cols[1] :
            st.dataframe(emoji_df.rename(columns={0:'Emojis',1:'Count'}))
        with cols[0] :
            fig, ax = plt.subplots()
            ct = emoji_df.head(10)
            ct.iloc[9,0]='Other'
            ct.iloc[9,1]=sum(emoji_df[1][9:])
            ax.pie(ct[1],labels=ct[0],autopct="%0.2f",textprops={'fontsize': 7})
            st.pyplot(fig)

        # Alaysing the time
        st.title("Monthly Timeline")
        timeline = monthlyTimeline(Chats, selected)
        fig, ax = plt.subplots()
        ax.plot(timeline.Time, timeline.Message, c='#fb8b24')
        plt.xticks(rotation=90)
        plt.title("Message sent timeline")
        st.pyplot(fig)