from utils import get_all_signal_ids, get_signal, get_annotations
from filters import apply_filters
from segment import segment_signal_workflow
from data_writer import data_formatter, arff_dump
from data_writer import train_test_split, balance_train_data
import matplotlib.pyplot as plt


def produce_files(major_classes, removed_classes, file_prefix, segments, annotations):
    print(f"=== Producing files for {major_classes} ===")
    dataset = data_formatter(
        segments, annotations, major_classes, removed_classes)

    train, test = train_test_split(dataset)
    classes = major_classes + ["X"]
    classes_string = ",".join(classes)
    arff_dump(test, "output/"+file_prefix+"_test.arff",
              classes_string, 1, None)
    arff_dump(train, "output/"+file_prefix+"_train.arff",
              classes_string,  1, None)

    if file_prefix != 'combined':
        balanced_train = balance_train_data(train, major_classes)
        arff_dump(balanced_train, "output/balanced/"+file_prefix+"_train.arff",
                  classes_string,  1, None)


def save_patient_samples(sample_id, segments, annotations, major, removed):
    print(f"=== Producing files for {sample_id} L ===")
    dataset = data_formatter(segments, annotations, [major], removed)
    path = "output/patients_"+major+"/"+str(sample_id)+".arff"
    if dataset:
        classes = major + ",X"
        arff_dump(dataset, path, classes, 1, None)


def main():
    print("== PREPARING SEGMENTS ==")
    ids = get_all_signal_ids()
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
        # save data for L patient wise
        # save_patient_samples(
        #     sample_id, segments, segment_annotations, "L", ["N"])
        save_patient_samples(
            sample_id, segments, segment_annotations, "N", [])

    # #  Phase 1 Arrythmia vs normal

    # major_classes = ["N"]
    # removed_classes = ['']
    # produce_files(major_classes, removed_classes, "phase_1", all_segments, all_annotations)

    # # # # combined
    # removed_classes = ['N']
    # major_classes = ['L', 'R', 'V',  'F', '/', 'f', 'A']
    # produce_files(major_classes, removed_classes,
    #               "combined", all_segments, all_annotations)

    # # # # Phase 2 Arrythmia classification

    # major_classes = ["L"]
    # removed_classes = ['N']
    # produce_files(major_classes, removed_classes,
    #               "L", all_segments, all_annotations)

    # major_classes = ["R"]
    # removed_classes = ['N', "L"]
    # produce_files(major_classes, removed_classes,
    #               "R", all_segments, all_annotations)

    # major_classes = ["V"]
    # removed_classes = ['N', "L", "R"]
    # produce_files(major_classes, removed_classes,
    #               "V", all_segments, all_annotations)

    # major_classes = ["/"]
    # removed_classes = ['N', "L", "R", "V"]
    # produce_files(major_classes, removed_classes,
    #               "slash", all_segments, all_annotations)

    # major_classes = ["A"]
    # removed_classes = ['N', "L", "R", "V", "/"]
    # produce_files(major_classes, removed_classes,
    #               "A", all_segments, all_annotations)

    # major_classes = ["f"]
    # removed_classes = ['N', "L", "R", "V", "/", "A"]
    # produce_files(major_classes, removed_classes,
    #               "f", all_segments, all_annotations)

    # major_classes = ["F"]
    # removed_classes = ['N', "L", "R", "V", "/", "A", "f"]
    # produce_files(major_classes, removed_classes,
    #               "upper_F", all_segments, all_annotations)


main()
