import sys
import matplotlib.pyplot as plt
from utils import get_signal, get_annotations
from filters import apply_low_pass, apply_high_pass
from segment import get_squared_double_difference, get_peaks, get_peak_annotation, segment_signal_workflow


def test_filtering():
    signal = get_signal(102)
    low_pass = apply_low_pass(signal)
    high_pass = apply_high_pass(signal)
    figure, ax = plt.subplots(3)
    ax[0].set_title("original")
    ax[1].set_title("low pass")
    ax[2].set_title("high pass")
    ax[0].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
    ax[1].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
    ax[2].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
    ax[0].plot(signal[:10000])
    ax[0].plot()
    ax[1].plot(low_pass[:10000])
    ax[2].plot(high_pass[:10000])
    plt.show()


def test_get_squared_double_difference():
    signal = get_signal(100, 0, 1000)
    sdd = get_squared_double_difference(signal)
    plt.plot(signal)
    plt.plot(sdd)
    plt.show()


def test_peak_finding():
    signal = get_signal(102, 0, 5000)
    sdd = get_squared_double_difference(signal)
    peaks = get_peaks(sdd)
    plt.plot(signal)
    for peak in peaks:
        plt.axvline(peak, color="r", linestyle="dotted", alpha=0.5)
    plt.show()


def test_get_peak_annotation():
    signal = get_signal(100, 0, 5000)
    annotations = get_annotations(100, 0, 5000)
    sdd = get_squared_double_difference(signal)
    peaks = get_peaks(sdd)
    peaks, annotations = get_peak_annotation(peaks, annotations)
    plt.plot(signal)
    y = max(signal)
    for peak, annotation in zip(peaks, annotations):
        print(peak)
        plt.annotate(annotation, (peak, y))
    plt.show()


def test_segment_signal():
    signal = get_signal(102)
    annotations = get_annotations(102)
    segments, annotations = segment_signal_workflow(signal, annotations)
    for seg, anno in zip(segments, annotations):
        if anno != 'N':
            plt.plot(seg)
            plt.title(anno)
            plt.show()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
