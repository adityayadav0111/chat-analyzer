from urlextract import URLExtract
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji



## Creating obj of URL Extract
extract = URLExtract()

## Statistics (Row 1)
def fetch_stats(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    ## Total No of messages        
    num_messages = df.shape[0]

    ## Total no of words
    words=[]
    for i in df['message']:
        words.extend(i.split())

    ## Total media shared
    num_media = df[df['message']=='<Media omitted>\n'].shape[0]

    ## Total no of links
    num_links=[]
    for i in df['message']:
        num_links.extend(extract.find_urls(i))
        
    return num_messages,len(words),num_media,len(num_links)
# ------------------------------------------------------------------------------

## Most Active user in a group(Row 2)
def most_active_users(df):
    x = df['user'].value_counts().head()

    perc_df = round((df['user'].value_counts() / df.shape[0])*100,2).reset_index().rename(columns={'percent':'Name','count':'percent'})

    return x, perc_df
# ------------------------------------------------------------------------------



## Wordcloud
def create_wordcloud(selected_user,df):

    f = open('stopwords.txt','r')
    stop_words1 = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

## removal of unnecessary messages and users
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop(message):
        y =[]
        for i in message.lower().split():
            if i not in stop_words1:
                y.append(i)
            return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = df['message'].apply(remove_stop)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


# ------------------------------------------------------------------------------

## Common words
def most_common(selected_user,df):

    f = open('stopwords.txt','r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

## removal of unnecessary messages and users
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words =[]
    for i in temp['message']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)

    most_comm = Counter(words).most_common(20)
    new_df = pd.DataFrame(most_comm)

    return new_df
# ------------------------------------------------------------------------------

## Emoji Analysis

def most_used_emo(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis =[]
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])
        
        emo = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emo

# ------------------------------------------------------------------------------

## Message Trend
def monthly_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

# ------------------------------------------------------------------------------

## Daily Timeline
def daily_timeline(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby("only_date").count()['message'].reset_index()

    return daily_timeline


# ------------------------------------------------------------------------------
## weekly activity

def weekly_activity(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

# ------------------------------------------------------------------------------

## Monthly 
def monthly_activity(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month_name'].value_counts()

# ------------------------------------------------------------------------------
 ## heatmap
def activity_heatmap(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    plt.figure(figsize=(20,6))
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap

    




    













