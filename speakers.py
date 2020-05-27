import os
from config import PATH
from tqdm import tqdm
import json

class Data():
    def __init__(self, simple=True):
        self.simple = simple
        self.speakers = []
        self.audios = []
        self.dictionary = {}
        self.speaker_to_intervals = {}
        self.recursion = 0
        self.speaker_to_datasetid = {}
        self.datasetid_to_speaker = {}
        self.anonymized_dict = {}
        self.complex_transcripts = []
        self.all_speakers = []


        self.list_of_speakers()
        print("Created list of speakers.")
        self.get_intervals()
        print("Created intervals.")


        print("Filter simple dictionaries")

        pbar = tqdm(total=len(self.all_speakers))
        for speaker in self.all_speakers:
            if speaker in self.speakers:
                self.filter_dictionary_simple(speaker)
            if speaker in self.complex_transcripts:
                self.filter_dictionary_complex(speaker)
            pbar.update(1)
        pbar.close()


        for index, (key, value) in enumerate(self.speaker_to_intervals.iteritems()):
            self.speaker_to_datasetid[key] = index
            self.datasetid_to_speaker[index] = key
            self.anonymized_dict[index] = value
        print("Created anonymized dictionary.")

        with open(PATH + '/data/voc/'+'speakers_to_intervals.json', 'w') as fp:
            json.dump(self.speaker_to_intervals, fp)




    def get_intervals(self):
        for speaker in self.all_speakers:
            transcript_path = PATH + '/data/voc/transcripts/' + speaker + '.txt'
            with open(transcript_path, 'r') as f:
                intervals_by_id = {}
                for line in f:
                    id = line.split('\t')[1]
                    start = line.split('\t')[2]
                    end = line.split('\t')[3]
                    if id not in intervals_by_id:
                        intervals_by_id[id] = [(start, end)]
                    else:
                        intervals_by_id[id].append((start, end))
            self.dictionary[speaker] = intervals_by_id


    def filter_dictionary_simple(self, speaker):
        for tuple in self.dictionary[speaker]['speaker']:
            if self.check_overlap(tuple, self.dictionary[speaker]['interviewer']):
                if speaker not in self.speaker_to_intervals:
                    self.speaker_to_intervals[speaker] = [tuple]
                else:
                    self.speaker_to_intervals[speaker].append(tuple)

    def filter_dictionary_complex(self, speaker):
        if 'speaker' in self.dictionary[speaker] and 'other' in self.dictionary[speaker]:
            for tuple in self.dictionary[speaker]['speaker']:
                if self.check_overlap(tuple, self.dictionary[speaker]['interviewer']) and self.check_overlap(tuple, self.dictionary[speaker]['other']):
                    if speaker not in self.speaker_to_intervals:
                        self.speaker_to_intervals[speaker] = [tuple]
                    else:
                        self.speaker_to_intervals[speaker].append(tuple)
        elif 'interviewer1' in self.dictionary[speaker]:
            for tuple in self.dictionary[speaker]['speaker']:
                if self.check_overlap(tuple, self.dictionary[speaker]['interviewer1']) and self.check_overlap(tuple, self.dictionary[speaker]['interviewer2']):
                    if speaker not in self.speaker_to_intervals:
                        self.speaker_to_intervals[speaker] = [tuple]
                    else:
                        self.speaker_to_intervals[speaker].append(tuple)
        elif 'speaker2' in self.dictionary[speaker]:
            for tuple in self.dictionary[speaker]['speaker1']:
                if self.check_overlap(tuple, self.dictionary[speaker]['speaker2']) and self.check_overlap(tuple, self.dictionary[speaker]['interviewer']):
                    if speaker not in self.speaker_to_intervals:
                        self.speaker_to_intervals[speaker] = [tuple]
                    else:
                        self.speaker_to_intervals[speaker].append(tuple)




    def check_overlap(self, speaker_tuple, other_list):
        for tuple in other_list:
            if tuple == speaker_tuple:
                return False
            if float(tuple[0]) < float(speaker_tuple[0]) < float(tuple[1]):
                return False
            if float(tuple[0]) < float(speaker_tuple[1]) < float(tuple[1]):
                return False
        return True




    def list_of_speakers(self):
        for root, folders, files in os.walk(PATH + '/data/voc/'):
            for f in files:
                if f.endswith('.wav'):
                    self.audios.append(f.replace('.wav', ''))

        for root, folders, files in os.walk(PATH + '/data/voc/transcripts/'):
            for f in files:
                if f.endswith('.txt'):
                    with open(PATH + '/data/voc/transcripts/' + f, 'r') as text:
                        ids = []
                        for line in text:
                            if line.split('\t')[1] not in ids:
                                ids.append(line.split('\t')[1])
                        if len(ids) == 2 and f.replace('.txt', '') in self.audios:
                            self.speakers.append(f.replace('.txt', ''))
                            self.all_speakers.append(f.replace('.txt', ''))
                        if not self.simple:
                            if f.replace('.txt', '') in self.audios:
                                if len(ids) == 3 and 'other' in ids:
                                    self.all_speakers.append(f.replace('.txt', ''))
                                    self.complex_transcripts.append(f.replace('.txt', ''))
                                elif len(ids) == 3 and 'interviewer1' in ids:
                                    self.all_speakers.append(f.replace('.txt', ''))
                                    self.complex_transcripts.append(f.replace('.txt', ''))
                                elif len(ids) == 3 and 'speaker2' in ids:
                                    self.all_speakers.append(f.replace('.txt', ''))
                                    self.complex_transcripts.append(f.replace('.txt', ''))


