from utils import get_all_signal_ids, get_signal, get_annotations
from filters import apply_filters
from segment import segment_signal_workflow
from data_writer import balance_dataset_for_2_class, arff_dump
from data_writer import train_test_split, balance_dataset_arrythmias
import matplotlib.pyplot as plt


def produce_files(major_classes, removed_classes, file_prefix, segments, annotations):
    print(f"=== Producing files for {major_classes} ===")
    dataset = balance_dataset_arrythmias(
        segments, annotations, major_classes, removed_classes)
    train, test = train_test_split(dataset)
    classes = major_classes + ["X"]
    classes_string = ",".join(classes)
    arff_dump(test, "output/"+file_prefix+"_test.arff",
              classes_string, 1, None)
    arff_dump(train, "output/"+file_prefix+"_train.arff",
              classes_string,  1, None)


def save_patient_samples_L(sample_id, segments, annotations):
    print(f"=== Producing files for {sample_id} L ===")
    dataset = balance_dataset_arrythmias(segments, annotations, ["L"], ["N"])
    path = "output/patients_L/"+str(sample_id)+".arff"
    if dataset:
        arff_dump(dataset, path, "L, X", 1, None)


def main():
    print("== PREPARING SEGMENTS ==")
    ids = get_all_signal_ids()
    all_segments = []
    all_annotations = []
    for i, sample_id in enumerate(ids):
        print(int(i*100/len(ids)), "%")
        signals = get_signal(sample_id)
        annotations = get_annotations(sample_id)
        channel_segments = []
        channel_annotations = []
        for i, signal in enumerate(signals):
            filtered_signal = apply_filters(signal)
            segments, segment_annotations = segment_signal_workflow(
                filtered_signal, annotations)
            channel_segments += (segments)
            channel_annotations += (segment_annotations)
        all_segments += (channel_segments)
        all_annotations += (channel_annotations)
        #save_patient_samples_L(sample_id, channel_segments, channel_annotations)

    #  Phase 1 Arrythmia vs normal

    # major_classes = ["N"]
    # removed_classes = ['']
    # produce_files(major_classes, removed_classes, "phase_1", all_segments, all_annotations)

    # # combined
    # removed_classes = ['N']
    # major_classes = ['L', 'R', 'V',  'F', '/', 'f', 'A']
    # produce_files(major_classes, removed_classes, "combined", all_segments, all_annotations)
    # # # Phase 2 Arrythmia classification

    major_classes = ["L"]
    removed_classes = ['N']
    produce_files(major_classes, removed_classes, "L_non_rel", all_segments, all_annotations)

    major_classes = ["R"]
    removed_classes = ['N', "L"]
    produce_files(major_classes, removed_classes, "R_non_rel", all_segments, all_annotations)

    major_classes = ["V"]
    removed_classes = ['N', "L", "R"]
    produce_files(major_classes, removed_classes, "V_non_rel", all_segments, all_annotations)

    major_classes = ["/"]
    removed_classes = ['N', "L", "R", "V"]
    produce_files(major_classes, removed_classes, "slash_non_rel", all_segments, all_annotations)

    major_classes = ["A"]
    removed_classes = ['N', "L", "R", "V", "/"]
    produce_files(major_classes, removed_classes, "A_non_rel", all_segments, all_annotations)

    major_classes = ["f"]
    removed_classes = ['N', "L", "R", "V", "/", "A"]
    produce_files(major_classes, removed_classes, "f_non_rel", all_segments, all_annotations)

    major_classes = ["F"]
    removed_classes = ['N', "L", "R", "V", "/", "A", "f"]
    produce_files(major_classes, removed_classes, "upper_F_non_rel", all_segments, all_annotations)

main()
