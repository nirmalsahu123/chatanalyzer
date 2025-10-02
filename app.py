
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    # st.dataframe(df)


    # fetch user unique

    unique_user = df['user'].unique().tolist()
    unique_user.remove('group notifications')
    unique_user.sort()
    unique_user.insert(0,"overall")


    selected_user = st.sidebar.selectbox("select user", unique_user)
    

    if st.sidebar.button("show analysis"):

        num_messages, words,num_media, url = helper.fetch_stats(selected_user,df)
        st.title("TOP STATISTICS")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("total messages")
            st.title(num_messages)

        with col2:
            st.header("total words")
            st.title(words)
        with col3:
            st.header("shared media")
            st.title(num_media)
        with col4:
            st.header("shared links")
            st.title(url)
        
        # time line 
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # daily time line 
        st.title("Daily_timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # ACTIVITY MAP
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            st.pyplot(fig)
            

        #ACTIVITY H+EATMAP
        st.title("weekly activity map")
        heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)


        #finding the busiest user in tthe group
        if selected_user=='overall':
            st.title('Most busy user')
            x,y = helper.fetch_busy_user(df)
            fig,ax = plt.subplots()
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(y)
        
        #wordcloud
        st.title('word cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title('Most common words')
        df = helper.most_common_words(selected_user, df)
        fig,ax = plt.subplots()
        ax.barh(df[0], df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # # most common emojis
        # emojis = helper.most_common_emoji(selected_user,df)
        # st.title("Emoji Analysis")

        # col1, col2 = st.columns(2)
        # with col1:
        #     st.dataframe(emojis)
        # with col2:
        #     fig, ax = plt.subplot()
        #     ax.pie(emojis[1], labels= emojis[0])
        #     st.pyplot(fig)
            

        #
        




