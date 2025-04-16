#import sys
import streamlit as st
import preprocess
from stats import Analysis
import matplotlib.pyplot as plt
import numpy as np

#st.write(f"Current Python executable: {sys.executable}")

st.sidebar.title("Whatsapp Chat Analyzer")

def file_format(uploaded_file):
    return uploaded_file.name.split('.')[-1].lower()

def prepare_user_list(df):
    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    # including 'Overall' in user_list, this will be responsible for showing the entire chat group analysis
    user_list.insert(0,'Overall')
    return user_list 


if __name__ == '__main__':
    # Upload file
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    # Check if no file uploaded
    if uploaded_file is None:
        st.title(
            """
            **Welcome!**

            Please upload your exported WhatsApp **`.txt` chat file** to begin the analysis.
            
            We'll help you explore messages, word counts, and much more!
            """
        )
        st.error("🚫 You haven't selected any file yet. Please upload a .txt chat file.")
    
    # If wrong file type
    elif file_format(uploaded_file) != 'txt':
        st.title(
            """
            **Welcome!**

            Please upload your exported WhatsApp **`.txt` chat file** to begin the analysis.
            
            We'll help you explore messages, word counts, and much more!
            """
        )
        st.error("🚫 Invalid file type. Please upload a WhatsApp-exported `.txt` file.")

    # Valid file uploaded
    else:
        try:
            data = uploaded_file.read().decode('utf-8').strip()
            if not data:
                st.error("🚫 The uploaded file is empty.")
            else:
                st.success("✅ File uploaded successfully!")

                df = preprocess.preprocess(data)
                
                if st.checkbox("🔍 Show full chat content"):
                    st.dataframe(df)

                # We need to organize the analysis based on the selected user
                user_list = prepare_user_list(df)
                selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

                st.title('Whatsapp Chat Analysis for ' + selected_user)
                if st.sidebar.button("Show Analysis"):
                    analyst_obj = Analysis(selected_user,df)

                    # basic stats
                    num_messages, num_words, num_media_files, num_links, emoji_df = analyst_obj.basic_stats()

                    # phase 1: show the basic stats one below the other

                    st.header("📨 Total Messages")
                    st.subheader(num_messages)

                    st.header("📝 Total Number of Words")
                    st.subheader(num_words)

                    st.header("📷 Number of Media Files Shared")
                    st.subheader(num_media_files)

                    st.header("🔗 Total Number of Links Shared")
                    st.subheader(num_links)

                    # phase 2: finding the busiest chatter in hte group
                    if selected_user == 'Overall':

                        # Dividing the space into two st.columns
                        # first column is for the bar chart and the second column is for the dataframe representation of top users
                        st.title('Most Busy Users')
                        top_users, top_users_df = analyst_obj.busy_chatter()
                        fig, ax = plt.subplots()
                        col1, col2 = st.columns(2)
                        with col1:
                            ax.bar(top_users.index,top_users.values,color='red')
                            plt.xticks(rotation='vertical')
                            st.pyplot(fig)

                        with col2:
                            st.dataframe(top_users_df)

                    # phase 3: word cloud
                    
                    st.title('Word Cloud')
                    most_common_words_df, wc_image = analyst_obj.get_commmon_words_and_word_cloud()
                    fig,ax = plt.subplots()
                    ax.imshow(wc_image)
                    st.pyplot(fig)

                    # phase 4: most common words in the chat
                    st.title('Most Common Words')
                    #st.dataframe(most_common_words_df)
                    fig,ax = plt.subplots()
                    ax.barh(most_common_words_df.head(20)[0],most_common_words_df.head(20)[1])
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                    # phase 5: Emoji analysis
                    st.title('Emoji Analysis')
                    emojicount = list(emoji_df['Count'])
                    perlist = [(i/sum(emojicount))*100 for i in emojicount]
                    emoji_df['Percentage use'] = np.array(perlist)
                    st.dataframe(emoji_df)


                    # phase 6: Monthly timeline
                    st.title('Mothly Timeline')
                    weekActivityMap, monthActivityMap, monthTimeline = analyst_obj.weekActivityMap_monthActivityMap_monthTimeline()
                    fig, ax = plt.subplots()
                    ax.plot(monthTimeline['month'], monthTimeline['Message'],color='green')
                    plt.xticks(rotation='vertical')
                    plt.tight_layout()
                    st.pyplot(fig)

                    # phase 7: Activity maps
                    st.title('Activity Maps')
                    col1, col2 = st.columns(2)
                    with col1:
                        st.header('Most Busy Day')
                        fig, ax = plt.subplots()
                        ax.bar(weekActivityMap.index,weekActivityMap.values,color='purple')
                        plt.xticks(rotation='vertical')
                        plt.tight_layout()
                        st.pyplot(fig)
                    with col2:
                        st.header('Most Busy Month')
                        fig, ax = plt.subplots()
                        ax.bar(monthActivityMap.index,monthActivityMap.values,color='orange')
                        plt.xticks(rotation='vertical')
                        plt.tight_layout()
                        st.pyplot(fig)



                    
                
        except UnicodeDecodeError:
            st.error("⚠️ Could not decode the file. Please ensure it is UTF-8 encoded.")

    
    



