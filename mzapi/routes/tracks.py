from typing import List

from fastapi import APIRouter, Header, Depends, Response
from sqlalchemy.orm import Session

from .schemas import StemConfiguration
from mzapi.core.database import database
from mzapi.jobs.save_track_stems import save_track_stems
from mzapi.jobs.models.job_state import JobState
from ..models.track import Track

router = APIRouter()


@router.get("/tracks", response_model=None)
async def get_tracks():
    db: Session = database.get_session()
    tracks = db.query(Track).all()
    return tracks


@router.post("/tracks/{track_id}/stem")
async def create_item(track_id: int, config: StemConfiguration,
                      deezer_arl_token: str = Header(None, alias="X-DEEZER-ARL-TOKEN")):
    if deezer_arl_token is None:
        return {"message": "Missing Deezer ARL Token header"}

    result = save_track_stems.delay(track_id=track_id, deezer_arl_token=deezer_arl_token, config=dict(config))
    return JobState(job_id=result.id, progress=0, stage=0)
