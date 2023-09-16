from collections import Counter
import pandas as pd

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

def most_common(chats, user):
    if user != 'Overall':
        chats = chats[chats['Sender']==user]

    f = open('stopwords_hinglish.txt', 'r')
    stpwrds = f.read().split('\n')
    f.close()

    words = []
    for msg in chats['Message'] :
        if msg == '<media omitted>\n':
            continue
        for wrd in str(msg).lower().split():
            if wrd not in stpwrds:
                words.append(wrd)
    ct = Counter(words)
    return ct

def emoji_analysis(chats, user):
    if user != 'Overall':
        chats = chats[chats['Sender']==user]

    import emoji
    used_emojis= []
    for msg in chats.Message :
        for ch in str(msg):
            if emoji.is_emoji(ch):
                used_emojis.append(ch)
    emoji_count = Counter(used_emojis)
    emoji_count

    used_emojis= pd.DataFrame(emoji_count.most_common(len(emoji_count)), index=range(len(emoji_count)))
    return used_emojis

def monthlyTimeline(chats, user):
    if user != 'Overall':
        chats = chats[chats['Sender']==user]

    timeline = chats.groupby(['Year','Month']).count()['Message'].reset_index()
    month_order = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
    timeline['Month_num'] = timeline.Month.map(month_order)
    timeline.sort_values(by=['Year','Month_num'],inplace=True)
    timeline.reset_index(inplace=True,drop=True)

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline.Year.iloc[i])+" - "+str(timeline.Month.iloc[i]))
    timeline['Time'] = time
    return timeline

def dailyTimeline(chats, user):
    if user != 'Overall':
        chats = chats[chats['Sender']==user]

    chats['Date'] = pd.to_datetime(chats['Year'].astype(str)+ '-' + chats['Month'].astype(str) + '-' + chats['Day'].astype(str))
    DailyCount = chats.groupby(chats.Date).count()['Message'].reset_index()
    DailyCount['Date']= [x.strftime("%d-%m-%y") for x in DailyCount.Date]
    return DailyCount
    
def Activity(chats, user):
    if user != 'Overall':
        chats = chats[chats['Sender']==user]

    wk = chats.groupby('WeekDay').count()['Message'].reset_index()
    wkct = {'Sunday':0, 'Monday':1, 'Tuesday':2, 'Wednesday':3 , 'Thursday':4, 'Friday':5, 'Saturday':6}
    wk['DayN'] = wk['WeekDay'].map(wkct)
    wk = wk.sort_values(by = 'DayN')
    wk.drop(columns = 'DayN', inplace= True)
    wk.reset_index(drop=True,inplace= True)

    mn = chats.groupby('Month').count()['Message'].reset_index()
    mn.reset_index(drop=True,inplace= True)

    return wk,mn


def chat_heatMap(chats,user):
    if user != 'Overall':
        chats = chats[chats['Sender']==user]

    htmp = chats.groupby(['WeekDay','Hour']).count()['Message'].reset_index()
    htmp = htmp.pivot_table(index= 'WeekDay', columns='Hour', values='Message', fill_value=0)
    return htmp
    # from seaborn import heatmap
    # ht = heatmap(htmp,annot = True, cmap = 'gist_gray',linewidths='0.1')
    # return ht