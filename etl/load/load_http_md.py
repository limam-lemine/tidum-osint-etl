from db.config import get_connection
from prefect import task
from model.http_header import Header
from uuid import UUID

@task(description="load http metadata into db", retries=2, retry_delay_seconds=2)
async def save_http_metadata(domain_id: UUID, header: Header):
    #we convert pydantic object to a dict with .model_dump
    #so psycopg can parse it automatically
    data = Header.model_dump()

    #foreign key     
    data["domain_id"] = domain_id

    async with await get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("""
                INSERT INTO etl.http_metadata (
                    domain_id, location, content_type, content_security_policy_report_only, 
                    response_date, expires, cache_control, server, content_length, 
                    x_xss_protection, x_frame_options, alt_svc, final_url, nbr_redirection
                )
                VALUES (
                    %(domain_id)s, %(location)s, %(content_type)s, %(content_security_policy_report_only)s, 
                    %(date)s, %(expires)s, %(cache_control)s, %(server)s, %(content_length)s, 
                    %(x_xss_protection)s, %(x_frame_options)s, %(alt_svc)s, %(final_url)s, %(nbr_redirection)s
                )
                ON CONFLICT (domain_id) DO UPDATE SET
                    location = EXCLUDED.location,
                    content_type = EXCLUDED.content_type,
                    content_security_policy_report_only = EXCLUDED.content_security_policy_report_only,
                    response_date = EXCLUDED.response_date,
                    expires = EXCLUDED.expires,
                    cache_control = EXCLUDED.cache_control,
                    server = EXCLUDED.server,
                    content_length = EXCLUDED.content_length,
                    x_xss_protection = EXCLUDED.x_xss_protection,
                    x_frame_options = EXCLUDED.x_frame_options,
                    alt_svc = EXCLUDED.alt_svc,
                    final_url = EXCLUDED.final_url,
                    nbr_redirection = EXCLUDED.nbr_redirection;
            """, data)