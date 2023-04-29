from random import shuffle
import numpy as np
import pandas as pd


def data_formatter(segments, annotations, major_classes, removed_classes):
    major_dataset = ([np.append(s, a) for s, a in zip(
        segments, annotations) if a in major_classes])
    minor_dataset = [np.append(s, "X") for s, a in zip(
        segments, annotations) if a not in major_classes and a not in removed_classes]
    print(f"{len(major_dataset)} instances in {major_classes}, {len(minor_dataset)} instances in X")
    dataset = major_dataset + minor_dataset
    shuffle(dataset)
    return dataset

def balance_train_data(train, major_classes):
    major_dataset = [s for s in train if s[-1] in major_classes]
    minor_dataset = [s for s in train if s[-1] == 'X' ]
    class_count = min(len(major_dataset), len(minor_dataset))
    balanced = major_dataset[:class_count] + minor_dataset[:class_count]
    print("balanced len", len(balanced))
    shuffle(balanced)
    return balanced


def train_test_split(data, test_percentage=0.2):
    train_i = int(len(data) * (1-test_percentage))
    return data[: train_i], data[train_i:]


def arff_dump(data, file_path, class_options, freq, rnd):
    print(f" Writing to {file_path}")
    columns = [str(i) for i in range(len(data[0])-1)]
    columns_with_class = columns + ["class"]
    df = pd.DataFrame(data, columns=columns_with_class)
    # if rnd is not None:
    #     df[columns] = df[columns].round(rnd)
    # df = df.loc[:, columns[::freq] + ["class"]]
    if class_options == "0,1":
        df = df.astype({"class": 'int32'})
    # else:
    #     for col in columns[:-1]:
    #         df = df.astype({col: 'float32'})
    # df = df.applymap(lambda x: round(x, 2) if isinstance(x, (float)) else x)
    # print(type(df.iat[0, 0]))
    preamble = ["@relation ecg"] + [f"@attribute {i} real" for i in range(
        len(df.columns)-1)] + ["@attribute class {"+class_options+"}", "@data"]
    with open(file_path, "w") as fp:
        fp.writelines('\n'.join(preamble)+"\n")
    df.to_csv(file_path, header=False, index=False, mode='a')
