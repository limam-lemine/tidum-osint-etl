from db.config import get_connection
from model.domain import Domain
from uuid import UUID


def get_create_domain(domain: Domain) -> UUID:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM etl.domain WHERE name = %s", (domain.name,))
            res = cursor.fetchone()

            if res:
                return res[0]

            cursor.execute(
                "INSERT INTO etl.domain (name, classification) VALUES (%s, %s) RETURNING id",
                (domain.name, None),
            )
            res = cursor.fetchone()
            conn.commit()
            return res[0]