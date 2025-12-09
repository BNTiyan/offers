"""
Very minimal example for Target.

This is intentionally simple and may need adjustment if Target's HTML changes.
Prefer using official APIs / feeds if available.
"""

from typing import List

import requests
from bs4 import BeautifulSoup

from src.models import Offer


SEARCH_URL = "https://www.target.com/s"


def fetch_offers(categories: List[str]) -> List[Offer]:
    offers: List[Offer] = []

    # Use a single broad keyword search across categories for demo purposes
    query = " OR ".join(categories)
    params = {"searchTerm": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OfferNotifier/1.0; +https://example.com)"
    }

    resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Target often uses data-test attributes for product tiles. This is a best-effort selector.
    product_elements = soup.select("[data-test='product-grid'] [data-test='list-entry-product-card']")

    for el in product_elements[:30]:
        title_el = el.select_one("[data-test='product-title']")
        price_el = el.select_one("[data-test='current-price']")
        was_price_el = el.select_one("[data-test='was-price']")
        link_el = el.select_one("a")

        if not (title_el and price_el and link_el):
            continue

        title = title_el.get_text(strip=True)
        url = link_el.get("href") or ""
        if url.startswith("/"):
            url = f"https://www.target.com{url}"

        currency = "$"

        def parse_price(text: str) -> float | None:
            text = text.replace("$", "").replace(",", "").strip()
            try:
                return float(text.split()[0])
            except (ValueError, IndexError):
                return None

        discounted_price = parse_price(price_el.get_text(strip=True))
        original_price = parse_price(was_price_el.get_text(strip=True)) if was_price_el else None

        offers.append(
            Offer(
                store="Target",
                title=title,
                original_price=original_price,
                discounted_price=discounted_price,
                currency=currency,
                url=url,
            )
        )

    return offers


