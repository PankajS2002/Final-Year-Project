import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}[\u202f\s][apm]+\s-\s'

    messages_list = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates_cleaned = [re.sub(r'[\u202fpma]+', '', date) for date in dates]
    min_length = min(len(messages_list), len(dates_cleaned))
    messages_list = messages_list[:min_length]
    dates_cleaned = dates_cleaned[:min_length]

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages_list, 'message_date': dates_cleaned})

    # Convert the 'message_date' column to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M - ')

    # Rename the 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])


    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df