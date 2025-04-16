import re
import pandas as pd

def split_user_msg(msg,user,message):
    msg.strip()
    user_msg = msg.split(sep=':',maxsplit=1)
    if len(user_msg)==1:
        user.append('Group Notification')
        message.append(user_msg[0].strip())
    else:
        user.append(user_msg[0].strip())
        message.append(user_msg[1].strip())

def preprocess(data):
    pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s')
    Messages = pattern.split(data)[1:]
    Dates = pattern.findall(data)
    Dates = list(map(lambda date: date.split('-')[0].strip(),Dates))
    user = []
    message = []
    for msg in Messages:
        split_user_msg(msg,user,message)
    
    df = pd.DataFrame({'Date': Dates, 'User': user, 'Message': message})
    return df
