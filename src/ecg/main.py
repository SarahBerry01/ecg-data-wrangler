from utils import get_all_signal_ids, get_signal, get_annotations
from filters import apply_filters
from segment import segment_signal_workflow


def main():
    print("== PREPARING SEGMENTS ==")
    ids = get_all_signal_ids()
    for i, sample_id in enumerate(ids):
        print(int(i*100/len(ids)), "%")
        signal = get_signal(sample_id)
        annotations = get_annotations(sample_id)
        filtered_signal = apply_filters(signal)
        segments, segment_annotations = segment_signal_workflow(
            filtered_signal, annotations)


main()
