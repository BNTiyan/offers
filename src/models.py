from dataclasses import dataclass
from typing import Optional


@dataclass
class Offer:
    store: str
    title: str
    original_price: Optional[float]
    discounted_price: Optional[float]
    currency: str
    url: str

    @property
    def discount_percent(self) -> Optional[float]:
        if self.original_price and self.discounted_price:
            try:
                return round(
                    100.0 * (self.original_price - self.discounted_price) / self.original_price,
                    1,
                )
            except ZeroDivisionError:
                return None
        return None


