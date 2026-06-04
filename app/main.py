import sys
import os
from pathlib import Path
import requests

import streamlit as st
from dotenv import load_dotenv

_PROJECT_ROOT = str(Path.cwd())
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))

# ── API Config ──
# Read API URL from env, or default to local FastAPI server
API_URL = os.getenv("API_URL", "http://localhost:8000/api/generate")

# ── Page Config ──
st.set_page_config(page_title="Crave AI Chef", page_icon="🍳", layout="centered")

st.title("🍳 Crave AI Recipe Generator")
st.write("Generate customized recipes based on what you have in your kitchen. Powered by Llama 3 via FastAPI.")

# ── Recipe Generation Form ──
with st.form("recipe_form"):
    st.subheader("What are you craving?")
    
    ingredients = st.text_input("Ingredients (e.g., chicken, rice, broccoli)", placeholder="What do you have?")
    
    col1, col2 = st.columns(2)
    with col1:
        cuisine = st.selectbox("Cuisine", ["Any", "Italian", "Indian", "Mexican", "Asian", "American", "Mediterranean"])
        time = st.selectbox("Cooking Time", ["Any", "Under 15 mins", "Under 30 mins", "Under 1 hour", "Take your time"])
    with col2:
        difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Medium", "Hard"])
        diet = st.selectbox("Dietary Preference", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"])
        
    special = st.text_area("Special Requests (Optional)", placeholder="e.g., Make it extra spicy, kid-friendly...")
    
    submitted = st.form_submit_button("Generate Recipes 🪄")

# ── Results Display ──
if submitted:
    if not ingredients.strip():
        st.warning("Please enter at least one ingredient!")
    else:
        with st.spinner("Chef Crave is brainstorming recipes for you..."):
            try:
                # Prepare payload for FastAPI
                payload = {
                    "ingredients": ingredients,
                    "diet": diet,
                    "cuisine": cuisine,
                    "time": time,
                    "difficulty": difficulty,
                    "special": special
                }
                
                # Make HTTP POST request to FastAPI backend
                response = requests.post(API_URL, json=payload, timeout=30)
                response.raise_for_status()
                
                raw_recipes = response.json()
                
                if raw_recipes:
                    st.success("Recipes generated successfully!")
                    
                    for r in raw_recipes:
                        name = r.get("name", "Delicious Recipe")
                        desc = r.get("description", "")
                        
                        st.markdown("---")
                        st.header(name)
                        st.write(f"*{desc}*")
                        
                        # Image URL is now provided directly by the API response
                        img_url = r.get("image_url")
                        if img_url:
                            st.image(img_url, width="stretch")
                            
                        # Quick stats
                        st.write(f"**Cuisine:** {r.get('cuisine', 'Custom')} | **Time:** {r.get('time', '30m')} | **Difficulty:** {r.get('difficulty', 'Medium')}")
                        st.write(f"**Nutrition:** {r.get('calories', '')} | Protein: {r.get('protein', '')} | Carbs: {r.get('carbs', '')} | Fat: {r.get('fat', '')}")
                        
                        col_ing, col_steps = st.columns([1, 2])
                        
                        with col_ing:
                            st.subheader("🛒 Ingredients")
                            for ing in r.get("ingredients", []):
                                st.write(f"- {ing}")
                                
                        with col_steps:
                            st.subheader("👨‍🍳 Instructions")
                            for i, step in enumerate(r.get("steps", []), 1):
                                st.write(f"**Step {i}:** {step}")
                                
                        if r.get("tip"):
                            st.info(f"**Chef's Tip:** {r.get('tip')}")
                        
                        # ── Feedback Form ──
                        with st.expander(f"Rate {name} ⭐"):
                            f_rating = st.slider("Rating (1-5)", 1, 5, 5, key=f"rate_{name}")
                            f_comment = st.text_input("Comment (optional)", key=f"com_{name}")
                            if st.button("Submit Feedback", key=f"btn_{name}"):
                                try:
                                    fb_payload = {
                                        "recipe_name": name,
                                        "rating": f_rating,
                                        "comment": f_comment
                                    }
                                    fb_url = API_URL.replace("/generate", "/feedback")
                                    fb_res = requests.post(fb_url, json=fb_payload, timeout=5)
                                    fb_res.raise_for_status()
                                    st.toast(f"Thank you for rating {name}!")
                                except Exception as e:
                                    st.error("Could not submit feedback at this time.")
                            
                else:
                    st.error("Failed to generate recipes. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to FastAPI backend. Is it running on http://localhost:8000 ?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
