from abc import ABC, abstractmethod
from typing import List
from playwright.sync_api import Page
from models import JobListing


class BaseScraper(ABC):
    def __init__(self, page: Page):
        self.page = page

    def wait_and_click(self, locator, timeout: int = 10000):
        locator.wait_for(state='visible', timeout=timeout)
        locator.click()

    @abstractmethod
    def search(self, keyword: str, location: str) -> List[JobListing]:
        """Cada scraper implementa sua própria lógica."""
        ...
