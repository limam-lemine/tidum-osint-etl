from playwright.async_api import async_playwright
from model.domain import Domain
from prefect import task, get_run_logger
from pathlib import Path
from datetime import datetime

@task(name="take screenshot")
async def take_screenshot(domain: Domain, store_folder) -> str | None :
    logger = get_run_logger()

    Path(store_folder).mkdir(parents=True, exist_ok=True)

    tmp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{domain.name}_{tmp}.png"
    full_path = str(Path(store_folder) /filename) #create a folder to store screenshots

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page(
                viewport={"width": 1920, "height": 1080}
            )
            url = f"http://{domain.name}"
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(3000) # wait untill js render
            await page.screenshot(
                path=full_path,
                full_page=True
            )
            logger.info(f"screenshot done !!")
            return full_path
        except Exception as e:
            logger.error(f"screenshot faild !! | {e}")
            return None
        finally:
            await browser.close()
