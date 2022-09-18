import os
from data_funcs import get_col_names


class Csv:
    def __init__(self):
        self.classifier
        self.data

def delete_classified_files(classified_files: tuple) -> None:
    for filename in classified_files:
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("The file does not exist")
    return


def split_csv_by_classification(filename: str) -> tuple[list]:
    """creates two lists of string, edible lists and poison list"""
    with open(filename) as csv_file:
        lines = csv_file.readlines()[1:]
    edible = []
    poisonous = []
    for line in lines:
        if line.startswith('e'):
            edible.append(line)
        else:
            poisonous.append(line)

    return edible, poisonous

def create_two_csv_files(edible, poisonous ,filename):
    col_names = get_col_names(filename)
    col_names[-1] += '\n'
    col_names = ",".join(col_names)

    csv_names = ("edible.csv", 'poisonous.csv')
    with open('edible.csv', 'w') as edible_file:
        edible_file.write(col_names)
        for line in edible:
            edible_file.write(line)

    with open('poisonous.csv', 'w') as poisonous_file:
        poisonous_file.write(col_names)
        for line in poisonous:
            poisonous_file.write(line)
    return csv_names