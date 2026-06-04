import sys
import os
from pathlib import Path

# ── Resolve project root reliably for Streamlit ──
# Streamlit may not resolve __file__ correctly, so we walk up 
# from the current working directory (which is always the project root
# when launched via `streamlit run app/main.py` from the project dir).
_PROJECT_ROOT = str(Path.cwd())
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))

# Import the core logic
from src.llm.engine import generate_recipes as llm_generate_recipes
from src.utils.images import get_food_image

# ── Page Config ──
st.set_page_config(page_title="Crave AI Chef", page_icon="🍳", layout="centered")

st.title("🍳 Crave AI Recipe Generator")
st.write("Generate customized recipes based on what you have in your kitchen. Powered by Llama 3 & Unsplash.")

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
                raw_recipes = llm_generate_recipes(
                    ingredients=ingredients,
                    diet=diet if diet != "None" else "",
                    cuisine=cuisine if cuisine != "Any" else "",
                    time=time if time != "Any" else "",
                    difficulty=difficulty if difficulty != "Any" else "",
                    special=special
                )
                
                if raw_recipes:
                    st.success("Recipes generated successfully!")
                    
                    for r in raw_recipes:
                        name = r.get("name", "Delicious Recipe")
                        desc = r.get("description", "")
                        
                        st.markdown("---")
                        st.header(name)
                        st.write(f"*{desc}*")
                        
                        # Unsplash image
                        img_url = get_food_image(name)
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
                            
                else:
                    st.error("Failed to generate recipes. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.write("Hint: Make sure your GROQ_API_KEY is set correctly in Streamlit Secrets.")
