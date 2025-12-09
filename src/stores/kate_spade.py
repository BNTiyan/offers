"""
Minimal Kate Spade example.

Selectors are approximate and may need tuning over time.
"""

from typing import List, Set

import requests
from bs4 import BeautifulSoup

from src.models import Offer


SEARCH_URL = "https://www.katespade.com/search"


def fetch_offers(categories: List[str]) -> List[Offer]:
    offers: List[Offer] = []
    seen_urls: Set[str] = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OfferNotifier/1.0; +https://example.com)"
    }

    for category in categories:
        search_terms = {
            category,
            f"{category} sale",
            f"{category} clearance",
            f"{category} deals",
        }

        for term in search_terms:
            params = {"q": term}

            resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=15)
            print(f"  [Kate Spade] term='{term}' url={resp.url}")
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")

            product_elements = soup.select(".product-tile, .product-grid__item")

            for el in product_elements[:30]:
                title_el = el.select_one(".product-name, .product-tile__name")
                price_el = el.select_one(".product-sales-price, .product-price")
                was_price_el = el.select_one(".product-standard-price, .product-price--was")
                link_el = el.select_one("a[href]")

                if not (title_el and link_el):
                    continue

                title = title_el.get_text(strip=True)
                url = link_el.get("href") or ""
                if url.startswith("/"):
                    url = f"https://www.katespade.com{url}"

                if url in seen_urls:
                    continue
                seen_urls.add(url)

                currency = "$"

                def parse_price(text: str) -> float | None:
                    text = text.replace("$", "").replace(",", "").strip()
                    try:
                        return float(text.split()[0])
                    except (ValueError, IndexError):
                        return None

                discounted_price = parse_price(price_el.get_text(strip=True)) if price_el else None
                original_price = (
                    parse_price(was_price_el.get_text(strip=True)) if was_price_el else None
                )

                offers.append(
                    Offer(
                        store="Kate Spade",
                        title=title,
                        original_price=original_price,
                        discounted_price=discounted_price,
                        currency=currency,
                        url=url,
                    )
                )

    return offers


