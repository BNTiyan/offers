from src.config import get_config
from src.stores import fetch_all_offers
from src.whatsapp.twilio_client import send_whatsapp_message


def main() -> None:
    config = get_config()

    offers = fetch_all_offers(config.categories)
    if not offers:
        print("No offers found; not sending WhatsApp message.")
        return

    print(f"Fetched {len(offers)} offers. Sending WhatsApp message...")
    send_whatsapp_message(config, offers)
    print("WhatsApp message sent.")


if __name__ == "__main__":
    main()


