import time

from mzapi.core.effects_processor import EffectsProcessor
from mzapi.core.jobs_app import celery

from mzapi.core.deezer_spleeter import DeezerSpleeter
from mzapi.core.deezer_downloader import DeezerDownloader
from mzapi.jobs.models.job_state import JobStages


@celery.task(bind=True, ignore_result=False)
def save_track_stems(self, track_id=None, deezer_arl_token=None, config=None):
    task_id = self.request.id
    DeezerDownloader.download(track_id=track_id, deezer_arl_token=deezer_arl_token, task_id=task_id)
    DeezerSpleeter.spleet(track_id, task_id=task_id)
    EffectsProcessor.apply(track_id, task_id=task_id)

    return {'progress': 100, 'stage': JobStages.FINISHED}
