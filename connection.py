from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
# read from db from environment variable

load_dotenv()

database_url = os.getenv('DATABASE_URL')

print(database_url)
engine = create_engine(database_url)

# engine = create_engine("postgresql://team_pokin:pokin5432!@34.128.115.20/batikpedia")

session = Session(engine)
