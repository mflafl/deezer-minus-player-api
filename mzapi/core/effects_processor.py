import os

from pedalboard import Pedalboard, Chorus, Reverb, Compressor, Gain, LadderFilter, Phaser, Convolution
from pedalboard.io import AudioFile


class EffectsProcessor:
    @staticmethod
    def apply(track_id, task_id=None):
        board = Pedalboard([
            Compressor(threshold_db=-50, ratio=25),
            Gain(gain_db=30),
            Chorus(),
            LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
            Phaser(),
            # Convolution("./guitar_amp.wav", 1.0),
            Reverb(room_size=0.25),
        ])

        source_file = f'{os.environ["DOWNLOAD_PATH"]}/{track_id}/accompaniment.flac'
        output_file = f'{os.environ["DOWNLOAD_PATH"]}/{track_id}/output.flac'

        with AudioFile(source_file) as f:
            with AudioFile(output_file, 'w', f.samplerate, f.num_channels) as o:
                while f.tell() < f.frames:
                    chunk = f.read(int(f.samplerate))
                    effected = board(chunk, f.samplerate, reset=False)
                    o.write(effected)
