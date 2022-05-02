import librosa
from espeak_phonemizer import EspeakPhonemizer
from transcriber import Transcriber
from searcher import Searcher

if __name__ == '__main__':
    transcriber = Transcriber()
    espeak_phonemizer = EspeakPhonemizer()
    searcher = Searcher()

    wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_011.wav'
    audio_input, sample_rate = librosa.load(wav_file, sr=16000)

    query = 'persönlich'
    query = espeak_phonemizer(query, language='de')


    transcription = transcriber(audio_input)
    res = searcher(transcription, query, language='de', max_char_errors=4)

    print(res)
    # here goes search(query_phons, transcription) -> search_output
