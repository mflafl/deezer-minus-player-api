from fastapi import APIRouter, Header
from .schemas import StemConfiguration
from mzapi.jobs.save_track_stems import save_track_stems
from mzapi.jobs.models.job_state import JobState
import deezer

router = APIRouter()


@router.post("/tracks/{track_id}/stem")
async def create_item(track_id: int, config: StemConfiguration,
                      deezer_arl_token: str = Header(None, alias="X-DEEZER-ARL-TOKEN")):
    if deezer_arl_token is None:
        return {"message": "Missing Deezer ARL Token header"}

    result = save_track_stems.delay(track_id=track_id, deezer_arl_token=deezer_arl_token, config=config)
    return JobState(job_id=result.id, progress=0, stage=0)


@router.get('/tracks/{track_id}')
async def get_track_by_id(track_id: int, deezer_arl_token: str = Header(None, alias="X-DEEZER-ARL-TOKEN")):
    dz = deezer.Deezer()
    dz.login_via_arl(arl=deezer_arl_token)
    track = dz.api.get_track(track_id)
    return track
