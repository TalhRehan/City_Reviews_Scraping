from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from utils.filter import is_exact_city_mention

def search_twitter_for_city(city, max_tweets=10):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    search_url = f"https://twitter.com/search?q={city}&src=typed_query&f=live"
    driver.get(search_url)
    print(f"Searching Twitter for: {city}")

    time.sleep(10)  # Wait for tweets to load

    # Scroll to load more tweets (optional)
    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    tweet_divs = soup.find_all("div", attrs={"data-testid": "tweet"})
    print(f"Found {len(tweet_divs)} tweets for {city}")

    results = []
    for tweet in tweet_divs[:max_tweets]:
        tweet_text = ""
        for span in tweet.find_all("span"):
            tweet_text += span.text + " "

        # Try to extract tweet date/time (may need adjustment if Twitter changes HTML)
        date_tag = tweet.find("time")
        tweet_date = date_tag["datetime"] if date_tag else "N/A"

        # FILTER: Only include tweets that actually mention the city
        if is_exact_city_mention(tweet_text, city):
            results.append({
                "review": tweet_text.strip(),
                "date": tweet_date,
                "city": city
            })

    return results
