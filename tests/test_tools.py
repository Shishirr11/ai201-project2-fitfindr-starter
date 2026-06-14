from tools import search_listings, suggest_outfit, create_fit_card

def test_search_returns_results():
    results = search_listings("tee", size=None, max_price=100)
    assert isinstance(results, list)

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=25)
    assert all(item["price"] <= 25 for item in results)

def test_suggest_outfit_empty_wardrobe():
    result = suggest_outfit({"title": "Cool Jacket"}, {"items": []})
    assert "empty" in result or "basics" in result

def test_create_fit_card_empty_outfit():
    result = create_fit_card("", {"title": "Vintage Tee", "price": 20})
    assert "Still figuring out" in result