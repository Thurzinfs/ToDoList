from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DECLATARIVE_URL = 'sqlite:///db.db'

engine = create_engine(DECLATARIVE_URL)

sessionlocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

base = declarative_base()

def get_session():
    session = sessionlocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()