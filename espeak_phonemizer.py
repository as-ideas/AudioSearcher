from phonemizer.phonemize import phonemize


class EspeakPhonemizer:

    def __call__(self, text: str, language: str) -> str:
        return phonemize(text,
                         language=language,
                         backend='espeak',
                         strip=True,
                         preserve_punctuation=True,
                         with_stress=False,
                         njobs=1,
                         language_switch='remove-flags')


if __name__ == '__main__':
    espeak_phonemizer = EspeakPhonemizer()
    phones = espeak_phonemizer('persönlich', language='de')
    print(phones)