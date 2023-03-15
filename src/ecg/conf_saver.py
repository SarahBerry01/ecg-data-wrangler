import sys
import csv


def save(file, train_acc, test_acc):
    row = []
    with open(file, "r") as fp:
        for line in fp:
            if len(line)> 4:
                number = line.split(" ")[-1].strip()
                row.append(number)
    row += [train_acc, test_acc]
    with open("tested_confs.csv", "a", newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(row)




if __name__ == '__main__':
    save(sys.argv[1], sys.argv[2], sys.argv[3])
