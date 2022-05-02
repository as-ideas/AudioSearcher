from typing import List, Tuple

import librosa
import numpy as np
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

DEFAULT_PROCESSOR = 'facebook/wav2vec2-xlsr-53-espeak-cv-ft'
DEFAULT_MODEL = 'facebook/wav2vec2-xlsr-53-espeak-cv-ft'


class Transcriber:

    def __init__(self,
                 processor_name: str = DEFAULT_PROCESSOR,
                 model_name: str = DEFAULT_MODEL,
                 sample_rate: int = 16000) -> None:
        self.processor = Wav2Vec2Processor.from_pretrained(processor_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        self.sample_rate = sample_rate

    def __call__(self, wav: np.array) -> List[Tuple[str, float]]:
        """
        Transceribes a wav file and returns the phoneme to time mapping (in seconds)
        :param wav: audio input
        :return: List of tuples, where each tuple consists of (phoneme, time in seconds)
        """

        input_values = self.processor(wav, sampling_rate=self.sample_rate, return_tensors="pt").input_values
        prediction = self.model(input_values)
        logits = prediction.logits
        predicted_ids = torch.argmax(logits, dim=-1)
        norm = len(wav) / predicted_ids.size(1) / self.sample_rate
        transcribed = []
        last_phon = ''
        for i in range(predicted_ids.size(1)):
            t = self.processor.decode(predicted_ids[0, i:i+1])
            if t != '' and t != last_phon:
                for c in t:
                    transcribed.append((c, i * norm))
                last_phon = t
        return transcribed


if __name__ == '__main__':
    transcriber = Transcriber()
    wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_011.wav'
    audio_input, sample_rate = librosa.load(wav_file, sr=16000)

    transcription = transcriber(audio_input)

    for c, t in transcription:
        print(c, t)