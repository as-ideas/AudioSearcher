from typing import List
import re


def search(transcription: str, query: str) -> List:
    """
    Search for the substring and return positions
    :parameter transcription a list of tuples with the character and start time, eg [('a', 0.2), ('b', 0.4)]
    :parameter query: a free text user input[]
    :returns List of tuples with the start time and end time of the search result, eg [(0.1, 0.2), (0.5, 0.6)]
    """

    result_durations = []

    # reconstruct input
    reconstructed_sample = [x[0] for x in transcription]
    reconstructed_sample = "".join(reconstructed_sample).lower()

    # clean user input
    cleaned_query = "".join([x for x in query.lower() if x.isalnum()])

    # do search
    found_durations = [(m.start(0), m.end(0)) for m in re.finditer(cleaned_query, reconstructed_sample)]

    for duration in found_durations:
        start_pos, end_pos = duration
        durations = [x[1] for x in transcription[start_pos:end_pos]]
        result_durations.append((durations[0], durations[-1]))

    return result_durations
