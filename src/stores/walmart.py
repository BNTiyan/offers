"""
Minimal Walmart example.

Walmart heavily uses client-side rendering and APIs; this HTML-based example
may require adjustments or replacement with official APIs.
"""

from typing import List

import requests
from bs4 import BeautifulSoup

from src.models import Offer


SEARCH_URL = "https://www.walmart.com/search"


def fetch_offers(categories: List[str]) -> List[Offer]:
    offers: List[Offer] = []

    query = " ".join(categories)
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OfferNotifier/1.0; +https://example.com)"
    }

    resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Walmart often uses data-item-id and product-card-style elements.
    product_elements = soup.select("[data-item-id]")

    for el in product_elements[:30]:
        title_el = el.select_one("a[aria-label]")
        price_el = el.select_one("span[aria-hidden='true']")
        link_el = el.select_one("a[aria-label]")

        if not (title_el and price_el and link_el):
            continue

        title = title_el.get("aria-label") or title_el.get_text(strip=True)
        url = link_el.get("href") or ""
        if url.startswith("/"):
            url = f"https://www.walmart.com{url}"

        currency = "$"

        def parse_price(text: str) -> float | None:
            text = text.replace("$", "").replace(",", "").strip()
            try:
                return float(text.split()[0])
            except (ValueError, IndexError):
                return None

        discounted_price = parse_price(price_el.get_text(strip=True))

        offers.append(
            Offer(
                store="Walmart",
                title=title,
                original_price=None,  # not easily available from HTML list page
                discounted_price=discounted_price,
                currency=currency,
                url=url,
            )
        )

    return offers


