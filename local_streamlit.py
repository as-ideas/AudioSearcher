import streamlit as st


def mocksearch_service(text):
    print(f'Searching for {text}')
    return [(1, 3), (68, 76)]


def process_timestamps(ts_list):
    if ts_list:
        print('Getting ready to display your search results ..')
        st.write('Here are the timestamps ..')
        st.write([i[0] for i in ts_list])
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


if __name__ == '__main__':
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    icon("search")
    selected = st.text_input("", "Search...")  # searched text goes into this var
    button_clicked = st.button("OK")  # Bool Flag, indicates whether 'ok' button has been clicked
    audio('/Users/tjain1/Downloads/STU1 MOD R rough.wav')
    if button_clicked:
        timestamp_list = mocksearch_service(selected)
        process_timestamps(timestamp_list)
