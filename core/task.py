from patchright.async_api import async_playwright, Page, Response
from aioconsole import ainput
from config import Config
from loguru import logger


class Task:
    def __init__(self):
        self.page: Page = None

    async def find_node(
        self,
        xpath: str,
        timeout: int = Config.patchright.node_timeout,
        state: str = "visible",
    ):
        locator = self.page.locator(f"xpath={xpath}")
        try:
            await locator.wait_for(timeout=timeout * 1000, state=state)
        except Exception:
            return None
        return locator

    async def visit(self, url):
        try:
            await self.page.goto(url, timeout=Config.patchright.page_timeout * 1000)
            return None
        except Exception:
            return f"visit {url} timeout"

    async def login(self):
        err = await self.visit("https://github.com/login")
        if err:
            return err

        await ainput("After login, press Enter to continue...")

        pages = self.page.context.pages
        for index, page in enumerate(pages):
            if index != 0:
                await page.close()
        self.page = pages[0]
        return None

    async def response(self, response: Response):
        pass

    async def logic(self):
        # TODO: 添加逻辑
        self.page.on("response", self.response)

        err = await self.login()
        if err:
            return f"login | {err}"

        return None

    async def init_patchright(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch_persistent_context(
                bypass_csp=True,
                no_viewport=True,
                executable_path=Config.patchright.chrome_path,
                headless=Config.patchright.headless,
                user_data_dir=f"./assets/{Config.patchright.port}",
                ignore_default_args=[
                    "--disable-field-trial-config",
                    "--disable-background-networking",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-breakpad",
                    "--disable-dev-shm-usage",
                    "--disable-features=AcceptCHFrame,AutoExpandDetailsElement,AvoidUnnecessaryBeforeUnloadCheckSync,CertificateTransparencyComponentUpdater,DeferRendererTasksAfterInput,DestroyProfileOnBrowserClose,DialMediaRouteProvider,ExtensionManifestV2Disabled,GlobalMediaControls,HttpsUpgrades,ImprovedCookieControls,LazyFrameLoading,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,Translate",
                    "--disable-hang-monitor",
                    "--disable-prompt-on-repost",
                    "--disable-renderer-backgrounding",
                    "--force-color-profile=srgb",
                    "--password-store=basic",
                    "--use-mock-keychain",
                    "--export-tagged-pdf",
                    "--disable-search-engine-choice-screen",
                    "--disable-blink-features=AutomationControlled",
                    "--flag-switches-begin",
                    "--flag-switches-end",
                    "about:blank",
                    "--no-sandbox",
                    "--enable-automation",
                ],
            )
            self.page = browser.pages[0]

            err = await self.logic()
            return err

    async def start(self):
        err = await self.init_patchright()
        if err:
            logger.error(err)
            return
