from email.message import EmailMessage
from typing import Iterable
import smtplib
import ssl

from src.config import AppConfig
from src.models import Offer
from src.whatsapp.twilio_client import build_message_text


def send_email_message(config: AppConfig, offers: Iterable[Offer]) -> None:
    if not config.email.smtp_host or not config.email.email_from or not config.email.email_to:
        raise RuntimeError("Email SMTP settings are not fully configured.")

    body = build_message_text(offers, config.max_offers_per_store)

    msg = EmailMessage()
    msg["Subject"] = "Deals Roundup"
    msg["From"] = config.email.email_from
    msg["To"] = config.email.email_to
    msg.set_content(body)

    context = ssl.create_default_context()

    if config.email.use_tls:
        with smtplib.SMTP(config.email.smtp_host, config.email.smtp_port) as server:
            server.starttls(context=context)
            if config.email.username and config.email.password:
                server.login(config.email.username, config.email.password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(config.email.smtp_host, config.email.smtp_port) as server:
            if config.email.username and config.email.password:
                server.login(config.email.username, config.email.password)
            server.send_message(msg)


