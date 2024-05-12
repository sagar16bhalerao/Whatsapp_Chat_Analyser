import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w+\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    date = []
    times = []
    for i in dates:
        date.append(i.split(', ')[0])
        times.append(i.split(', ')[1])

    time = []
    for i in times:
        time.append(i.split('\u202f')[0])

    df = pd.DataFrame({'user_message':messages, 'message_date':date})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df