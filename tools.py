import os
from groq import Groq
from dotenv import load_dotenv 
from utils.data_loader import load_listings

load_dotenv()

# Setup Groq client
ai_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
LLM_MODEL = "llama-3.3-70b-versatile"

def search_listings(description, size=None, max_price=None):
    listings = load_listings()
    results = []
    
    for item in listings:
        # Check if the price exceeds our limit
        if max_price is not None and item.get("price", float('inf')) > max_price:
            continue
            
        # Check if the size does not match
        if size is not None and item.get("size") != size:
            continue
            
        # Check if the description keyword is missing from both title and description
        title_match = description.lower() in item.get("title", "").lower()
        desc_match = description.lower() in item.get("description", "").lower()
        if not title_match and not desc_match:
            continue
            
        results.append(item)
        
    return results

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