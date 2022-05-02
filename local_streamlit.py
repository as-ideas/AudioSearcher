import streamlit as st


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
    print(selected)
    button_clicked = st.button("OK") ## Bool Flag
    print(button_clicked)

    audio('/Users/tjain1/Downloads/STU1 MOD R rough.wav')