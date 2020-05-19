import os
from config import PATH

class InterviewDataset():
    def __init__(self):
        self.dictionary = {}
        self.list = []
        self.speaker_list = []
        self.n_speakers = 0
        self.speaker_to_intervals = {}
        for root, folders, files in os.walk(PATH+'/data/voc/'):
            print(root)
            if len(files) == 0:
                continue
            for file in files:
                if file.endswith('BAK_Confid_004.txt'):
                    speaker = file.replace('.txt', '')
                    self.speaker_list.append(speaker)
                    intervals_by_id = {}
                    transcript_to_dictionary = {}
                    absolute_path = os.path.join(root, file)
                    with open(absolute_path, 'r') as f:
                        # id_list = []
                        # for line in f:
                        #     if len(line.split()) > 1:
                        #         id = line.split()[0]
                        #         if id not in id_list:
                        #             id_list.append(id)
                        # print('file = {}, id_list = {}'.format(speaker, id_list))
                        # if len(id_list) == 2:
                        for line in f:
                            if len(line.split()) > 4:
                                id = line.split()[1]
                                start = line.split()[2]
                                end = line.split()[3]
                                if id not in transcript_to_dictionary:
                                    transcript_to_dictionary[id] = raw_input('Speaker is: {}. What should id ({}) be called?: '.format(speaker, id))
                                if transcript_to_dictionary[id] not in intervals_by_id:
                                    intervals_by_id[transcript_to_dictionary[id]] = [(start, end)]
                                else:
                                    intervals_by_id[transcript_to_dictionary[id]].append((start, end))
                        self.dictionary[speaker] = intervals_by_id
        for speaker in self.speaker_list:
            self.filter_dictionary(speaker)


    def filter_dictionary(self, speaker):
        if len(self.dictionary[speaker]['interviewer']) == 0 or len(self.dictionary[speaker]['speaker']) == 0:
            return
        first_interviewer_tuple = self.dictionary[speaker]['interviewer'][0]
        first_speaker_tuple = self.dictionary[speaker]['speaker'][0]
        # same
        if first_interviewer_tuple == first_speaker_tuple:
            print('same')
            self.dictionary[speaker]['interviewer'].remove(first_interviewer_tuple)
            self.dictionary[speaker]['speaker'].remove(first_speaker_tuple)
            return self.filter_dictionary(speaker)
        # before
        if float(first_interviewer_tuple[1]) <= float(first_speaker_tuple[0]):
            print('before')
            self.dictionary[speaker]['interviewer'].remove(first_interviewer_tuple)
            return self.filter_dictionary(speaker)
        # after
        if float(first_interviewer_tuple[0]) >= float(first_speaker_tuple[1]):
            print('after')
            self.dictionary[speaker]['speaker'].remove(first_speaker_tuple)
            if speaker not in self.speaker_to_intervals:
                self.speaker_to_intervals[speaker] = [first_speaker_tuple]
            else:
                self.speaker_to_intervals[speaker].append(first_speaker_tuple)
            return self.filter_dictionary(speaker)
        # completely overlapping
        if float(first_interviewer_tuple[0]) < float(first_speaker_tuple[0]) and float(first_interviewer_tuple[1]) > float(first_speaker_tuple[1]):
            self.dictionary[speaker]['speaker'].remove(first_speaker_tuple)
            return self.filter_dictionary(speaker)
        # completely subset
        if float(first_interviewer_tuple[0]) > float(first_speaker_tuple[0]) and float(first_interviewer_tuple[1]) < float(first_speaker_tuple[1]):
            self.dictionary[speaker]['interviewer'].remove(first_interviewer_tuple)
            self.dictionary[speaker]['speaker'].remove(first_speaker_tuple)
            return self.filter_dictionary(speaker)
        # overlapping before
        if float(first_interviewer_tuple[1]) > float(first_speaker_tuple[0]) and float(first_interviewer_tuple[1]) < float(first_speaker_tuple[1]) and float(first_interviewer_tuple[0]) < float(first_speaker_tuple[0]):
            self.dictionary[speaker]['speaker'].remove(first_speaker_tuple)
            return self.filter_dictionary(speaker)
            # overlapping after
        if float(first_interviewer_tuple[0]) > float(first_speaker_tuple[0]) and float(first_interviewer_tuple[0]) < float(first_speaker_tuple[1]) and float(first_interviewer_tuple[1]) > float(first_speaker_tuple[1]):
            self.dictionary[speaker]['speaker'].remove(first_speaker_tuple)
            return self.filter_dictionary(speaker)
        print('doing nothing')



