from typing import List
from .base import BaseScraper
from models import JobListing
from core.config import MAX_JOBS
from playwright.sync_api import TimeoutError
import random


class InfoJobsScraper(BaseScraper):
    BASE_URL = "https://www.infojobs.com.br/empregos.aspx"

    def search(self, keyword: str, location: str) -> List[JobListing]:
        url = f"{self.BASE_URL}?palabra={keyword}&provincia={location}"
        self.page.set_viewport_size({"width": 1176, "height": 664})
        self.page.goto(url)
        jobs = []

        btn = self.page.locator("#didomi-notice-agree-button")

        if btn.is_visible(timeout=3000):
            btn.click()
        # espera carregar os cards

        self.page.wait_for_selector("div.js_cardLink")

        cards = self.page.locator("div.js_cardLink")

        total = min(cards.count(), MAX_JOBS)

        for i in range(total):
            try:
                card = cards.nth(i)

                title = card.locator("h2").inner_text().strip()

                try:
                    company = card.locator("a.text-body").inner_text().strip()
                except TimeoutError:
                    company = "Não informado"

                try:
                    location_text = card.locator("div.mb-8").first.evaluate(
                        "el => el.childNodes[0].textContent"
                    ).strip()
                except TimeoutError:
                    location_text = "Não informado"

                url = card.locator("a").first.get_attribute("href")

                salary = card.locator("svg.icon-money").first.evaluate(
                    "el => el.parentElement.textContent"
                ).strip()

                # 👉 delay humano
                self.page.wait_for_timeout(random.randint(800, 1400))

                # 👉 clique no card (abre lateral)
                card.click()

                description = ''

                jobs.append(JobListing(
                    title=title,
                    company=company,
                    location=location_text,
                    url=url,
                    source="infojobs",
                    salary=salary,
                    description=description,
                ))

            except Exception as e:
                print(f"Erro InfoJobs: {e}")
                continue

        return jobs