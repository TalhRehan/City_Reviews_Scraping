from bs4 import BeautifulSoup
import time
from utils.filter import is_exact_city_mention

def scrape_facebook_group_posts(driver, group_url, city, max_posts=5):
    driver.get(group_url)
    time.sleep(5)  # Wait for page to load

    for _ in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "lxml")
    posts = soup.find_all("div", attrs={"role": "article"})
    print(f"Found {len(posts)} posts on this page.")

    results = []
    for post in posts[:max_posts]:
        text_elements = post.find_all("div", attrs={"dir": "auto"})
        post_text = " ".join([el.get_text(separator=" ") for el in text_elements])

        date_text = "N/A"
        date_candidate = post.find("a", href=True)
        if date_candidate and date_candidate.has_attr("aria-label"):
            date_text = date_candidate["aria-label"]

        # Only save posts that match city!
        if is_exact_city_mention(post_text, city):
            results.append({
                "review": post_text.strip(),
                "date": date_text,
                "city": city
            })

    return results
