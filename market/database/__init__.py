from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata

engine = create_engine(settings.postgres_dsn)
Session = sessionmaker(bind=engine)
