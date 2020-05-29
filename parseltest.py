from __future__ import division
import parselmouth
import numpy as np
import seaborn as sns
from config import PATH
import json
import soundfile as sf
import pandas as pd
import os
from speakers import Data


data = Data()
existing_results = []
for root, folders, files in os.walk(PATH + '/results/pitch/'):
    for f in files:
        if f.endswith('.csv'):
            speaker_name = f.replace('pitch_results_for_', '').replace('.csv', '')
            existing_results.append(speaker_name)
for key in data.speakers:
    print(key)
    if key not in existing_results:
        audio_path = PATH + '/data/voc/simple_audio/' + key + '.wav'
        n_seconds = 3
        audio, audio_sampling_rate = sf.read(audio_path)
        audio_duration_seconds = audio.shape[0] * 1. / audio_sampling_rate
        audio_duration_minutes = audio_duration_seconds / 60.
        step_seconds = 0.04
        mean = []
        min = []
        max = []
        start_min = []
        for interval in data.speaker_to_intervals[key]:
            speaker = key
            start = float(interval[0])
            end = float(interval[1])
            if end - start >= 3:
                start_samples = int(audio_sampling_rate * start)
                end_samples = int(audio_sampling_rate * end)
                step_samples_at_audio_rate = int(step_seconds * audio_sampling_rate)
                for lower in range(start_samples, end_samples, step_samples_at_audio_rate):
                    x = audio[lower:lower + (int(3 * audio_sampling_rate))]
                    if x.shape[0] != 3 * audio_sampling_rate:
                        break
                    sf.write(PATH + '/data/clips/{}_{}_{}.wav'.format(speaker, lower / audio_sampling_rate, (lower + (int(3 * audio_sampling_rate))) / audio_sampling_rate), x, audio_sampling_rate)
                    sound = parselmouth.Sound(PATH + '/data/clips/{}_{}_{}.wav'.format(speaker, lower / audio_sampling_rate, (lower + (int(3 * audio_sampling_rate))) / audio_sampling_rate))
                    pitch = sound.to_pitch()
                    pitch_values = pitch.selected_array['frequency']
                    if pitch_values[pitch_values!=0].size != 0:
                        mean.append(np.mean(pitch_values[pitch_values!=0]))
                        start_min.append(lower / 44100.)

                    os.remove(PATH + '/data/clips/{}_{}_{}.wav'.format(speaker, lower / audio_sampling_rate, (lower + (int(3 * audio_sampling_rate))) / audio_sampling_rate))

            df = pd.DataFrame(data={'speaker': speaker, 'start_second': start_min, 'mean': mean})
            df = df.assign(
                # Time in seconds of the end of the prediction fragment
                t_end=df['start_second'] + 3,
                # Time in seconds of the center of the prediction fragment
                t_center=df['start_second'] + 1.5
            )
            df.to_csv(PATH + '/results/pitch/pitch_results_for_' + speaker + '.csv', index=False)







