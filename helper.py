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

    num_messages = df.shape[0]
    num_words = wrdCt(df)
    num_media = len(df[df.Message == '<Media omitted>\n'])
    num_links = linkCt(df)

    return (num_messages, num_words,num_media,num_links)

def busyUsers(Chat, count_size=7):
    BusyUsers  = Chat.Sender.value_counts().head(count_size)
    ChatTable = round((Chat.Sender.value_counts()/Chat.shape[0])*100,2).reset_index().rename(columns = {'count':"Percent"})
    return BusyUsers, ChatTable
