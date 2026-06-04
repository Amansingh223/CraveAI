import os
import requests
import re

UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

def get_food_image(recipe_name: str) -> str:
    """Fetches a food image from Unsplash or falls back to a placeholder."""
    if UNSPLASH_KEY and UNSPLASH_KEY != "your_unsplash_access_key_here":
        try:
            query = "+".join(recipe_name.split()[:3])
            url = (
                f"https://api.unsplash.com/photos/random"
                f"?query={query}+food&orientation=landscape&client_id={UNSPLASH_KEY}"
            )
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                return resp.json()["urls"]["regular"]
        except Exception:
            pass
            
    # Fallback if Unsplash fails or key is missing
    seed = abs(hash(recipe_name)) % 1000
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', recipe_name)
    tags = clean_name.replace(' ', ',')
    return f"https://loremflickr.com/900/600/{tags},food?lock={seed}"
