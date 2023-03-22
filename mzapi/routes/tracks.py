import json
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from .schemas import StemConfiguration
from mzapi.jobs.save_track_stems import save_track_stems
from mzapi.jobs.models.job_state import JobState

router = APIRouter()


@router.get("/track/favorites")
async def favorites():
    with open("mzapi/moc/track/favorites.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return JSONResponse(content=data)


@router.post("/track/{track_id}/stem")
async def create_item(track_id: int, config: StemConfiguration,
                      deezer_arl_token: str = Header(None, alias="X-DEEZER-ARL-TOKEN")):
    if deezer_arl_token is None:
        return {"message": "Missing Deezer ARL Token header"}

    result = save_track_stems.delay(track_id=track_id, deezer_arl_token=deezer_arl_token)
    return JobState(job_id=result.id, progress=0, stage=0)
