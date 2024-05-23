import pandas as pd
from transformers import pipeline
from transformers import AutoTokenizer

def sentiment_analysis(news_path):
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

def save_in_csv(news_path, news_df):
    # Save the news in a CSV file
    try:
        news_df.to_csv(news_path, sep=';', index=False)
    except:
        print("ERROR : Unable to open the file !")
        raise