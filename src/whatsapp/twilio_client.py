from typing import Iterable

from twilio.rest import Client

from src.models import Offer
from src.config import AppConfig


def build_message_text(offers: Iterable[Offer], max_per_store: int) -> str:
    offers_by_store = {}
    for offer in offers:
        offers_by_store.setdefault(offer.store, []).append(offer)

    lines: list[str] = []
    lines.append("🔥 Deals Roundup")
    lines.append("")

    for store, store_offers in offers_by_store.items():
        lines.append(f"== {store} ==")
        for offer in store_offers[:max_per_store]:
            discount_part = ""
            if offer.discount_percent is not None:
                discount_part = f" (-{offer.discount_percent}%)"

            price_part = ""
            if offer.original_price is not None and offer.discounted_price is not None:
                price_part = (
                    f"{offer.currency}{offer.discounted_price:.2f} "
                    f"(was {offer.currency}{offer.original_price:.2f}{discount_part})"
                )
            elif offer.discounted_price is not None:
                price_part = f"{offer.currency}{offer.discounted_price:.2f}"

            lines.append(f"- {offer.title}")
            if price_part:
                lines.append(f"  {price_part}")
            lines.append(f"  {offer.url}")
            lines.append("")

    if len(lines) == 2:
        return "No offers found for the configured categories."

    return "\n".join(lines).strip()


def send_whatsapp_message(config: AppConfig, offers: Iterable[Offer]) -> None:
    # Make Twilio truly optional: if credentials are missing, just skip sending.
    if not config.twilio.account_sid or not config.twilio.auth_token:
        print("Twilio credentials are not configured; skipping WhatsApp notification.")
        return

    message_text = build_message_text(offers, config.max_offers_per_store)

    client = Client(config.twilio.account_sid, config.twilio.auth_token)
    client.messages.create(
        body=message_text,
        from_=config.twilio.whatsapp_from,
        to=config.twilio.whatsapp_to,
    )


