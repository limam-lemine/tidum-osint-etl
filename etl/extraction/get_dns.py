import dns.asyncresolver
import dns.resolver
from prefect import task, flow
from model.domain import Domain
from model.dns_records import DnsRecords
from prefect.cache_policies import INPUTS, TASK_SOURCE
import asyncio

@task(
        retries=2,
        retry_delay_seconds=5, 
        name="dns lookup", 
        cache_policy=INPUTS + TASK_SOURCE
)
async def lookup(domain: Domain, record_type: str): 
    try:
        answers = await dns.asyncresolver.resolve(domain.name, record_type)
        return [ str(record) for record in answers]
    except dns.resolver.NoAnswer:
        return []
    except dns.resolver.NXDOMAIN: #query name doesn't exist
        return None
    except dns.resolver.LifetimeTimeout:
        raise #prefect will retry the query

@flow(name="fetch dns records")
async def fetch_dns_records(domain: Domain) -> DnsRecords:
    record_type = ["A","AAAA","NS","TXT","MX","CNAME"]
    tasks = [lookup(domain, rt) for rt in record_type]
    results = await asyncio.gather(*tasks, return_exceptions=True) #return_exceptions=True : if a record fail the execution continues
    res = dict(zip(record_type, results))
    
    return DnsRecords(domain_name=domain.name,**res)
