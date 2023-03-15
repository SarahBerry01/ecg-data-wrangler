from random import shuffle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def balance_dataset_for_2_class(segments, annotations):
    n_class = [np.append(s, int(0))
               for s, a in zip(segments, annotations) if a == 'N']
    ab_class = [np.append(s, int(1))
                for s, a in zip(segments, annotations) if a != 'N']
    class_count = min(len(n_class), len(ab_class))
    shuffle(n_class)
    shuffle(ab_class)
    balanced_n_class = n_class[: class_count]
    balanced_ab_class = ab_class[: class_count]
    dataset = balanced_n_class + balanced_ab_class
    shuffle(dataset)
    return dataset


def balance_dataset_arrythmias(segments, annotations):
    ab_class_minor = [np.append(s, "X")
                      for s, a in zip(segments, annotations) if a in ["j", "e", "a", "S", "Q", "J", "E"]]
    ab_class = [np.append(s, ord(a))
                for s, a in zip(segments, annotations) if a != 'N'] + ab_class_minor
    shuffle(ab_class)
    return ab_class


def train_test_split(data, test_percentage=0.2):
    train_i = int(len(data) * (1-test_percentage))
    return data[: train_i], data[train_i:]


def arff_dump(data, file_path, class_options):
    columns = [str(i) for i in range(270)] + ["class"]
    df = pd.DataFrame(data, columns=columns)
    print("x")
    # if class_options == "0,1":
    df = df.astype({"class": 'int32'})
    # else:
    #     for col in columns[:-1]:
    #         df = df.astype({col: 'float32'})
    df = df.applymap(lambda x: round(x, 2) if isinstance(x, (float)) else x)
    print(type(df.iat[0, 0]))
    preamble = ["@relation ecg"] + [f"@attribute {i} real" for i in range(
        270)] + ["@attribute class {"+class_options+"}", "@data"]
    with open(file_path, "w") as fp:
        fp.writelines('\n'.join(preamble)+"\n")
    df.to_csv(file_path, header=False, index=False, mode='a')


def one_hot(segments):
    max_v = 3
    min_v = -3
    for segment in segments:
        pass
