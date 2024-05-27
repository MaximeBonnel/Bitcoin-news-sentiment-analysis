import pandas as pd
import streamlit as st

def display_data(news_path):
    # Load the data from the CSV file
    dataFrame = pd.read_csv(news_path, sep=";")

    # Application title
    st.write("""# News scrapped from Bitcon.com""")

    # display a bar chart
    bar_chart(dataFrame)

    # Display the CSV file
    st.write(dataFrame)


def  bar_chart(dataFrame):
    # display a bar chart

    # Count the number of 'positive', 'negative', and 'neutral' in the 'sentiment' column
    sentiment_counts = pd.DataFrame(dataFrame['sentiment'].value_counts())

    # Create a bar chart
    st.bar_chart(sentiment_counts)