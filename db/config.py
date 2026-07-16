import psycopg
from dotenv import load_dotenv
import os

load_dotenv()
def get_connection():
    return psycopg.Connection.connect(os.getenv("DATABASE_URL"))

