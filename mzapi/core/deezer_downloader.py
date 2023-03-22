import os
import deezer
import deemix
import deemix.settings as settings
import deemix.downloader as downloader
from deemix.__main__ import LogListener

listener = LogListener()


class DeezerDownloader:
    @staticmethod
    def download(track_id: int, deezer_arl_token: str):
        dz = deezer.Deezer()
        dz.login_via_arl(arl=deezer_arl_token)
        downObj = deemix.generateDownloadObject(dz, link=f'https://deezer/track/{track_id}', bitrate=9)
        new_settings = settings.DEFAULTS
        new_settings['downloadLocation'] = f"{os.environ['DOWNLOAD_PATH']}/{track_id}"
        new_settings['tracknameTemplate'] = str(track_id)
        downloader.Downloader(dz, downObj, settings=new_settings, listener=listener).start()
