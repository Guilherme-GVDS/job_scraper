from typing import List
from .base import BaseScraper
from models import JobListing
from core.config import MAX_JOBS
from playwright.sync_api import TimeoutError


class CathoScraper(BaseScraper):
    BASE_URL = 'https://www.catho.com.br/vagas/'

    def search(self, keyword: str, location: str) -> List[JobListing]:
        url = f'{self.BASE_URL}?q={keyword}&where={location}'

        self.page.goto(url)
        jobs = []

        # botão "Agora não"
        button = self.page.get_by_role('button', name='Agora não')
        if button.is_visible(timeout=2000):
            button.click()

        # cookies
        cookie_btn = self.page.get_by_role(
            'button',
            name='Aceitar todos os cookies'
        )
        if cookie_btn.is_visible(timeout=2000):
            cookie_btn.click()

        cards = self.page.locator(
            'ul.search-result-custom_jobList__lVIvI li'
        )

        for i in range(min(cards.count(), MAX_JOBS)):
            try:
                card = cards.nth(i)

                try:
                    title = card.locator(
                        'h2.Title-module__title___3S2cv'
                    ).inner_text().strip()

                except TimeoutError:
                    title = 'Não informado'

                try:
                    company = card.locator('p.sc-bDumWk').first.evaluate(
                        "el => el.childNodes[0].textContent"
                    ).strip()

                except TimeoutError:
                    company = 'Não informado'

                try:
                    location_text = card.locator(
                        'a'
                    ).nth(1).inner_text().strip()
                    location_text = location_text.split('(')[0].strip()

                except TimeoutError:
                    location_text = 'Não informado'

                url = card.locator('a').first.get_attribute('href')

                try:
                    salary = card.locator(
                        'div.custom-styled_salaryText__oSvPo'
                    ).inner_text().strip()

                except TimeoutError:
                    salary = 'Não informado'

                description = ''

                jobs.append(JobListing(
                    title=title,
                    company=company,
                    location=location_text,
                    url=url,
                    source='catho',
                    salary=salary,
                    description=description,
                ))

            except Exception as e:
                print(f'Erro Catho: {e}')
                continue

        return jobs
