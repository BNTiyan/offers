import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


load_dotenv()


@dataclass
class TwilioConfig:
    account_sid: str
    auth_token: str
    whatsapp_from: str
    whatsapp_to: str


@dataclass
class AppConfig:
    categories: List[str]
    max_offers_per_store: int
    twilio: TwilioConfig


def get_config() -> AppConfig:
    categories_raw = os.getenv(
        "CATEGORIES",
        "clothes,shoes,jackets,toys,kids toys",
    )
    categories = [c.strip().lower() for c in categories_raw.split(",") if c.strip()]

    max_offers = int(os.getenv("MAX_OFFERS_PER_STORE", "5"))

    twilio = TwilioConfig(
        account_sid=os.getenv("TWILIO_ACCOUNT_SID", "").strip(),
        auth_token=os.getenv("TWILIO_AUTH_TOKEN", "").strip(),
        whatsapp_from=os.getenv("TWILIO_WHATSAPP_FROM", "").strip(),
        whatsapp_to=os.getenv("TWILIO_WHATSAPP_TO", "").strip(),
    )

    return AppConfig(
        categories=categories,
        max_offers_per_store=max_offers,
        twilio=twilio,
    )


