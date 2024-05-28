import pandas as pd
import streamlit as st

def display_data(news_path, news_history_path):
    # Load the data from the CSV file
    dataFrame = pd.read_csv(news_path, sep=";")

    # Load the news history from the CSV file
    news_history_df = pd.read_csv(news_history_path, sep=";")

    # Application title
    st.write("""# News scrapped from Bitcon.com""")

    # Create a session state for the button
    if 'button_state' not in st.session_state:
        st.session_state['button_state'] = 0

    # Display the CSV file if the button is clicked
    if st.button('Display news'):
        if st.session_state['button_state'] == 0:
            st.write(dataFrame)
            st.session_state['button_state'] = 1
        else:
            st.write("")  # Effacez les nouvelles
            st.session_state['button_state'] = 0

    # Title
    st.write("""### Today's news sentiment analysis""")

    # display a bar chart
    bar_chart(dataFrame)

    # Title
    st.write("""### Historical news sentiment analysis""")
    line_chart(news_history_df)


def  bar_chart(dataFrame):
    # display a bar chart

    # Count the number of 'positive', 'negative', and 'neutral' in the 'sentiment' column
    sentiment_counts = pd.DataFrame(dataFrame['sentiment'].value_counts())

    # Create a bar chart
    st.bar_chart(sentiment_counts)

def line_chart(dataFrame):
    # display a line chart

    # Create a line chart
    st.line_chart(dataFrame, x='Date', y='sentiment')

### TODO
# Use matplotlib to display the data
"""
import matplotlib.pyplot as plt

# Create a line chart
plt.figure()
plt.plot(dataFrame['Date'], dataFrame['sentiment'])
plt.gca().invert_yaxis()
plt.show()
"""