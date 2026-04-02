import random
from typing import List
from .base import BaseScraper
from models import JobListing
from core.config import MAX_JOBS


class LinkedInScraper(BaseScraper):
    BASE_URL = 'https://www.linkedin.com/jobs/search'

    def search(self, keyword: str, location: str) -> List[JobListing]:
        self.page.goto(
            f'{self.BASE_URL}?keywords={keyword}&location={location}'
        )

        try:
            self.page.get_by_role('button', name='Fechar').click()
        except TimeoutError:
            pass

        # Aplica o filtro 'Última semana'
        self.wait_and_click(self.page.get_by_role(
            'button',
            name='a qualquer momento')
        )
        self.wait_and_click(self.page.get_by_text('Última semana'))
        self.wait_and_click(self.page.get_by_role('button', name='Concluído'))

        jobs = []
        cards = self.page.locator('ul.jobs-search__results-list li')
        for i in range(min(cards.count(), MAX_JOBS)):
            try:
                card = cards.nth(i)

                title = card.locator(
                    'h3.base-search-card__title'
                ).inner_text().strip()
                company = card.locator(
                    'h4.base-search-card__subtitle a'
                ).inner_text().strip()
                location_text = card.locator(
                    'span.job-search-card__location'
                ).inner_text().strip()
                url = card.locator(
                    'a.base-card__full-link'
                ).get_attribute('href')

                # delay humano
                self.page.wait_for_timeout(random.randint(1200, 1700))

                card.locator('a.base-card__full-link').click()

                self.page.wait_for_selector('div.show-more-less-html__markup')

                description = self.page.locator(
                    'div.show-more-less-html__markup'
                ).inner_text().strip()

                jobs.append(JobListing(
                    title=title,
                    company=company,
                    location=location_text,
                    url=url,
                    source='linkedin',
                    description=description,
                ))

            except Exception as e:
                print(f'Erro ao extrair card: {e}')
                continue
        return jobs
