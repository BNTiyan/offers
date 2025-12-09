"""Store-specific offer fetchers."""

from typing import List

from src.models import Offer

from . import (  # Add other stores here as they are implemented
    amazon,
    costco,
    kate_spade,
    michael_kors,
    nike,
    nordstrom_rack,
    target,
    tory_burch,
    walmart,
)


def fetch_all_offers(categories: List[str]) -> List[Offer]:
    """
    Fetch offers from all supported stores for the given categories.

    Each store module should export a `fetch_offers(categories: List[str]) -> List[Offer]`.
    """
    offers: List[Offer] = []

    for module in (
        amazon,
        costco,
        kate_spade,
        michael_kors,
        nike,
        nordstrom_rack,
        target,
        tory_burch,
        walmart,
    ):
        try:
            offers.extend(module.fetch_offers(categories))
        except Exception as exc:  # noqa: BLE001
            # Fail-soft per store so one broken integration doesn't kill everything
            # In a real system, log this instead of printing.
            print(f"Error fetching offers from {module.__name__}: {exc}")

    return offers


