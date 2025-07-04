import json

def get_facebook_urls_for_city(city, config_path="config/facebook_sources.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        sources = json.load(f)
    return sources.get(city, [])
