import numpy as np
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
from random import shuffle

from utils import get_signal, get_annotations, get_all_signal_ids
from filters import apply_low_pass, apply_high_pass, apply_filters
from segment import get_squared_double_difference, get_peaks
from segment import get_peak_annotation, segment_signal_workflow


def test_filtering():
    ids = get_all_signal_ids()
    for sample_id in ids:
        signal, _ = get_signal(sample_id)
        low_pass = apply_low_pass(signal)
        high_pass = apply_high_pass(low_pass)
        figure, ax = plt.subplots(3)
        figure.set_size_inches(10, 5)
        ax[0].set_title("original")
        ax[1].set_title("low pass")
        ax[2].set_title("low pass and high pass")
        ax[0].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
        ax[1].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
        ax[2].axhline(y=0, color='black', linestyle='dotted', alpha=0.5)
        ax[0].plot(signal[:10000])
        ax[1].plot(low_pass[:10000])
        ax[2].plot(high_pass[:10000])
        plt.tight_layout()
        plt.savefig('plots/filtering/' + str(sample_id))
        plt.close()


def test_baseline_wander_removal():
    signal, _ = get_signal(234)
    low_pass = apply_low_pass(signal)
    high_pass = apply_high_pass(low_pass)
    figure, ax = plt.subplots(2)
    ax[0].set_title("id = 234")
    ax[1].set_title("low pass and high pass")
    ax[0].axhline(y=0, color='black', alpha=0.2)
    ax[1].axhline(y=0, color='black', alpha=0.2)
    ax[0].plot(signal[:6000], linewidth=0.6)
    ax[1].plot(high_pass[:6000], linewidth=0.6)
    x = list(range(6000))
    p = np.poly1d(np.polyfit(x, signal[:6000], 3))
    p_filtered = np.poly1d(np.polyfit(x, high_pass[:6000], 3))
    ax[0].plot(p(x))
    ax[1].plot(p_filtered(x))
    plt.tight_layout()
    plt.show()


def test_get_squared_double_difference():
    signal, _ = get_signal(100, 0, 1000)
    sdd = get_squared_double_difference(signal)
    plt.plot(signal)
    plt.plot(sdd)
    plt.show()


def test_get_peak_annotation():
    signal, _ = get_signal(100, 0, 5000)
    annotations = get_annotations(100, 0, 5000)
    filtered_signal = apply_filters(signal)
    sdd = get_squared_double_difference(filtered_signal)
    peaks = get_peaks(sdd)
    peaks, annotations = get_peak_annotation(peaks, annotations)
    plt.plot(filtered_signal)
    y = max(filtered_signal)
    for peak, annotation in zip(peaks, annotations):
        plt.annotate(annotation, (peak, y))
    plt.show()


def test_segment_signal():
    signal, _ = get_signal(102)
    annotations = get_annotations(102)
    filtered_signal = apply_filters(signal)
    segments, annotations = segment_signal_workflow(
        filtered_signal, annotations)
    for seg, anno in zip(segments, annotations):
        if anno != 'N':
            plt.plot(seg)
            plt.title(anno)
            plt.show()


def test_filtering_effect_on_segmenting():
    beat_anno = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V',
                 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?']
    signal, _ = get_signal(102)
    annotations = get_annotations(102)
    filtered_signal = apply_filters(signal)
    filtered_segments, filtered_annotations = segment_signal_workflow(
        filtered_signal, annotations)
    unfiltered_segments, unfiltered_annotations = segment_signal_workflow(
        signal, annotations)
    expected_segments = len([s for s in annotations.symbol if s in beat_anno])
    print(f"{expected_segments=}")
    print(f"{len(filtered_segments)=}")
    print(f"{len(unfiltered_segments)=}")


def get_class_distribution_post_process():
    print("== PREPARING SEGMENTS ==")
    ids = get_all_signal_ids()
    all_annotations = []
    for i, sample_id in enumerate(ids):
        print(int(i*100/len(ids)), "%")
        signals = get_signal(sample_id)
        annotations = get_annotations(sample_id)
        for signal in signals:
            filtered_signal = apply_filters(signal)
            segments, segment_annotations = segment_signal_workflow(
                filtered_signal, annotations)
            all_annotations += (segment_annotations)
    values, bins, bars = plt.hist(
        sorted(all_annotations), bins=np.arange(15)-0.5, alpha=0.5)
    plt.bar_label(bars, fontsize=8)
    plt.show()


def get_class_distribution():
    beat_anno = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V',
                 'r', 'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?']
    ids = get_all_signal_ids()
    all_annotations = []
    for i, sample_id in enumerate(ids):
        print(int(i*100/len(ids)), "%")
        annotations = get_annotations(sample_id).symbol
        annotations = [a for a in annotations if a in beat_anno]
        all_annotations += (annotations)
        all_annotations += (annotations)
    values, bins, bars = plt.hist(
        sorted(all_annotations), bins=np.arange(15)-0.5, alpha=0.5)
    plt.bar_label(bars, fontsize=8)
    plt.show()


def save_arrythmia_plots():
    dist = defaultdict(int)
    print("== PREPARING SEGMENTS ==")
    ids = get_all_signal_ids()
    all_segments = []
    all_annotations = []
    for i, sample_id in enumerate(ids):
        print(int(i*100/len(ids)), "%")
        signals = get_signal(sample_id)
        annotations = get_annotations(sample_id)
        for signal in signals:
            filtered_signal = apply_filters(signal)
            segments, segment_annotations = segment_signal_workflow(
                filtered_signal, annotations)
            all_segments += (segments)
            all_annotations += (segment_annotations)
    s = shuffle(zip(all_segments, all_annotations))
    for seg, anno in s:
        if dist[anno] < 2:
            plt.plot(seg)
            plt.title(anno)
            plt.savefig('plots/examples/' + str(ord(anno)) + str(dist[anno]))
            plt.close()
            dist[anno] += 1
    print(dist)


def test_sdd():
    signal, _ = get_signal(102, 0, 5000)
    filtered_signal = apply_filters(signal)
    sdd = get_squared_double_difference(filtered_signal)
    peaks = get_peaks(sdd)
    figure, ax = plt.subplots(2)
    ax[0].plot(filtered_signal)
    for peak in peaks:
        ax[0].axvline(peak, color="orange", linestyle="dashed", alpha=0.8)
    ax[1].plot(sdd)
    plt.show()
    plt.show()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
