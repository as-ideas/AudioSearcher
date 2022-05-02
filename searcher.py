from typing import List, Tuple
import regex


class Searcher:

    def __call__(self,
                 transcription: List[Tuple[str, float]],
                 query: str,
                 language: str = 'en',
                 max_char_errors: int = 3) -> List[Tuple[float, float]]:

        """
        Search for the substring and return positions
        :parameter transcription a list of tuples with the character and start time, eg [('a', 0.2), ('b', 0.4)]
        :parameter query: a free text user input[]
        :returns List of tuples with the start time and end time of the search result, eg [(0.1, 0.2), (0.5, 0.6)]
        """

        result_durations = []

        # reconstruct input
        reconstructed_sample = [x[0] for x in transcription]
        reconstructed_sample = ''.join(reconstructed_sample).lower()

        query = regex.compile(query + '{' + f'e<={max_char_errors}' + '}')
        # do search
        found_durations = [(m.start(0), m.end(0)) for m in regex.finditer(query, reconstructed_sample)]

        for duration in found_durations:
            start_pos, end_pos = duration
            durations = [x[1] for x in transcription[start_pos:end_pos]]
            result_durations.append((durations[0], durations[-1]))

        return result_durations

if __name__ == '__main__':
    sample_phonemized = [("h", 0.1), ("ə", 0.3), ("l", 0.5), ("ʊ", 0.7), (" ", 0.8),
                         ("w", 0.3), ("ɜː", 0.5), ("l", 0.7), ("d", 0.8)]
    query = "wɜːlz"

    searcher = Searcher()
    found_durations = searcher(sample_phonemized, query, max_char_errors=1)
    print(found_durations)