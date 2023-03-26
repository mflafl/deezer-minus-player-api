from fastapi import APIRouter

from celery.result import AsyncResult

from mzapi.jobs.models.job_state import JobState

router = APIRouter()


@router.get("/job/{job_id}")
async def get_job(job_id: str):
    result = AsyncResult(job_id)
    return JobState(job_id=result.id, progress=result.info['progress'], stage=result.info['stage'])
