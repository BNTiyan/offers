"""
Minimal Amazon example.

Amazon actively defends against scraping and frequently changes its HTML.
This module is a best-effort demo only; for production use, prefer official APIs or
affiliate feeds and always follow Amazon's Terms of Service.
"""

from typing import List

import requests
from bs4 import BeautifulSoup

from src.models import Offer


SEARCH_URL = "https://www.amazon.com/s"


def fetch_offers(categories: List[str]) -> List[Offer]:
    offers: List[Offer] = []

    query = " ".join(categories)
    params = {"k": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OfferNotifier/1.0; +https://example.com)",
        "Accept-Language": "en-US,en;q=0.9",
    }

    resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Amazon search results items
    product_elements = soup.select("div.s-main-slot div[data-component-type='s-search-result']")

    for el in product_elements[:30]:
        title_el = el.select_one("h2 a span")
        link_el = el.select_one("h2 a")
        price_whole_el = el.select_one("span.a-price span.a-offscreen")
        original_price_el = el.select_one("span.a-text-price span.a-offscreen")

        if not (title_el and link_el and price_whole_el):
            continue

        title = title_el.get_text(strip=True)
        url = link_el.get("href") or ""
        if url.startswith("/"):
            url = f"https://www.amazon.com{url}"

        currency = "$"

        def parse_price(text: str) -> float | None:
            # Amazon prices look like "$39.99"
            text = text.replace("$", "").replace(",", "").strip()
            try:
                return float(text.split()[0])
            except (ValueError, IndexError):
                return None

        discounted_price = parse_price(price_whole_el.get_text(strip=True))
        original_price = (
            parse_price(original_price_el.get_text(strip=True)) if original_price_el else None
        )

        offers.append(
            Offer(
                store="Amazon",
                title=title,
                original_price=original_price,
                discounted_price=discounted_price,
                currency=currency,
                url=url,
            )
        )

    return offers


