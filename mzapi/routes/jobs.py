from fastapi import APIRouter, HTTPException

from celery.result import AsyncResult

from mzapi.jobs.models.job_state import JobState

router = APIRouter()


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    result = AsyncResult(job_id)

    if result.info is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobState(job_id=result.id, progress=result.info['progress'], stage=result.info['stage'])
