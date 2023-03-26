import os

import deezer
import deemix
import deemix.settings as settings
import deemix.downloader as downloader
from celery import current_app

from mzapi.jobs.models.job_state import JobStages


class DeezerDownloaderProgressListener:
    def __init__(self, task_id):
        self.task_id = task_id

    def send(self, type, data):
        if type == 'updateQueue':
            if 'failed' in data:
                progress = 0
            elif 'downloaded' in data:
                progress = 100
            else:
                progress = data['progress']

            meta = {'stage': JobStages['DOWNLOAD'], 'progress': progress}
            current_app.backend.store_result(self.task_id, meta, 'PROGRESS')


class DeezerDownloader:
    @staticmethod
    def download(track_id: int, deezer_arl_token: str, task_id=None):
        dz = deezer.Deezer()
        dz.login_via_arl(arl=deezer_arl_token)
        downObj = deemix.generateDownloadObject(dz, link=f'https://deezer/track/{track_id}', bitrate=9)
        new_settings = settings.DEFAULTS
        new_settings['downloadLocation'] = f"{os.environ['DOWNLOAD_PATH']}/{track_id}"
        new_settings['tracknameTemplate'] = str(track_id)
        downloader.Downloader(dz, downObj, settings=new_settings,
                              listener=DeezerDownloaderProgressListener(task_id)).start()
