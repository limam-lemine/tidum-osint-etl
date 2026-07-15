from prefect import flow
import asyncio
from uuid import UUID

from load.load_dns_records import save_dns_records
from load.load_http_md import save_http_metadata
from load.load_whois_lookup import save_whois_records

from extraction.get_dns import fetch_dns_records
from extraction.get_http_MD import fetch_http_header
from extraction.get_whois import fetch_whois
from model.domain import Domain

@flow(name="main flow", retries=2, retry_delay_seconds=2)
async def main_flow(domain_id: UUID, domain: Domain):

    dns_records, http_md = await asyncio.gather(fetch_dns_records(domain), fetch_http_header(domain))
    whois = fetch_whois(domain)

    await asyncio.gather(
        save_dns_records(domain_id, dns_records),
        save_http_metadata(domain_id, http_md),
        save_whois_records(domain_id, whois)
    )


#the entrypoint to start the flow 
async def start_flow(domain_id: UUID, domain: Domain):
    asyncio.run(main_flow(domain_id, domain))


