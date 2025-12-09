"""
Minimal Nike example.

Nike uses modern frontend tech and may change layouts; treat these selectors as
initial guesses.
"""

from typing import List

import requests
from bs4 import BeautifulSoup

from src.models import Offer


SEARCH_URL = "https://www.nike.com/w"


def fetch_offers(categories: List[str]) -> List[Offer]:
    offers: List[Offer] = []

    # Nike's browsing is category-based; we approximate by using a text query param.
    query = " ".join(categories)
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OfferNotifier/1.0; +https://example.com)"
    }

    resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    product_elements = soup.select("div.product-card, div.product-grid__items div.product-card")

    for el in product_elements[:30]:
        title_el = el.select_one("a.product-card__link-overlay, a.product-card__title")
        price_el = el.select_one(".product-price, .product-card__price")
        was_price_el = el.select_one(".product-price--was, .product-card__price--strikethrough")
        link_el = el.select_one("a[href]")

        if not (title_el and link_el):
            continue

        title = title_el.get_text(strip=True)
        url = link_el.get("href") or ""
        if url.startswith("/"):
            url = f"https://www.nike.com{url}"

        currency = "$"

        def parse_price(text: str) -> float | None:
            text = text.replace("$", "").replace(",", "").strip()
            try:
                # Nike sometimes shows ranges like "$80 - $120"; take the first part.
                return float(text.split()[0])
            except (ValueError, IndexError):
                return None

        discounted_price = parse_price(price_el.get_text(strip=True)) if price_el else None
        original_price = parse_price(was_price_el.get_text(strip=True)) if was_price_el else None

        offers.append(
            Offer(
                store="Nike",
                title=title,
                original_price=original_price,
                discounted_price=discounted_price,
                currency=currency,
                url=url,
            )
        )

    return offers


