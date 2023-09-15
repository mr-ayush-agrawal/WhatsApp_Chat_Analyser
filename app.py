import streamlit as st
import matplotlib.pyplot as plt
import preprocess
from pandas import DataFrame
import numpy as np
import helper

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

    stats = helper.fetch_stats(selected, Chats)

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
            chart_data, tabel_data = helper.busyUsers(Chats)
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
        wrdcld = helper.create_wordCloud(Chats, selected)
        fig, ax = plt.subplots()
        ax.imshow(wrdcld)
        st.pyplot(fig)

        # Most Common Words 
        st.title('Most Common Words')
        word_count = helper.most_common(Chats, selected)
        word_count = DataFrame(word_count.most_common(25))
        word_count.rename(columns={0:'Words', 1:'Frequency'}, inplace= True)

        fig,ax = plt.subplots()
        ax.barh(word_count['Words'],word_count['Frequency'])
        st.pyplot(fig)

        # Analysing emojis used
        emoji_df = helper.emoji_analysis(Chats, selected)
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
        timeline = helper.monthlyTimeline(Chats, selected)
        fig, ax = plt.subplots()
        ax.plot(timeline.Time, timeline.Message, c='#fb8b24')
        plt.xticks(rotation=90)
        plt.title("Message sent timeline")
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        timeline = helper.dailyTimeline(Chats, selected)
        fig,ax = plt.subplots(figsize=(12,8))
        from datetime import date
        ax.plot(timeline.Date, timeline.Message, c= 'g')
        # plt.locator_params(axis='x', nbins =10)
        xmin, xmax = ax.get_xlim()
        ax.set_xticks(np.round(np.linspace(xmin, xmax),15))
        plt.xticks(rotation = 60)
        plt.title("Daily TimeLine")
        st.pyplot(fig)

        # WeekDays, Monthly Activity Map
        weekMap, MonthMap = helper.Activity(Chats, selected)
        st.title("Weekly Activity Map")
        cols = st.columns(2)
        with cols[0] :
            st.header("Weekly Activity")
            fig, ax = plt.subplots()
            ax.barh(weekMap['WeekDay'].values,weekMap['Message'],color='#313131')
            st.pyplot(fig)
        with cols[1]:
            st.header("Monthly Activity")
            fig, ax = plt.subplots()
            ax.barh(MonthMap['Month'].values,MonthMap['Message'],color='#c9cba3')
            st.pyplot(fig)

