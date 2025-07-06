import os
import json
import hashlib

SEEN_PATH = os.path.join("data", "seen_reviews.json")

def load_seen_hashes():
    if not os.path.exists(SEEN_PATH):
        return set()
    with open(SEEN_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_seen_hashes(seen_hashes):
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(list(seen_hashes), f, ensure_ascii=False, indent=2)

def review_hash(review):
    # Hash on text + date + city (change as needed)
    h = hashlib.sha256()
    h.update(review["review"].strip().lower().encode("utf-8"))
    h.update(str(review["date"]).encode("utf-8"))
    h.update(str(review["city"]).encode("utf-8"))
    return h.hexdigest()
