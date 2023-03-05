from random import shuffle
import numpy as np
import pandas as pd


def balance_dataset_for_2_class(segments, annotations):
    n_class = [np.append(s, int(0))
               for s, a in zip(segments, annotations) if a == 'N']
    ab_class = [np.append(s, int(1))
                for s, a in zip(segments, annotations) if a != 'N']
    class_count = min(len(n_class), len(ab_class))
    shuffle(n_class)
    shuffle(ab_class)
    balanced_n_class = n_class[:class_count]
    balanced_ab_class = ab_class[:class_count]
    dataset = balanced_n_class + balanced_ab_class
    shuffle(dataset)
    return dataset


def train_test_split(data, test_percentage=0.2):
    train_i = int(len(data) * (1-test_percentage))
    return data[:train_i], data[train_i:]


def arff_dump(data, file_path, class_options):
    columns = [str(i) for i in range(270)] + ["class"]
    df = pd.DataFrame(data, columns=columns)
    print(df)
    df = df.astype({"class": 'int32'})
    preamble = ["@relation ecg"] + [f"@attribute {i} real" for i in range(
        270)] + ["@attribute class {"+class_options+"}", "@data"]
    with open(file_path, "w") as fp:
        fp.writelines('\n'.join(preamble)+"\n")
    df.to_csv(file_path, header=False, index=False, mode='a')
