from db.config import get_connection
from prefect import task
from model.whois_m import Whois
from uuid import UUID

@task(description="load whois lookup records into db", retries=2, retry_delay_seconds=2)
def save_whois_records(domain_id: UUID, whois_record: Whois):
    data = whois_record.model_dump()
    
    data["domain_id"] = domain_id

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO etl.whois_lookup (
                    domain_id, registrar, registrar_url, reseller, whois_server, referral_url,
                    updated_date, creation_date, expiration_date, name_servers, status, emails,
                    dnssec, name, org, address, city, state, registrant_postal_code, country,
                    tech_name, tech_org, admin_name, admin_org
                )
                VALUES (
                    %(domain_id)s, %(registrar)s, %(registrar_url)s, %(reseller)s, %(whois_server)s, %(referral_url)s,
                    %(updated_date)s, %(creation_date)s, %(expiration_date)s, %(name_servers)s, %(status)s, %(emails)s,
                    %(dnssec)s, %(name)s, %(org)s, %(address)s, %(city)s, %(state)s, %(registrant_postal_code)s, %(country)s,
                    %(tech_name)s, %(tech_org)s, %(admin_name)s, %(admin_org)s
                )
                ON CONFLICT (domain_id) DO UPDATE SET
                    registrar = EXCLUDED.registrar,
                    registrar_url = EXCLUDED.registrar_url,
                    reseller = EXCLUDED.reseller,
                    whois_server = EXCLUDED.whois_server,
                    referral_url = EXCLUDED.referral_url,
                    updated_date = EXCLUDED.updated_date,
                    creation_date = EXCLUDED.creation_date,
                    expiration_date = EXCLUDED.expiration_date,
                    name_servers = EXCLUDED.name_servers,
                    status = EXCLUDED.status,
                    emails = EXCLUDED.emails,
                    dnssec = EXCLUDED.dnssec,
                    name = EXCLUDED.name,
                    org = EXCLUDED.org,
                    address = EXCLUDED.address,
                    city = EXCLUDED.city,
                    state = EXCLUDED.state,
                    registrant_postal_code = EXCLUDED.registrant_postal_code,
                    country = EXCLUDED.country,
                    tech_name = EXCLUDED.tech_name,
                    tech_org = EXCLUDED.tech_org,
                    admin_name = EXCLUDED.admin_name,
                    admin_org = EXCLUDED.admin_org;
            """, data)