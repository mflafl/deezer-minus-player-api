import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Database:
    engine = None

    def init(self):
        self.engine = create_engine(os.environ['DATABASE_URL'])  # , echo=True

    def get_session(self):
        return Session(bind=self.engine)

    def get_db(self):
        return self.engine


database = Database()
