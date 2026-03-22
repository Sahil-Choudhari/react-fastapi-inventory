from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "mysql+mysqlconnector://root:xYz987%40%23%24@localhost:3306/pyapp"

engine = create_engine(db_url, echo=True)

session = sessionmaker(autoflush=False, bind=engine)

