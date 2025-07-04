from rapidfuzz import fuzz

def is_exact_city_mention(text, city, threshold=85):
    # Checks if the city is mentioned as a standalone word, not as part of another city
    words = text.lower().split()
    city_lower = city.lower()
    for word in words:
        # Use fuzzy ratio for flexibility, but must be a strong match
        if fuzz.ratio(word, city_lower) >= threshold:
            return True
    return False
