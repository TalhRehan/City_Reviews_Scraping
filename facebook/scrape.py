from bs4 import BeautifulSoup
import time
from utils.filter import is_exact_city_mention

def scrape_comments_from_post(post, city, max_comments=5):
    comments = []
    # Try finding comment divs (Facebook changes often, selector may need update)
    comment_divs = post.find_all("div", attrs={"data-ad-preview": "message"})
    count = 0
    for comment in comment_divs:
        comment_text = comment.get_text(separator=" ").strip()
        if is_exact_city_mention(comment_text, city):
            comments.append({
                "review": comment_text,
                "date": "N/A",  # Date extraction can be added
                "city": city
            })
            count += 1
            if count >= max_comments:
                break
    return comments

def scrape_facebook_group_posts_with_comments(driver, group_url, city, max_posts=5, max_comments=5):
    driver.get(group_url)
    time.sleep(5)
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
        if is_exact_city_mention(post_text, city):
            results.append({
                "review": post_text.strip(),
                "date": date_text,
                "city": city
            })
        # Now get comments for this post
        comments = scrape_comments_from_post(post, city, max_comments)
        results.extend(comments)
    return results
