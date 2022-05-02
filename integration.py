import librosa

from espeak_phonemizer import EspeakPhonemizer
from transcriber import Transcriber

if __name__ == '__main__':
    transcriber = Transcriber()
    espeak_phonemizer = EspeakPhonemizer()

    wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_011.wav'
    audio_input, sample_rate = librosa.load(wav_file, sr=16000)

    query = 'persönlich'

    query_phons = espeak_phonemizer(query, language='de')
    transcription = transcriber(audio_input)

    # here goes search(query_phons, transcription) -> search_output

    print(query_phons)
    print(transcription)
