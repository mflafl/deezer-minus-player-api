from pydantic import BaseModel


class StemConfiguration(BaseModel):
    vocals: str = None
