import librosa
import streamlit as st
import io
from scipy.io.wavfile import write

from espeak_phonemizer import EspeakPhonemizer
from searcher import Searcher
from transcriber import Transcriber


def mocksearch_service(text):
    print(f'Searching for {text}')
    return [(1, 3), (68, 76)]


def process_timestamps(ts_list):
    if ts_list:
        print('Getting ready to display your search results ..')
        st.write('Here are the timestamps ..')
        st.write([f'start: {start}, end: {end}, sim: {sim}' for start, end, sim in ts_list])
    else:
        st.write(f'Could not find what you were looking for ..')


def audio(filename):
    audio_file = open(filename, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')


def audio_wav(wav, sr=16000):
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, sr, wav)
    st.audio(byte_io, format='audio/wav')


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

@st.cache
def get_audio_transcription(file):
    audio_input, sample_rate = librosa.load(file, sr=16000)
    transcriber = Transcriber()
    transcribed = transcriber(audio_input)
    return audio_input, transcribed


wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0367_046-r_0367_047.wav'


audio_input, transcribed = get_audio_transcription(wav_file)
espeak_phonemizer = EspeakPhonemizer()
searcher = Searcher()
audio(wav_file)
reconstructed_sample = [x[0] for x in transcribed]
reconstructed_sample = ''.join(reconstructed_sample).lower()
st.write(reconstructed_sample)

if __name__ == '__main__':
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    icon("search")
    query = st.text_input("", "Search...")  # searched text goes into this var
    button_de = st.button("DE")  # Bool Flag, indicates whether 'ok' button has been clicked
    button_en = st.button("EN")  # Bool Flag, indicates whether 'ok' button has been clicked


    if button_de or button_en:
        language = 'de' if button_de else 'en'
        phonemized_query = espeak_phonemizer(query, language='en')
        st.write(f'Looking for query: {query}, language: {language}, phonemes: {phonemized_query}')
        phonemized_query = phonemized_query.replace(' ', '')

        reconstructed_sample = [x[0] for x in transcribed]
        reconstructed_sample = ''.join(reconstructed_sample).lower()
        print(reconstructed_sample)

        timestamp_list = searcher(transcribed, phonemized_query, language='de', max_char_errors=int(len(query) * 0.5))
        timestamp_list.sort(key=lambda x: -x[-1])
        print(timestamp_list)
        if len(timestamp_list) == 0:
            st.write(f'Could not find what you were looking for...')
        for left, right, sim in timestamp_list:
            st.write(f'similarity: {sim}, start: {left}, end: {right}')
            left = int(left * 16000)
            right = int(right * 16000)
            audio_wav(audio_input[left:right])