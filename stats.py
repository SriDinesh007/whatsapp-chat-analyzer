import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import datetime as dt

class Analysis:

    extractor = URLExtract()

    def __init__(self,selected_user,df):
        self.selected_user = selected_user
        if selected_user != 'Overall':
            self.df = df[df['User'] == selected_user]
        else:
            self.df = df

    def basic_stats(self):

        num_messages = self.df.shape[0]
        num_words = 0
        num_media_files = 0
        num_links = 0
        emojis = []
        for message in self.df['Message']:
            emojis.extend([c for c in message if emoji.is_emoji(c)])
            num_words += len(message.split())
            num_links += len(self.extractor.find_urls(message))
            if message.strip() == '<Media omitted>':
                num_media_files += 1
        
        emoji_df = pd.DataFrame(Counter(emojis).most_common())
        emoji_df.columns = ['Emoji', 'Count']
        
        return num_messages, num_words, num_media_files, num_links, emoji_df
    
    def busy_chatter(self):

        users = self.df[self.df['User']!='Group Notification']['User']
        # Top 5 most active users by message count
        top_users = users.value_counts().head()

        # Calculate percentage contribution for all users
        user_percentage = (users.value_counts() / users.shape[0]) * 100
        user_percentage_df = user_percentage.reset_index()
        user_percentage_df.columns = ['User', 'Percentage of total messages']

        return top_users, user_percentage_df
    
    def create_word_cloud(self,common_words_df):
        wc= WordCloud(width=500,height=500,min_font_size=10,background_color='white')
        wc_image = wc.generate(common_words_df[0].str.cat(sep=" "))
        return wc_image

    def get_commmon_words_and_word_cloud(self):
        with open('stop_hinglish.txt','r',encoding='utf-8') as file:
            stopwords = file.read()
        
        stopwords = stopwords.split('\n')

        temp_df = self.df[self.df['User']!='Group Notification']
        words = []
        for msg in temp_df['Message']:
            msg = msg.lower().strip()
            if msg != 'this message was deleted':
                for word in msg.split():
                    if word not in stopwords and word not in ['<media','omitted>'] and not emoji.is_emoji(word):
                        words.append(word)
        
        most_common_words_df = pd.DataFrame(Counter(words).most_common())

        wc_image = self.create_word_cloud(most_common_words_df)

        return most_common_words_df, wc_image


    def weekActivityMap_monthActivityMap_monthTimeline(self):
        temp_df = self.df
        temp_df['year'] = pd.to_datetime(self.df['Date']).dt.year
        temp_df['month'] = pd.to_datetime(self.df['Date']).dt.month_name()
        temp_df['day'] = pd.to_datetime(self.df['Date']).dt.day_name()

        weekActivityMap = temp_df['day'].value_counts()
        monthActivityMap = temp_df['month'].value_counts()
        temp_df = temp_df.groupby(['year','month']).count()['Message'].reset_index()
        time = []
        for i in range(temp_df.shape[0]):
            time.append(temp_df['month'][i]+'-'+str(temp_df['year'][i]))
        temp_df['month'] = time
        temp_df.drop(columns=['year'],inplace=True)
        return weekActivityMap, monthActivityMap, temp_df
    
    









    
            

           

        