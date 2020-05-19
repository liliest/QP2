#Gender classification
This repository contains files related to my second qualifying paper on voice gender classification using deep neural networks with raw audio as inputs.
##Data
This project uses data from the [Voices of California corpus](http://web.stanford.edu/dept/linguistics/VoCal/index.html). `speakers.py` handles transcripts of many hundreds of sociolinguistic interviews to determine when in the matching recording the interviewee is producing non-overlapping speech.
Model predictions are calculated and stored in anonymized `.csv` files by `process.py`.
## Requirements
This project was written in Python 2.7.16, and there are tricky interleaving dependencies, particularly with regard to the `pysoundfile` module. I can't guarantee it works on any other version. 
##Acknnowledgements
I owe a great many thanks to Oscar Knagg, who made the code
from his very successful raw-audio voice gender classification experiment public in 2018.
`data.py`, `utils.py` and `models.py` remain essentially unchanged. I have modified `process.py` to suit my particular needs.
I trained the network myself (on the same LibriSpeech dataset) and achieved very slightly higher accuracy than Knagg reports in his [Medium article](https://medium.com/@oknagg/gender-classification-from-raw-audio-with-1d-convolutions-969c82e6b3d1) (99.1% after 7 epochs).




