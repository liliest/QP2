import pandas as pd
from scipy.signal import resample
import numpy as np
from tqdm import tqdm
import soundfile as sf
import json

from data import LibriSpeechDataset
from config import PATH, LIBRISPEECH_SAMPLING_RATE
from speakers import Data
from models import *
from utils import whiten

import os

import torch

n_seconds = 3

trainset = LibriSpeechDataset(['train-clean-100','train-clean-360'], int(LIBRISPEECH_SAMPLING_RATE * n_seconds))

print('Predicting {} GPU support'.format('with' if torch.cuda.is_available() else 'without'))
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def predict():
    intervals = Data(False)
    existing_results = []
    for root, folders, files in os.walk(PATH + '/results/'):
        for f in files:
            if f.endswith('.csv'):
                speaker_name = f.replace('results_for_', '').replace('.csv', '')
                existing_results.append(speaker_name)
    num_intervals = 0
    for key in intervals.speaker_to_intervals:
        if key not in existing_results:
            for interval in intervals.speaker_to_intervals[key]:
                num_intervals += 1
    pbar = tqdm(total=num_intervals)
    for key in intervals.all_speakers:
        if key not in existing_results:
            model_path = 'data/weights/max_pooling__n_layers=7__n_filters=64__downsampling=1__n_seconds=3.torch'
            step_seconds = 0.04
            batchsize_for_prediction = 1
            if key in intervals.complex_transcripts:
                audio_path = PATH + '/data/voc/audio/' + key + '.wav'
            if key in intervals.speakers:
                audio_path = PATH + '/data/voc/simple_audio/' + key + '.wav'
            speaker = key



            ##############
            # Load audio #
            ##############

            audio, audio_sampling_rate = sf.read(audio_path)
            audio_duration_seconds = audio.shape[0]*1./audio_sampling_rate
            audio_duration_minutes = audio_duration_seconds/60.

            ##############
            # Load model #
            ##############

            model_type = model_path.split('/')[-1].split('__')[0]
            model_name =        model_path.split('/')[-1].split('.')[0]
            model_params = {i.split('=')[0]: float(i.split('=')[1]) for i in model_name.split('__')[1:]}

            # Here we assume that the model was trained on the LibriSpeech dataset
            model_sampling_rate = LIBRISPEECH_SAMPLING_RATE/model_params['downsampling']
            model_num_samples = int(model_params['n_seconds']*model_sampling_rate)

            if model_type == 'max_pooling':
                    model = ConvNet(int(model_params['n_filters']), int(model_params['n_layers']))
            elif model_type == 'dilated':
                model = DilatedNet(int(model_params['n_filters']), int(model_params['n_depth']), int(model_params['n_stacks']))
            else:
                raise(ValueError, 'Model type not recognised.')

            model.load_state_dict(torch.load(model_path))
            model.double()
            model.cuda()
            model.eval()

            ######################
            # Loop through audio #
            ######################

            step_samples = int(step_seconds*model_sampling_rate)
            step_samples_at_audio_rate = int(step_seconds*audio_sampling_rate)
            default_shape = None
            batch = []
            pred = []
            start_min = []

            for interval in intervals.speaker_to_intervals[key]:
                start = float(interval[0])
                end = float(interval[1])
                start_samples = int(audio_sampling_rate * start)
                end_samples = int(audio_sampling_rate * end)

                for lower in range(start_samples, end_samples, step_samples_at_audio_rate):
                    x = audio[lower:lower+(int(model_params['n_seconds']*audio_sampling_rate))]

                    if x.shape[0] != model_params['n_seconds']*audio_sampling_rate:
                        break

                    x = torch.from_numpy(x).reshape(1, -1)

                    x = whiten(x)

                    # For me the bottleneck is this scipy resample call, increasing batch size doesn't make it any faster
                    x = torch.from_numpy(
                        resample(x, model_num_samples, axis=1)
                    ).reshape((1, 1, model_num_samples))

                    y_hat = model(x).item()

                    pred.append(y_hat)
                    start_min.append(lower / 44100.)
                pbar.update(1)

            df = pd.DataFrame(data={'speaker': speaker, 'start_second': start_min, 'p': pred})
            df = df.assign(
                # Time in seconds of the end of the prediction fragment
                t_end=df['start_second'] + model_params['n_seconds'],
                # Time in seconds of the center of the prediction fragment
                t_center=df['start_second'] * 60 + model_params['n_seconds'] / 2.
            )
            df.to_csv(PATH + '/results/results_for_' + speaker + '.csv', index=False)
    pbar.close()
