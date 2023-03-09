import numpy as np


def get_squared_double_difference(signal: list[float]) -> list[float]:
    """ calculate squared double difference
    as describe in
    https://www.sciencedirect.com/science/article/pii/S2212017312004227?via%3Dihub
    """

    def _dl(signal, i):
        return signal[i+1] - signal[i]

    def _d2(signal, j):
        return _dl(signal, j+1) - _dl(signal, j)

    def _d(signal, j):
        return _d2(signal, j) ** 2

    return [_d(signal, j)*100 for j in range(len(signal)-2)]


def get_peaks(difference_ar: list[float]) -> list[int]:
    """
    Get peak indecies and values from a calculated difference array
    """
    threshold = np.percentile(difference_ar, 97)
    peak_indices = [i for i, v in enumerate(difference_ar) if v > threshold]

    def _filter_peaks(peaks: list[int]) -> list[int]:
        """ peak finding returns many points on the same peak. 
        This just takes the first in that area over 100 samples.
        """

        filtered_peaks = [peaks[0]]
        for i in range(1, len(peaks)):
            if peaks[i] - filtered_peaks[-1] > 100:
                filtered_peaks.append(peaks[i])
        return filtered_peaks
    return _filter_peaks(peak_indices)


def get_peak_annotation(peaks, annotations):
    '''
    Get list of peaks and list of corresponding annotations
    '''
    beat_anno = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V',
                 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?']
    filtered_peaks = []
    filtered_annotations = []
    for peak in peaks:
        annotation_symbols = zip(annotations.sample, annotations.symbol)
        for sample, symbol in annotation_symbols:
            if abs(sample - peak) < 35 and symbol in beat_anno:
                filtered_peaks.append(peak)
                filtered_annotations.append(symbol)
    return filtered_peaks, filtered_annotations


def segment_signal(signal, peaks, annotations) -> list[list[float]]:
    """split signal into single cycles

    Args:
        signal (list[float]): input signal
        annotated_peaks: tuple of indecies of peaks and annotation

    Returns:
        list[list[float]]: a list containing each of the segments.
    """

    segments = []
    segment_annotations = []
    for peak, annotation in zip(peaks, annotations):
        window_start = peak - 135
        window_end = peak + 135
        if window_start >= 0 and window_end <= len(signal):
            segment = signal[window_start:window_end]
            segments.append(segment)
            segment_annotations.append(annotation)
    return segments, segment_annotations


def segment_signal_workflow(signal, annotations):
    sdd = get_squared_double_difference(signal)
    peaks = get_peaks(sdd)
    f_peaks, f_annotations = get_peak_annotation(peaks, annotations)
    segments, segment_annotations = segment_signal(
        signal, f_peaks, f_annotations)
    return segments, segment_annotations
