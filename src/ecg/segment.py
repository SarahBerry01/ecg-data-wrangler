import numpy as np


def get_squared_double_difference(signal: list[float]) -> list[float]:
    """ calculate squared double difference
    as describe in https://www.sciencedirect.com/science/article/pii/S2212017312004227?via%3Dihub
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
