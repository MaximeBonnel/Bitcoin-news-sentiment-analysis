import pandas as pd
import streamlit as st

def display_data(news_path):
    # Load the data from the CSV file
    dataFrame = pd.read_csv(news_path, sep=";")

    # Application title
    st.write("""# News scrapped from Bitcon.com""")

    # Display the CSV file
    st.write(dataFrame)