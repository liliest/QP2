import parselmouth
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import PATH
import json
import soundfile as sf

with open('speakers.json', 'r') as fp:
    speakers = json.load(fp)

speaker = 'BAK_Mendoza_Elisa'
intervals = speakers[speaker]
audio_path = PATH + '/data/voc/simple_audio/'+speaker+'.wav'
n_seconds = 3
audio, audio_sampling_rate = sf.read(audio_path)
audio_duration_seconds = audio.shape[0] * 1. / audio_sampling_rate
audio_duration_minutes = audio_duration_seconds / 60.
step_seconds = 0.04
interval = speakers[speaker][0]
start = float(interval[0])
end = float(interval[1])
start_samples = int(audio_sampling_rate * start)
end_samples = int(audio_sampling_rate * end)
step_samples_at_audio_rate = int(step_seconds * audio_sampling_rate)

for lower in range(start_samples, end_samples, step_samples_at_audio_rate):
    x = audio[lower:lower + (int(3 * audio_sampling_rate))]

    if x.shape[0] != 3 * audio_sampling_rate:
        break

    sf.write('/data/voc/clips/{}_{}_{}'.format(speaker,))


def draw_pitch(pitch):
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")







