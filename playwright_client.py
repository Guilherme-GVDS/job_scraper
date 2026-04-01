from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from typing import Optional


class PlaywrightClient:
    """Client Playwright reutilizável em formato de classe."""

    def __init__(
        self,
        browser_type: str = "chromium",
        headless: bool = True,
        slow_mo: int = 0,
    ):
        self.browser_type = browser_type
        self.headless = headless
        self.slow_mo = slow_mo

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    # ── Ciclo de vida ──────────────────────────────────────────────

    def start(self) -> "PlaywrightClient":
        """Inicia o Playwright e abre o browser."""
        self._playwright = sync_playwright().start()
        launcher = getattr(self._playwright, self.browser_type)
        self._browser = launcher.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        return self

    def stop(self) -> None:
        """Fecha tudo na ordem correta."""
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    # ── Context manager ───────────────────────────────────────────

    def __enter__(self) -> "PlaywrightClient":
        return self.start()

    def __exit__(self, *_) -> None:
        self.stop()

    # ── Propriedades de acesso ─────────────────────────────────────

    @property
    def page(self) -> Page:
        if not self._page:
            raise RuntimeError("Client não iniciado. Use .start() ou `with`.")
        return self._page

    @property
    def context(self) -> BrowserContext:
        if not self._context:
            raise RuntimeError("Client não iniciado. Use .start() ou `with`.")
        return self._context

    # ── Helpers de navegação ───────────────────────────────────────

    def goto(self, url: str, wait_until: str = "networkidle") -> None:
        self.page.goto(url, wait_until=wait_until)

    def new_page(self) -> Page:
        """Abre uma nova aba e a define como página ativa."""
        self._page = self._context.new_page()
        return self._page

    def screenshot(self, path: str, full_page: bool = True) -> None:
        self.page.screenshot(path=path, full_page=full_page)

    def get_text(self, selector: str) -> str:
        return self.page.inner_text(selector)

    def click(self, selector: str) -> None:
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)

    def wait_for(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)
