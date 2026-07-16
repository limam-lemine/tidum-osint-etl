from db.config import get_connection
from prefect import task
from model.dns_records import DnsRecords
from uuid import UUID 

@task(description="load dns records into db", retries=2, retry_delay_seconds=2)
def save_dns_records(domain_id: UUID, dnsRecords: DnsRecords):
    #we convert pydantic object to a dict with .model_dump
    #so psycopg can parse it automatically
    data = dnsRecords.model_dump()

    #Foreign key 
    data["domain_id"] = domain_id
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO etl.dns_records(domain_id,a,aaaa,ns,txt,cname)
                           VALUES(%(domain_id)s,%(a)s,%(aaaa)s,%(ns)s,%(txt)s,%(cname)s)
                           ON CONFLICT (domain_id) DO UPDATE SET
                                a = EXCLUDED.a, 
                                aaaa = EXCLUDED.aaaa, 
                                ns = EXCLUDED.ns, 
                                txt = EXCLUDED.txt, 
                                cname = EXCLUDED.cname; 
                            """, data)
    
    
    
    
    