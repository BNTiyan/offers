## Offer Notifier – WhatsApp Deals from Major Stores

This project fetches **discounted offers** (original price, reduced price, link) from various shopping websites and **sends a WhatsApp message automatically** with the best deals.

Supported stores (scaffolded):
- Amazon
- Target
- Kohl's
- Macy's
- JCPenney
- Costco
- Walmart
- Tommy Hilfiger

> ⚠️ **Important**: Many sites restrict automated scraping in their Terms of Service. This project is structured to make it easy to plug in *official APIs or affiliate feeds* where available. The included HTML-scraping examples are for educational purposes and may need to be adapted or replaced with compliant integrations.

### 1. Features

- **Store abstraction**: each store has its own module that returns a list of standardized `Offer` objects.
- **Category filtering**: focus on clothes, shoes, jackets, toys, kids toys (configurable).
- **WhatsApp notifications**: send a formatted message with:
  - Original price
  - Discounted price
  - Product title
  - Link
- **Config-driven**: set everything via environment variables / `.env`.

### 2. Tech Stack

- **Language**: Python 3.10+
- **HTTP & parsing**: `requests`, `beautifulsoup4`
- **Scheduling**: simple CLI (can be wired to cron) or a loop
- **WhatsApp**: Twilio WhatsApp API (can be swapped out)

### 3. Setup

#### 3.1. Create and activate a virtual environment (recommended)

```bash
cd /Users/bhavananare/github/offers
python3 -m venv .venv
source .venv/bin/activate
```

#### 3.2. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example env file and edit the values:

```bash
cp env.example .env
```

Then open `.env` and set at least:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_FROM` (format: `whatsapp:+14155238886` or your approved Twilio sender)
- `TWILIO_WHATSAPP_TO` (format: `whatsapp:+<your_phone_number>`)

Optional:

- `CATEGORIES` – comma-separated list like `clothes,shoes,jackets,toys,kids toys`
- `MAX_OFFERS_PER_STORE` – integer, how many top offers to include from each store

### 5. Running the Script

Fetch offers once and send a WhatsApp message:

```bash
python -m src.main
```

This will:
- Call each configured store fetcher
- Normalize offers
- Build a single WhatsApp message containing the best offers
- Send it using Twilio

### 6. Scheduling (Cron Example)

To run this every morning at 8:00:

```bash
crontab -e
```

Add:

```bash
0 8 * * * cd /Users/bhavananare/github/offers && /Users/bhavananare/github/offers/.venv/bin/python -m src.main >> offer_notifier.log 2>&1
```

### 7. Extending Store Integrations

Each store lives under `src/stores/` and implements a `fetch_offers()` function that returns a list of `Offer` objects. The provided implementations are **minimal examples** and may break if the HTML structure changes.

To add/modify a store:
- Edit the corresponding file in `src/stores/`
- Adjust the HTML selectors or replace them with official APIs as needed

### 8. Disclaimer

- Use this code **at your own risk** and respect the Terms of Service of each website.
- Prefer **official APIs / affiliate feeds** rather than heavy HTML scraping.


