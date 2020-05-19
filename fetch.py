from config import PATH, BOX_PATH
import os
import shutil
from speakers import data

local_transcripts = []
box_audio = []
simple_local_audio = []

data = data()
speakers = data.speakers

for root, folders, files in os.walk(BOX_PATH):
    for f in files:
        if f.endswith('.wav'):
            box_audio.append(f.replace('.wav', ''))

for root, folders, files in os.walk(PATH + '/data/voc/simple_audio/'):
    for f in files:
        if f.endswith('.wav'):
            simple_local_audio.append(f.replace('.wav', ''))

for root, folders, files in os.walk(PATH + '/data/voc/'):
    for f in files:
        if f.endswith('.txt'):
            local_transcripts.append(f.replace('.txt', ''))

for audio in box_audio:
    if audio not in simple_local_audio and audio in local_transcripts and audio in speakers:
        source = BOX_PATH + audio + '.wav'
        destination = PATH + '/data/voc/simple_audio/' + audio + '.wav'
        print('Copying {}'.format(audio))
        shutil.copyfile(source, destination)








