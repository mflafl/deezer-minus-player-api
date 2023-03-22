from dataclasses import dataclass
import json

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from mzapi.models.base import Base

@dataclass
class Data:
    id: int
    external_id: int
    stemed: bool

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, default=0)
    external_source = Column(String, default='')
    data = Column(JSONB)
    stemmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, data: Data):
        self.data = json.dumps(data.__dict__)
