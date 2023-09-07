'''
This file would contain a function PreProcess(Chats)
The input will be the text data and would return a pandas dataframe
the columns of the dataframe would be 
Message, Sender, Year, Month, Day, Hour, Minute
'''
import re
import pandas as pd
def PreProcess(Chats):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    Messages = re.split(pattern,Chats)[1:]
    TimeStamp = re.findall(pattern, Chats)
    Data = pd.DataFrame({'Stamp':TimeStamp, "Message": Messages})
    Data['Stamp'] = pd.to_datetime(Data['Stamp'], format='%m/%d/%y, %H:%M - ')

    Senders = []
    Messages = []

    for msg in Data['Message'] :
        ent = re.split('([\w\W]+?):\s', msg)
        if ent[1:] :            # If having any sender
            Senders.append(ent[1])
            Messages.append(ent[2].lower())
        else :
            Senders.append("Notification")
            Messages.append(ent[0].lower())

    Data['Sender']  = Senders
    Data['Message'] = Messages

    Data['Year'] = Data['Stamp'].dt.year
    Data['Month'] = Data['Stamp'].dt.month_name()
    Data['Day'] = Data['Stamp'].dt.day
    Data['Hour'] = Data['Stamp'].dt.hour
    Data['Minute'] = Data['Stamp'].dt.minute
    Data.drop('Stamp', axis=1, inplace=True)

    return Data