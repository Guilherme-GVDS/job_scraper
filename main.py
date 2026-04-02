from output.excel_exporter import export_to_excel
from playwright_client import PlaywrightClient
# from scrapers.linkedin import LinkedInScraper
# from scrapers.catho import CathoScraper
from scrapers.infojobs import InfoJobsScraper
# from scrapers.indeed import IndeedScraper

SCRAPERS = [InfoJobsScraper]


def run(keyword: str, location: str):
    all_jobs = []

    with PlaywrightClient(headless=False) as client:
        for ScraperClass in SCRAPERS:
            scraper = ScraperClass(client.page)
            jobs = scraper.search(keyword, location)
            all_jobs.extend(jobs)

    export_to_excel(all_jobs)
    return all_jobs


if __name__ == "__main__":
    vagas = run("Desenvolvedor", "São Paulo")
