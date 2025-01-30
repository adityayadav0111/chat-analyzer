import re 
import pandas as pd

def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_msg':messages,'msg_date':dates})

    ## Converting Datatype of "msg_date"
    df['msg_date'] = pd.to_datetime(df['msg_date'],format='%d/%m/%Y, %H:%M -  ')


    ## Changing col name for better readability
    df.rename(columns={'msg_date':'date'},inplace=True)


    users = []
    msg = []

    for i in df['user_msg']:
        entry = re.split(r'([\w\W]+?):\s',i)
        if entry[1:]: # Which will be basically user
            users.append(entry[1])
            msg.append(entry[2])
        else:
            users.append('group_notificaion')   ## This is basically system-generated notifications
            msg.append(entry[0])

    df['user'] = users
    df['message'] = msg
    df.drop(columns = ['user_msg'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['only_date'] = df['date'].dt.date
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()
    df['month_name'] = df['date'].dt.month_name()

    ## Hourly-daywise heat map
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1 ))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
        
    return df