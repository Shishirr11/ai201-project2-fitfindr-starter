import os
from groq import Groq
from dotenv import load_dotenv 
from utils.data_loader import load_listings
from typing import Optional

load_dotenv()

# Setup Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

def search_listings(
    description: str,
    size:Optional[str] = None,
    max_price: Optional[float] = None,
) -> list[dict]:
    listings = load_listings()
    scored_results = []
    
    # Clean up the description to find keywords
    search_words = set(description.lower().split())

    for item in listings:
        # Filter by price
        if max_price is not None and item.get("price", float('inf')) > max_price:
            continue
            
        # Filter by size (case-insensitive substring match as per docstring)
        if size is not None:
            item_size = item.get("size", "").lower()
            if size.lower() not in item_size:
                continue

        # Score by keyword overlap in title and description
        score = 0
        text_to_search = (item.get("title", "") + " " + item.get("description", "")).lower()
        
        for word in search_words:
            if word in text_to_search:
                score += 1
                
        # Drop items with 0 score, otherwise keep them
        if score > 0:
            scored_results.append({"item": item, "score": score})

    # Sort highest score first and return just the dictionaries
    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return [result["item"] for result in scored_results]

def suggest_outfit(new_item, wardrobe):
    # Graceful failure mode for an empty wardrobe
    if not wardrobe or not wardrobe.get("items"):
        return "Your wardrobe is currently empty! Try pairing this piece with universal basics like classic blue jeans or a simple white tee."
    
    prompt = f"I just thrifted this item: {new_item}. Here is my current wardrobe: {wardrobe}. Suggest one complete outfit combination."
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    return response.choices[0].message.content

def create_fit_card(outfit, new_item):
    # Graceful failure mode for a missing outfit string
    if not outfit:
        return f"Just scored this {new_item.get('title')} for ${new_item.get('price')}! Still figuring out how to style it."
        
    prompt = f"Turn this styling advice into a short, punchy social media caption with emojis. Advice: {outfit}. Item: {new_item}"
    
    # Higher temperature ensures the captions vary on each run
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content