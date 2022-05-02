import struct
from typing import List, Tuple

import librosa
import numpy as np
import torch
import webrtcvad
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

DEFAULT_PROCESSOR = 'facebook/wav2vec2-xlsr-53-espeak-cv-ft'
DEFAULT_MODEL = 'facebook/wav2vec2-xlsr-53-espeak-cv-ft'


class LongTranscriber:

    def __init__(self,
                 processor_name: str = DEFAULT_PROCESSOR,
                 model_name: str = DEFAULT_MODEL,
                 sample_rate: int = 16000,
                 min_wav_piece_len: int = 50000) -> None:
        self.processor = Wav2Vec2Processor.from_pretrained(processor_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        self.sample_rate = sample_rate
        self.min_wav_piece_len = min_wav_piece_len

    def __call__(self, wav: np.array) -> List[Tuple[str, float]]:
        """
        Transceribes a wav file and returns the phoneme to time mapping (in seconds)
        :param wav: audio input
        :return: List of tuples, where each tuple consists of (phoneme, time in seconds)
        """

        wav_pieces = self._split_wav_at_silences(wav)
        offset = 0
        transcription = []
        for wav_piece in wav_pieces:
            piece_trans = self._transcribe_piece(wav_piece)
            piece_trans = [(c, t + offset) for c, t in piece_trans]
            transcription.extend(piece_trans)
            offset += len(wav_piece) / self.sample_rate

        return transcription

    def _transcribe_piece(self, wav: np.array) -> List[Tuple[str, float]]:
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

    def _split_wav_at_silences(self, wav: np.array) -> List[np.array]:
        int16_max = (2 ** 15) - 1
        samples_per_window = (30 * 16000) // 1000
        wav = wav[:len(wav) - (len(wav) % samples_per_window)]
        pcm_wave = struct.pack("%dh" % len(wav), *(np.round(wav * int16_max)).astype(np.int16))
        voice_flags = []
        vad = webrtcvad.Vad(mode=3)
        for window_start in range(0, len(wav), samples_per_window):
            window_end = window_start + samples_per_window
            voice_flags.append(vad.is_speech(pcm_wave[window_start * 2:window_end * 2],
                                             sample_rate=16000))
        voice_flags = np.array(voice_flags)
        def moving_average(array, width):
            array_padded = np.concatenate((np.zeros((width - 1) // 2), array, np.zeros(width // 2)))
            ret = np.cumsum(array_padded, dtype=float)
            ret[width:] = ret[width:] - ret[:-width]
            return ret[width - 1:] / width
        audio_mask = moving_average(voice_flags, 8)
        audio_mask = np.round(audio_mask).astype(np.bool)
        audio_mask = np.repeat(audio_mask, samples_per_window)

        split_points = [0]
        for i in range(1, len(wav)):
            if audio_mask[i] and not audio_mask[i-1] and i - split_points[-1] > self.min_wav_piece_len:
                split_points.append(i)

        split_points.append(len(wav))

        last_index = 0
        split_wavs = []
        for split_index in split_points[1:]:
            split_wavs.append(wav[last_index:split_index])
            last_index = split_index

        return split_wavs


if __name__ == '__main__':
    transcriber = LongTranscriber()
    wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_011.wav'
    audio_input, sample_rate = librosa.load(wav_file, sr=16000)

    transcription = transcriber(audio_input)

    for c, t in transcription:
        print(c, t)