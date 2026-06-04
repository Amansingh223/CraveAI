from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from pathlib import Path

# Add project root to sys.path so 'src' module can be imported properly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.llm.engine import generate_recipes
from src.utils.images import get_food_image

app = FastAPI(
    title="CraveAI Backend API",
    description="API for generating recipes using Llama 3 via Groq",
    version="1.0.0"
)

# Pydantic models for request and response validation
class RecipeRequest(BaseModel):
    ingredients: str
    diet: Optional[str] = "None"
    cuisine: Optional[str] = "Any"
    time: Optional[str] = "Any"
    difficulty: Optional[str] = "Any"
    special: Optional[str] = ""

class RecipeResponse(BaseModel):
    name: str
    description: str
    cuisine: str
    time: str
    difficulty: str
    calories: str
    servings: str
    protein: str
    carbs: str
    fat: str
    ingredients: List[str]
    steps: List[str]
    tip: str
    image_url: Optional[str] = None

@app.post("/api/generate", response_model=List[RecipeResponse])
async def api_generate_recipes(request: RecipeRequest):
    try:
        # Generate raw recipe JSON array using the LLM engine
        diet_list = [request.diet] if request.diet and request.diet != "None" else []
        
        raw_recipes = generate_recipes(
            ingredients=request.ingredients,
            diet=diet_list,
            cuisine=request.cuisine if request.cuisine != "Any" else "",
            time=request.time if request.time != "Any" else "",
            difficulty=request.difficulty if request.difficulty != "Any" else "",
            special=request.special
        )
        
        if not raw_recipes:
            raise HTTPException(status_code=500, detail="LLM failed to generate recipes")
            
        # Post-process to add image URLs before returning to frontend
        for recipe in raw_recipes:
            recipe_name = recipe.get("name", "")
            if recipe_name:
                recipe["image_url"] = get_food_image(recipe_name)
                
        return raw_recipes

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "ok", "message": "CraveAI API is running"}
