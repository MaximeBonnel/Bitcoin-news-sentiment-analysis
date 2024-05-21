import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

def news_scraping(news_path, number_of_news):
    # Constants
    URL = "https://news.bitcoin.com"

    # Create a DataFrame
    news_df = pd.DataFrame(columns=['title', 'head', 'content', 'sentiment'])

    # Scraping of the news
    news_df = scraping(URL, number_of_news, news_df)

    # Save the news in a CSV file
    save_in_csv(news_path, news_df)
    

def scraping(url, number_of_news, news_df):
    # Initializations
    page_index = 1
    counter = 0

    driver = webdriver.Firefox()

    while counter <= number_of_news:
        # Open the website & wait for the page to load
        driver.get(url + '/page/' + str(page_index) + '/')
        time.sleep(3)

        # Get the content of the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Search the articles in the page
        table = soup.find('div', attrs={'class': 'sc-ebDIoU'})

        if table is None:
            print("ERROR : Unable to find the articles !")
            raise

        for row in table.findAll('div', attrs={'class': 'sc-gcgBMM'}):
            article = {}
            
            # Get the content of the article
            article = article_scraping(driver, url + row.a['href'])

            # Save the article in the DataFrame
            news_df = news_df._append(article, ignore_index=True)
            
            counter += 1
            if counter > number_of_news:
                break
        
            # Change the page index if the counter is modulable by 6
            if counter % 6 == 0:
                page_index += 1

    return news_df

def article_scraping(driver, url):
    # Open the website & wait for the page to load
    driver.get(url)
    time.sleep(3)

    # Get the content of the page
    article_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Get the title of the article
    try:
        title = article_soup.find('h1', attrs={'class': 'sc-eRVdyy'}).text
    except AttributeError:
        title = 'ERROR'
        print("ERROR : Unable to find the title !")

    # Get the content of the article
    try:
        content = article_soup.find('div', attrs={'class': 'article__body'})
    except AttributeError:
        content = 'ERROR'
        print("ERROR : Unable to find the content !")

    # Get the head of the article
    try:
        head = content.find('strong').text
    except AttributeError:
        head = 'ERROR'
        print("ERROR : Unable to find the head !")

    # Clean the content of the article
    # Delete tags 'h2', 'strong', 'em'
    for tag in ['h2', 'strong', 'em']:
        for match in content.findAll(tag):
            match.decompose()
    content = content.text.strip()


    article = {'title': title, 'head': head, 'content': content, 'sentiment': None}

    return article

def save_in_csv(news_path, news_df):
    # Save the news in a CSV file
    try:
        news_df.to_csv(news_path, sep=';', index=False)
    except:
        print("ERROR : Unable to open the file !")
        raise