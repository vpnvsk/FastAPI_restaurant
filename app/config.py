from dotenv import load_dotenv
import os


load_dotenv()

POSTGRES_USER=os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB=os.environ.get('POSTGRES_DB')
SECRET = os.environ.get('SECRET')
DB_HOST = os.environ.get('DB_HOST')


