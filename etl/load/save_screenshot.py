from db.config import get_connection
from prefect import task, get_run_logger
from uuid import UUID

@task(name="save screenshot path")
def save_screenshot(screenshot_path: str | None, domain_uuid: UUID):
    logger = get_run_logger()
    if not screenshot_path:
        logger.info("No screenshot skipping db write")
        return False
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           INSERT INTO etl.screenshot(domain_id, screenshot_path)
                           VALUES (%(domain_id)s,%(screenshot_path)s)
                        """, {"domain_id": domain_uuid, "screenshot_path": screenshot_path}
                        )
        conn.commit()
    return True
