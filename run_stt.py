# !pip install transformers
# !pip install datasets
from pathlib import Path

import librosa
import torch
import tqdm
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# load pretrained model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")

wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_012.wav'

audio_input, sample_rate = librosa.load(wav_file, sr=16000)
print(len(audio_input))

# pad input values and return pt tensor
input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

# INFERENCE

# retrieve logits & take argmax
prediction = model(input_values)
logits = prediction.logits
predicted_ids = torch.argmax(logits, dim=-1)

# transcribe
transcription = processor.decode(predicted_ids[0], clean_up_tokenization_spaces=False)
transcription = transcription.replace(' ', '')

# FINE-TUNE
print(wav_file)
print(transcription)
