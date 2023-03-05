from utils import get_all_signal_ids, get_signal, get_annotations
from filters import apply_filters
from segment import segment_signal_workflow
from data_writer import balance_dataset_for_2_class, arff_dump


def main():
    print("== PREPARING SEGMENTS ==")
    ids = get_all_signal_ids()[:2]
    all_segments = []
    all_annotations = []
    for i, sample_id in enumerate(ids):
        print(int(i*100/len(ids)), "%")
        signal = get_signal(sample_id)
        annotations = get_annotations(sample_id)
        filtered_signal = apply_filters(signal)
        segments, segment_annotations = segment_signal_workflow(
            filtered_signal, annotations)
        all_segments += (segments)
        all_annotations += (segment_annotations)
    dataset = balance_dataset_for_2_class(all_segments, all_annotations)
    arff_dump(dataset, "output/1.arff", "0,1")


main()
