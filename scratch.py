import copy
import csv
import logging

logging.basicConfig(level=logging.DEBUG)


def get_possible_classes(instances: list[dict]):
    possible_classes = []
    for instance in instances:
        possible_classes.append(instance['class'])
    possible_classes = set(possible_classes)
    # print(possible_classes)
    return possible_classes


def get_instances_from_csv(filename: str):
    # with open(filename, 'r') as csv_file:
    csv_file = open(filename)
    instances = csv.DictReader(csv_file, delimiter=',')
    return instances


def add_classes(data, instances):
    """add the unique classifiaction as keys to the data dictionary for that classifcation """

    possible_classes = get_possible_classes(instances)

    for cls in possible_classes:
        data[cls] = {}
    for instance in instances:
        logging.debug(instance)





def build_model(data, model):
    for cls in data:
        for col in data[cls]:
            model[cls][col] = {}
            col_vals = data[cls][col]
            col_unique_vals = set(col_vals)
            num_of_instances = len(col_vals)
            for val in col_unique_vals:
                val_counter = col_vals.count(val)
                # logging.debug(f"for class {cls} val {val} counter {val_counter}")
                if val_counter == 0:
                    numerator = 1
                    denominator = num_of_instances + 1
                else:
                    numerator = val_counter
                    denominator = num_of_instances

                model[cls][col][val] = numerator / denominator

    print("model:", model)
    return model



def classify_one_instance(model, instance:dict):
    frequencies = []
    for col in instance:
        frequencies = model[]

def get_num_of_instances(instances):
    counter = 0
    for instance in instances:
        counter += 1
    logging.info(f"number of instances: {counter}")
    return counter


def build_data_struct(col_names):
    """"build the structure of the data, primary dict, which every value of it is a unique classifier which is another key
    to the possible columns in the data, which are another key to the all the possible values in that column"""
    data = {}
    instances = get_instances_from_csv(filename)
    col_names = get_col_names(instances)

    # num_of_instances = get_num_of_instances(instances)
    add_classes(data, instances)

    add_columns_to_data(data, col_names)

    instances = get_instances_from_csv(filename)
    """" for unknown reason the instancs object is changed in the get_possible_classes so I have to regenerate it"""

    logging.debug(f"data {data}")

    model = copy.deepcopy(data)

    fill_data_with_vals(data, instances)
    build_model(data, model)

if __name__ == '__main__':
    # filename = 'mushroom_20.csv'
    filename = 'computer_data.csv'
    build_data_struct(filename)
