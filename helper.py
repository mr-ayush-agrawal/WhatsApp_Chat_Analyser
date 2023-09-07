def wrdCt(chats):
    wrds = []
    for msg in chats.Message :
        wrds.extend(msg.split())
    return len(wrds)

def fetch_stats(user, chats):
    # 1. Number of message
    # 2. Total Words typed 
    if user!= 'Overall':
        df = chats[chats['Sender']==user]
    else :
        df = chats.copy()

    # df is the dataframe to be analysed

    num_messages = df.shape[0]
    num_words = wrdCt(df)

    return (num_messages, num_words)