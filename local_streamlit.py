import librosa
import streamlit as st

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


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


wav_file = '/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_011.wav'
audio_input, sample_rate = librosa.load(wav_file, sr=16000)
espeak_phonemizer = EspeakPhonemizer()
transcriber = Transcriber()
searcher = Searcher()
transcribed = transcriber(audio_input)
audio('/Users/cschaefe/datasets/bild_snippets_cleaned/Snippets/r_0695_011.wav')


if __name__ == '__main__':
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    icon("search")
    query = st.text_input("", "Search...")  # searched text goes into this var
    button_clicked = st.button("OK")  # Bool Flag, indicates whether 'ok' button has been clicked

    if button_clicked:
        phonemized_query = espeak_phonemizer(query, language='de')
        print(transcribed)
        timestamp_list = searcher(transcribed, phonemized_query, language='de', max_char_errors=4)
        timestamp_list.sort(key=lambda x: x[-1])
        print(timestamp_list)
        process_timestamps(timestamp_list)
