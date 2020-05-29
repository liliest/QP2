import os
from config import PATH

for root, folders, files in os.walk(PATH + '/data/voc/transcripts/'):
    for f in files:
        if f.endswith('.txt'):
            new_lines = []
            with open(PATH+'/data/voc/transcripts/'+f, 'r') as fp:
                for line in fp:
                    split = line.split('\t')
                    if split[4] != '\n':
                        new_lines.append(line)
            with open(PATH+'/data/voc/transcripts/'+f, 'w+') as fp2:
                fp2.writelines("%s" % line for line in new_lines)

