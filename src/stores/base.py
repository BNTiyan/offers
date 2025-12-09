from abc import ABC, abstractmethod
from typing import List

from src.models import Offer


class BaseStoreFetcher(ABC):
    name: str

    @abstractmethod
    def fetch_offers(self, categories: List[str]) -> List[Offer]:
        """Return a list of offers for the given categories."""


