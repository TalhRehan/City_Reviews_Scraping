from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from utils.filter import is_exact_city_mention

def get_tweet_url(tweet):
    a_tag = tweet.find("a", href=True)
    if a_tag and '/status/' in a_tag['href']:
        return "https://twitter.com" + a_tag['href']
    return None

def scrape_replies_for_tweet(driver, tweet_url, city, max_replies=5):
    replies = []
    driver.get(tweet_url)
    time.sleep(6)  # Wait for replies to load

    soup = BeautifulSoup(driver.page_source, "lxml")
    reply_divs = soup.find_all("div", attrs={"data-testid": "tweet"})
    for reply in reply_divs[1:max_replies+1]:  # Skip first (main tweet)
        reply_text = ""
        for span in reply.find_all("span"):
            reply_text += span.text + " "
        date_tag = reply.find("time")
        reply_date = date_tag["datetime"] if date_tag else "N/A"
        if is_exact_city_mention(reply_text, city):
            replies.append({
                "review": reply_text.strip(),
                "date": reply_date,
                "city": city
            })
    return replies

def search_twitter_for_city_with_replies(city, max_tweets=5, max_replies=5):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    search_url = f"https://twitter.com/search?q={city}&src=typed_query&f=live"
    driver.get(search_url)
    print(f"Searching Twitter for: {city}")
    time.sleep(10)

    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    soup = BeautifulSoup(driver.page_source, "lxml")
    tweet_divs = soup.find_all("div", attrs={"data-testid": "tweet"})
    print(f"Found {len(tweet_divs)} tweets for {city}")

    all_results = []
    tweet_count = 0
    for tweet in tweet_divs:
        if tweet_count >= max_tweets:
            break
        tweet_text = ""
        for span in tweet.find_all("span"):
            tweet_text += span.text + " "
        date_tag = tweet.find("time")
        tweet_date = date_tag["datetime"] if date_tag else "N/A"

        if is_exact_city_mention(tweet_text, city):
            all_results.append({
                "review": tweet_text.strip(),
                "date": tweet_date,
                "city": city
            })

            # Scrape replies
            tweet_url = get_tweet_url(tweet)
            if tweet_url:
                replies = scrape_replies_for_tweet(driver, tweet_url, city, max_replies)
                all_results.extend(replies)
            tweet_count += 1

    driver.quit()
    return all_results
