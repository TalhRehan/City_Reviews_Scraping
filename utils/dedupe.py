def deduplicate_reviews(reviews):
    seen = set()
    unique_reviews = []
    for review in reviews:
        # Use the review text and date as the unique key
        key = (review["review"].strip().lower(), review["date"])
        if key not in seen:
            unique_reviews.append(review)
            seen.add(key)
    return unique_reviews
