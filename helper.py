def wrdCt(chats):
    wrds = []
    for msg in chats.Message :
        wrds.extend(msg.split())
    return len(wrds)

def linkCt(chats):
    from urlextract import URLExtract
    extractor = URLExtract()
    link = []
    for msg in chats.Message:
        link.extend(extractor.find_urls(msg))
    return len(link)

def fetch_stats(user, chats):
    # 1. Number of message
    # 2. Total Words typed 
    # 3. Media omited
    if user!= 'Overall':
        df = chats[chats['Sender']==user]
    else :
        df = chats.copy()

    # df is the dataframe to be analysed

    num_media = len(df[df.Message == '<media omitted>\n'])
    # Removing the Media from the data
    df.drop(df[df.Message == '<media omitted>\n'].index, inplace= True)

    num_messages = df.shape[0]
    num_words = wrdCt(df)
    num_links = linkCt(df)

    return (num_messages, num_words,num_media,num_links)

def busyUsers(Chat, count_size=7):
    Chat.drop(Chat[Chat['Sender']=='Notification'].index, inplace = True)
    BusyUsers  = Chat.Sender.value_counts().head(count_size)
    ChatTable = round((Chat.Sender.value_counts()/Chat.shape[0])*100,2).reset_index().rename(columns = {'count':"Percent of Message"})
    return BusyUsers, ChatTable

def create_wordCloud(chats, user):
    from wordcloud import WordCloud
    if user != 'Overall':
        chats = chats[chats['Sender']==user]
    
    # Removing all media the 
    chats.drop(chats[chats.Message == '<media omitted>\n'].index, inplace= True)

    wc = WordCloud(height=360, width=550, min_font_size=12, background_color='white')
    wrdlcd = wc.generate(chats['Message'].str.cat(sep=' '))
    return wrdlcd