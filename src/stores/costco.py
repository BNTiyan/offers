"""
Minimal Costco example.

Costco's site structure can change; this HTML-based demo may need updates.
Prefer official APIs / feeds where available and respect Costco's Terms of Use.
"""

from typing import List

import requests
from bs4 import BeautifulSoup

from src.models import Offer


SEARCH_URL = "https://www.costco.com/CatalogSearch"


def fetch_offers(categories: List[str]) -> List[Offer]:
    offers: List[Offer] = []

    query = " ".join(categories)
    params = {"keyword": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OfferNotifier/1.0; +https://example.com)"
    }

    resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Costco product tiles often use the "product" class.
    product_elements = soup.select(".product")

    for el in product_elements[:30]:
        title_el = el.select_one(".description a")
        price_el = el.select_one(".price, .price .value")
        link_el = el.select_one(".description a")

        if not (title_el and link_el):
            continue

        title = title_el.get_text(strip=True)
        url = link_el.get("href") or ""
        if url.startswith("/"):
            url = f"https://www.costco.com{url}"

        currency = "$"

        def parse_price(text: str) -> float | None:
            text = text.replace("$", "").replace(",", "").strip()
            try:
                return float(text.split()[0])
            except (ValueError, IndexError):
                return None

        discounted_price = parse_price(price_el.get_text(strip=True)) if price_el else None

        offers.append(
            Offer(
                store="Costco",
                title=title,
                original_price=None,  # list pages typically show current price only
                discounted_price=discounted_price,
                currency=currency,
                url=url,
            )
        )

    return offers


