def fetch_stats(user, chats):
    if user == 'Overall':
        return chats.shape[0]