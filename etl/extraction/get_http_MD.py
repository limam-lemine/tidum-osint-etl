import httpx
from prefect import task, get_run_logger
from model.domain import Domain
from model.http_header import Header

@task(
    name="fetching http metadata",
    retries=3, 
    retry_delay_seconds=5
)
async def fetch_http_header(domain: Domain) -> Header:
    logger = get_run_logger()
    url = domain.name if domain.name.startswith(("http://","https://")) else f"https://{domain.name}"
    logger.info(f"fetching http header for {domain.name}")
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            result = await client.get(url)
            logger.info(f"response {result.status_code}")
            return Header(**dict(result.headers), final_url=str(result.url), nbr_redirection=len(result.history))
    except httpx.HTTPError as e:
        logger.error(f"failed! | {e}")
        raise
    