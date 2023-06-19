import os
from spleeter.separator import Separator
import soundfile as sf
from celery import current_app

from mzapi.jobs.models.job_state import JobStages


class DeezerSpleeter:
    @staticmethod
    def spleet(track_id, task_id=None):
        meta = {'stage': JobStages['CONVERTING'], 'progress': 0}
        current_app.backend.store_result(task_id, meta, 'PROGRESS')

        # Set the input file path and the output directory path
        input_file = f"{os.environ['DOWNLOAD_PATH']}/{track_id}/{track_id}.flac"
        output_dir = f"{os.environ['DOWNLOAD_PATH']}/{track_id}"

        # Load the input file using soundfile
        audio_data, sample_rate = sf.read(input_file)

        # Split the audio into all possible channels using Spleeter
        # separator = Separator('spleeter:5stems')
        separator = Separator('spleeter:2stems')
        prediction = separator.separate(audio_data)

        # Save the split audio channels to the output directory
        for key, value in prediction.items():
            output_file = os.path.join(output_dir, key + '.flac')
            sf.write(output_file, value, sample_rate)

        # TODO: deezer library not providing progress callback
        meta = {'stage': JobStages['FINISHED'], 'progress': 100}
        current_app.backend.store_result(task_id, meta, 'PROGRESS')
