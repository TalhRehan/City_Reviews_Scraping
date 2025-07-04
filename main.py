import csv
import os
import sys
from datetime import datetime
from facebook.login_and_navigate import manual_facebook_login
from facebook.config_loader import get_facebook_urls_for_city
from facebook.scrape import scrape_facebook_group_posts_with_comments
from twitter.scrape import search_twitter_for_city_with_replies
from utils.dedupe import deduplicate_reviews

def save_reviews_to_csv(reviews, city):
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"{today}_{city}.csv"
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
    headers = ['review', 'date', 'city']

    with open(downloads_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)

    print(f"Saved {len(reviews)} reviews to {downloads_path}")

if __name__ == "__main__":
    # Get city from command line argument, default to "Lahore"
    city = sys.argv[1] if len(sys.argv) > 1 else "Lahore"
    print(f"Scraping reviews for city: {city}")

    fb_urls = get_facebook_urls_for_city(city)
    print(f"Facebook URLs for {city}: {fb_urls}")

    all_reviews = []

    # Facebook scraping (posts + comments)
    if fb_urls:
        driver = manual_facebook_login()
        print(f"Scraping posts and comments from: {fb_urls[0]}")
        fb_reviews = scrape_facebook_group_posts_with_comments(driver, fb_urls[0], city)
        for review in fb_reviews:
            print("---")
            print(f"FB: {review['review'][:200]}")
            print(f"Date: {review['date']}")
        driver.quit()
        all_reviews.extend(fb_reviews)

    # Twitter scraping (tweets + replies)
    twitter_reviews = search_twitter_for_city_with_replies(city)
    for review in twitter_reviews:
        print("---")
        print(f"TW: {review['review'][:200]}")
        print(f"Date: {review['date']}")
    all_reviews.extend(twitter_reviews)

    # Deduplicate and save
    unique_reviews = deduplicate_reviews(all_reviews)
    save_reviews_to_csv(unique_reviews, city)
