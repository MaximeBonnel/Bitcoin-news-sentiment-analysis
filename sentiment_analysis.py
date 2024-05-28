import os
import time
import pandas as pd
from transformers import pipeline
from transformers import AutoTokenizer

def sentiment_analysis(news_path, news_history_path):
    # Parameters
    MODEL = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    MAX_TOKEN = 510

    # Import the tokenizer to know the maximum length of the input
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # Import the data
    data = pd.read_csv(news_path, sep=';')
    # Convert the 'sentiment' column to string type
    data['sentiment'] = data['sentiment'].astype(str)

    # Import the model
    nlp = pipeline("sentiment-analysis", model=MODEL)

    # Analyze the sentiment of acticles
    for index in data.index:
        # Check if there is a head, otherwise use the content
        if data.loc[index, 'head'] is not None:
            context = data.loc[index, 'head']
        else:
            context = data.loc[index, 'content']

        # Convert context in tokens and truncate if necessary
        tokens = tokenizer.tokenize(context)
        if len(tokens) > MAX_TOKEN:
            tokens = tokens[:MAX_TOKEN]

        # Revert tokens to text and analize it
        context = tokenizer.convert_tokens_to_string(tokens)
        sentiment = nlp(context)

        # Add the sentiment to the dataframe
        data.loc[index, 'sentiment'] = sentiment[0]['label']

    # Save the dataframe in the CSV file
    save_in_csv(news_path, data)

    # Add the global news sentiment in the news history
    news_history(news_path, news_history_path)

def news_history(news_path, news_history_path):
    # If there is a news history file, load it otherwise create it
    if os.path.exists(news_history_path):
        # Load the historical news
        news_history_df = pd.read_csv(news_history_path, sep=';')
    else:
        # Create a DataFrame
        news_history_df = pd.DataFrame(columns=['Date', 'sentiment'])

    # Load the news
    news_df = pd.read_csv(news_path, sep=';')

    # Add the news sentiment in the news history DataFrame
    sentiment_counts = news_df['sentiment'].value_counts()

    positive_count = sentiment_counts.get('positive')
    negative_count = sentiment_counts.get('negative')

    if positive_count > negative_count:
        news_history_df.loc[len(news_history_df)] = [time.strftime("%d-%m-%y"), 'positive']
    elif positive_count < negative_count:
        news_history_df.loc[len(news_history_df)] = [time.strftime("%d-%m-%y"), 'negative']
    else:
        news_history_df.loc[len(news_history_df)] = [time.strftime("%d-%m-%y"), 'neutral']

    # Save the news history in a CSV file
    save_in_csv(news_history_path, news_history_df)

def save_in_csv(news_path, news_df):
    # Save the news in a CSV file
    try:
        news_df.to_csv(news_path, sep=';', index=False)
    except:
        print("ERROR : Unable to open the file !")
        raise