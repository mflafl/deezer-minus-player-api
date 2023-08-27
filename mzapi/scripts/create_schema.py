from sqlalchemy import create_engine

from mzapi.models.base import Base

engine = create_engine('postgresql+psycopg://postgres@localhost:5433/mzapi', echo=True)

Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine)
