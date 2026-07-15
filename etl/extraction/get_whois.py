import whois
from whois.exceptions import WhoisError
from prefect import task, get_run_logger
from prefect.cache_policies import TASK_SOURCE, INPUTS
from model.whois_m import Whois
from model.domain import Domain

#caching the results for future lookups
@task(
    name="fetch whois records", 
    retries=2, retry_delay_seconds=5, 
    cache_policy=INPUTS + TASK_SOURCE
)
def fetch_whois(domain: Domain) -> Whois :
    logger = get_run_logger()
    try:
        resultat = whois.whois(domain.name)
        return Whois(**dict(resultat))
    except WhoisError:
        logger.error(f"Error ! | {WhoisError}")
        return None