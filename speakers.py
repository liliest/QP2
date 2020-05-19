import os
from config import PATH

class data():
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


        self.list_of_speakers()
        self.get_intervals()


        for speaker in self.speakers:
            self.filter_dictionary(speaker)

        for index, (key, value) in enumerate(self.speaker_to_intervals.iteritems()):
            self.speaker_to_datasetid[key] = index
            self.datasetid_to_speaker[index] = key
            self.anonymized_dict[index] = value




    def get_intervals(self):
        for speaker in self.speakers:
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

    def filter_dictionary(self, speaker):
        for tuple in self.dictionary[speaker]['speaker']:
            if self.check_overlap(tuple, self.dictionary[speaker]['interviewer']):
                if speaker not in self.speaker_to_intervals:
                    self.speaker_to_intervals[speaker] = [tuple]
                else:
                    self.speaker_to_intervals[speaker].append(tuple)

    def check_overlap(self, speaker_tuple, interviewer_list):
        for tuple in interviewer_list:
            if tuple == speaker_tuple:
                return False
            if float(tuple[0]) < float(speaker_tuple[0]) < float(tuple[1]):
                return False
            if float(tuple[0]) < float(speaker_tuple[1]) < float(tuple[1]):
                return False
        return True




    def list_of_speakers(self):
        for root, folders, files in os.walk(PATH + '/data/voc/simple_audio/'):
            for f in files:
                if f.endswith('.wav'):
                    self.audios.append(f.replace('.wav', ''))

        for root, folders, files in os.walk(PATH + '/data/voc/transcripts/'):
            for f in files:
                if f.endswith('.txt'):
                    if self.simple:
                        with open(PATH + '/data/voc/transcripts/' + f, 'r') as text:
                            ids = []
                            for line in text:
                                if line.split('\t')[1] not in ids:
                                    ids.append(line.split('\t')[1])
                            if len(ids) == 2 and f.replace('.txt', '') in self.audios:
                                self.speakers.append(f.replace('.txt', ''))