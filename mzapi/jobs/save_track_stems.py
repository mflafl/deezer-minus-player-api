import time

from mzapi.core.jobs_app import celery

from mzapi.core.deezer_spleeter import DeezerSpleeter
from mzapi.core.deezer_downloader import DeezerDownloader
from mzapi.jobs.models.job_state import JobStage

@celery.task(bind=True, ignore_result=False)
def save_track_stems(self, track_id=None, deezer_arl_token=None):
    DeezerDownloader.download(track_id=track_id, deezer_arl_token=deezer_arl_token)
    # TODO: Update download progress using listener
    self.update_state(state='PROGRESS', meta={'stage': JobStage.CONVERTING, 'progress': 50})
    # TODO: spleeter not working (multiprocessing not allowed)
    # DeezerSpleeter.spleet(track_id)

    return 'Done'