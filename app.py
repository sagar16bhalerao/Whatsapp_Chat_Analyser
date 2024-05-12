import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Welcome to the WhatsApp Chat Analyzer \nCreated and Developed by Sagar Bhalerao')
st.text('From the WhatsApp app, export the chat you want to analyze. You can do this by \nopening the chat, tapping on the three dots in the top right corner, \nselecting "More," then "Export chat without media and upload it by \nclicking Browse Files."')


uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    st.header('Your Whatsapp Analysis\n(Click on Show analysis to see full analysis)')
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        # stats area
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(num_words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)
        with col4:
            st.header('Links Shared')
            st.title(num_links)

        # monthly timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)

        fig = px.line(timeline,'time','message',labels={'time':'Month','message':'No. of Messages'})
        st.plotly_chart(fig)

        # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)

        fig = px.line(daily_timeline,'only_date','message',labels={'only_date':'Date','message':'No. of Messages'})
        st.plotly_chart(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig = px.bar(busy_day,busy_day.index,busy_day.values,labels={'day_name':'Day','y':'No. of Messages'},width=330,height=500)
            st.plotly_chart(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig = px.bar(busy_month, busy_month.index, busy_month.values,labels={'month': 'Month', 'y': 'No. of Messages'},width=330,height=500)
            st.plotly_chart(fig)

        # finding the busiest users in the group (group level)
        if selected_user == 'Overall':

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.title('Top 5 Busy Users')
                ax.bar(x.index, x.values, color='#4a21ec')
                plt.xticks(rotation='vertical')
                plt.ylabel('No. of Messages')
                plt.xlabel('User Name')
                st.pyplot(fig)
            with col2:
                st.title('Messages in %')
                st.dataframe(new_df)
        # WordCloud
        st.header('WordCloud \n The size of word shows how frequently that word is used \n i.e The bigger the size, the more frequently the word used.')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.header('Top 20 Most Commonly Used Words')
        col1,col2 = st.columns(2)

        with col1:
            most_common_df = helper.most_common_words(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df['Word'],most_common_df['No of times it appeared in chat'])
            st.pyplot(fig)
        with col2:
            st.dataframe(most_common_df)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')

        col1, col2 = st.columns([1,3])

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = px.bar(emoji_df, x=0, y=1)
            st.plotly_chart(fig)





