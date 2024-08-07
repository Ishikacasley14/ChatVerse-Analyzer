import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
import functions
from PIL import Image

im = Image.open("what.ico")
st.set_page_config(
    page_title="WhatsApp Analysis",
    page_icon=im,
    layout="wide",
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("Do Visit @: ")
with col2:
    st.markdown("[LinkedIn](https://www.linkedin.com/in/ishika-casley/)")
with col3:
    st.markdown("[GitHub](https://github.com/Ishikacasley14)")
with col4:
    st.markdown("[My Portfolio](https://your-portfolio-link.com)") 


st.title('WhatsApp Chat Analyzer')
# Sidebar content
col1, col2, col3, col4 = st.sidebar.columns([1, 2, 2, 1])
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/479px-WhatsApp.svg.png', width=90)
with col3:
    st.image('analy.png', width=90)

st.sidebar.caption(
    'This application lets you analyze WhatsApp conversations in a very comprehensive manner, with charts, metrics, '
    'and other forms of analysis.'
)
st.sidebar.markdown('Developed with Streamlit, Developed by Ishika Casley')

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a TXT file", type="txt")

# Main content
with st.expander('See!!.. How it works?'):
    st.subheader('Steps to Analyze:')
    st.markdown(
        '1. Export the chat by going to WhatsApp on your phone, opening the chat, clicking on the three dots, '
        'selecting "More," and then choosing "Export Chat" without media. Save the file to your desired location.'
    )
    st.markdown(
        '2. Browse or drag and drop the chat file.'
    )
    st.markdown('3. Select a user or group to analyze, or leave the default setting of "All" to analyze for all users.')
    st.markdown('4. Click the "Show Analysis" button.')
    st.markdown(
        '5. Enable "Wide mode" for a better viewing experience in settings, or close the sidebar on mobile for improved view.'
    )
    st.markdown(
        '6. To analyze for a single user, select their name from the dropdown and click "Show Analysis" again.'
    )
    st.markdown('7. Repeat the steps for additional chats.')
if uploaded_file:
    df = functions.generateDataFrame(uploaded_file)
    try:
        dayfirst = st.radio("Select Date Format in text file:",('dd-mm-yy', 'mm-dd-yy'))
        if dayfirst=='dd-mm-yy':
            dayfirst=True
        else:
            dayfirst=False
        users = functions.getUsers(df)
        users_s = st.sidebar.selectbox("Select User to View Analysis", users)
        selected_user=""

        if st.sidebar.button("Show Analysis"):
            selected_user = users_s

            st.title("Showing Reults for : " + selected_user)
            df = functions.PreProcess(df,dayfirst)
            if selected_user != "Everyone":
                df = df[df['User'] == selected_user]
            df, media_cnt, deleted_msgs_cnt, links_cnt, word_count, msg_count = functions.getStats(df)
            st.title("Chat Statistics")
            stats_c = ["Total Messages", "Total Words", "Media Shared", "Links Shared", "Messages Deleted"]
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.subheader(stats_c[0])
                st.title(msg_count)
            with c2:
                st.subheader(stats_c[1])
                st.title(word_count)
            with c3:
                st.subheader(stats_c[2])
                st.title(media_cnt)
            with c4:
                st.subheader(stats_c[3])
                st.title(links_cnt)
            with c5:
                st.subheader(stats_c[4])
                st.title(deleted_msgs_cnt)

            # User Activity Count
            if selected_user == 'Everyone':
                x = df['User'].value_counts().head()
                name = x.index
                count = x.values
                st.title("Messaging Frequency")
                st.subheader('Messaging Percentage Count of Users')
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
                    columns={'User': 'name', 'count': 'percent'}))
                with col2:
                    fig, ax = plt.subplots()
                    ax.bar(name, count)
                    ax.set_xlabel("Users")
                    ax.set_ylabel("Message Sent")
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

            # Emoji
            emojiDF = functions.getEmoji(df)
            st.title("Emoji Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emojiDF)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emojiDF[1].head(), labels=emojiDF[0].head(), autopct="%0.2f", shadow=True)
                plt.legend()
                st.pyplot(fig)

            # Common Word
            commonWord = functions.MostCommonWords(df)
            fig, ax = plt.subplots()
            ax.bar(commonWord[0], commonWord[1])
            ax.set_xlabel("Words")
            ax.set_ylabel("Frequency")
            plt.xticks(rotation='vertical')
            st.title('Most Frequent Words Used In Chat')
            st.pyplot(fig)

            # Monthly Timeline
            timeline = functions.getMonthlyTimeline(df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['Message'])
            ax.set_xlabel("Month")
            ax.set_ylabel("Messages Sent")
            plt.xticks(rotation='vertical')
            st.title('Monthly Timeline')
            st.pyplot(fig)

            # Daily Timeline
            functions.dailytimeline(df)

            st.title('Most Busy Days')
            functions.WeekAct(df)
            st.title('Most Busy Months')
            functions.MonthAct(df)

            # WordCloud
            st.title("Wordcloud")
            df_wc = functions.create_wordcloud(df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = functions.activity_heatmap(df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

    except Exception as e:
        st.subheader("Unable to Process Your Request")

        st.subheader('Stay tune for more updates!!')

        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown('\n')
            st.markdown('\n')
            st.markdown('\n')
            st.image('https://media.giphy.com/media/xKRQG1M6w1ki10mHZY/giphy.gif', caption="Thank You!!")

        