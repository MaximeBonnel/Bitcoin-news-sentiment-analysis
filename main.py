from news_scraping import news_scraping
from sentiment_analysis import sentiment_analysis
from display_data import display_data
import time
import os

# Number of news to scrap
NUMBER_OF_NEWS = 10

# News path in fuction of the date
date = time.strftime("%d-%m-%y")
NEWS_PATH = 'data/news_' + date + '.csv'

# Scraping of the news
if not os.path.exists(NEWS_PATH):
    news_scraping(NEWS_PATH, NUMBER_OF_NEWS)
    print("News have been scraped !")

# Sentiment analysis
sentiment_analysis(NEWS_PATH)
print("Sentiment analysis done !")

# Display the data
display_data(NEWS_PATH)
print("Data have been displayed !\n")

#TODO
# - Try to get the date of the news
# - Add some graphs to display the data