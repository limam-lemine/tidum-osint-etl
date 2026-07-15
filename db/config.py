import psycopg
from dotenv import load_dotenv
import os

load_dotenv()
async def get_connection():
    return await psycopg.AsyncClientCursor.connect(os.getenv("DATABASE_URL"))

