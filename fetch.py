from config import PATH, BOX_PATH
import os
import shutil
from speakers import Data

local_transcripts = []
box_audio = []
local_audio = []

data = Data(False)
speakers = data.all_speakers

for root, folders, files in os.walk(BOX_PATH):
    for f in files:
        if f.endswith('.wav'):
            box_audio.append(f.replace('.wav', ''))

for root, folders, files in os.walk(PATH + '/data/voc/simple_audio/'):
    for f in files:
        if f.endswith('.wav'):
            local_audio.append(f.replace('.wav', ''))

for root, folders, files in os.walk(PATH + '/data/voc/audio/'):
    for f in files:
        if f.endswith('.wav'):
            local_audio.append(f.replace('.wav', ''))


for root, folders, files in os.walk(PATH + '/data/voc/'):
    for f in files:
        if f.endswith('.txt'):
            local_transcripts.append(f.replace('.txt', ''))

for audio in box_audio:
    print("Box audio is {}".format(audio))
    if audio not in local_audio:
        if audio in data.speakers:
            print(audio)
            source = BOX_PATH + audio + '.wav'
            destination = PATH + '/data/voc/simple_audio/' + audio + '.wav'
            print('Copying {}'.format(audio))
            shutil.copyfile(source, destination)
        if audio in data.complex_transcripts:
            print(audio)
            source = BOX_PATH + audio + '.wav'
            destination = PATH + '/data/voc/audio/' + audio + '.wav'
            print('Copying {}'.format(audio))
            shutil.copyfile(source, destination)









