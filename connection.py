from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("postgresql://team_pokin:pokin5432!@34.128.115.20/batikpedia")

session = Session(engine)
