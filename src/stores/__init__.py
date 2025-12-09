"""Store-specific offer fetchers."""

from typing import List

from src.models import Offer

from . import (  # Add other stores here as they are implemented
    amazon,
    # costco,  # temporarily disabled
    # kate_spade,  # temporarily disabled
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
        # costco,  # temporarily disabled
        # kate_spade,  # temporarily disabled
        michael_kors,
        nike,
        nordstrom_rack,
        target,
        tory_burch,
        walmart,
    ):
        store_name = module.__name__.split(".")[-1]
        print(f"Fetching offers from {store_name}...")
        before = len(offers)
        try:
            offers.extend(module.fetch_offers(categories))
        except Exception as exc:  # noqa: BLE001
            # Fail-soft per store so one broken integration doesn't kill everything
            print(f"Error fetching offers from {module.__name__}: {exc}")
        after = len(offers)
        added = after - before
        print(f"Finished {store_name}: added {added} offers (total so far: {after}).")

    return offers


