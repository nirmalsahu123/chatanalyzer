from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


def fetch_stats(selected_user, df):
    #fetch number of messages
    if selected_user != 'overall':
        df = df[df['user']==selected_user]
    
    new_messages=df.shape[0]
    # fetch no. of words
    words=[]
    for message in df['message']:
        words.extend(message.split())


    # fetch no. of media messages
    num_media = df[df['message']=='<Media omitted>\n'].shape[0]


    # fetch links
    
    extractor = URLExtract()
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return new_messages, len(words), num_media, len(links)


def fetch_busy_user(df):
    x = df['user'].value_counts().head()
    y = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name', 'user':'percent'})

    return x,y


def create_wordcloud(selected_user, df):
    f= open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    #remove group notification 
    temp = df[df['user']!= 'group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_user,df):
    
    f= open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user!='overall':
        df = df[df['user']==selected_user]
    #remove group notification 
    temp = df[df['user']!= 'group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']
    
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word  not in stop_words:
                words.append(word)

    
    if(Counter(words))==0:
        return pd.DataFrame(words)
    else:
        return pd.DataFrame(Counter(words).most_common(20))
    
    # return pd.DataFrame(Counter(words).most_common(20))
    


# def most_common_emoji(selected_user, df):
#     if selected_user!='overall':
#         df = df[df['user']==selected_user]

#     emojis = []
#     for message in df['message']:
#         emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
#     return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    

def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month','month_num']).count()['message'].reset_index()

    time =[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-" + str(timeline['year'][i]))
    timeline['time']=time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']== selected_user]
    
    return df.groupby('only_date').count()['message'].reset_index()


def week_activity(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']== selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']== selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user!='overall':
        df = df[df['user']== selected_user]
    return df.pivot_table(index='day_name', columns='period',values='message', aggfunc='count').fillna(0)
