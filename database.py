import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv('db_user')
password = os.getenv('db_password')

db_url = f'postgresql://{user}:{password}@localhost:5432/warehouse'
# Make sure database 'warehouse' is already present in the database
# SQLAlchemy uses the database, does not create it.

engine = create_engine(db_url)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
