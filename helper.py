def wrdCt(chats):
    wrds = []
    for msg in chats.Message :
        wrds.extend(msg.split())
    return len(wrds)

def fetch_stats(user, chats):
    # 1. Number of message
    # 2. Total Words typed 
    # 
    if user == 'Overall':
        num_messages = chats.shape[0]
        num_words = wrdCt(chats)
    else :
        num_messages = chats[chats['Sender']==user].shape[0]
        num_words = wrdCt(chats[chats['Sender']==user])

    return (num_messages, num_words)