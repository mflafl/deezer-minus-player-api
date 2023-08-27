from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from dataclasses import dataclass
import json

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB

from mzapi.models.base import Base


@dataclass
class Data:
    id: str
    external_id: int
    stemmed: bool


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    external_id = Column(Integer)
    external_source = Column(String)
    stemmed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    external_source_added_at = Column(DateTime)
    length = Column(Integer)
    title = Column(String, nullable=False)
    artist = Column(String)
    album = Column(String)
    data = Column(JSONB)
