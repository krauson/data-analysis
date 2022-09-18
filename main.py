import copy
import csv
import logging

from data_funcs import *

logging.basicConfig(level=logging.DEBUG)


def get_possible_classes(instances: list[dict]):
    possible_classes = []
    for instance in instances:
        possible_classes.append(instance['class'])
    possible_classes = set(possible_classes)
    # print(possible_classes)
    return possible_classes


def get_instances_from_csv(filename: str):
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


def fill_model(filled_data, model, uniq_vals):
    for cls in model:
        for col in model[cls]:
            col_values = filled_data[cls][col]
            num_of_instances = len(col_values)
            for uniq_val in uniq_vals[col]:
                val_counter = col_values.count(uniq_val)
                # logging.debug(f"for class {cls} val {uniq_val} counter {val_counter}")
                if val_counter == 0:
                    numerator = 1
                    denominator = num_of_instances + 1
                else:
                    numerator = val_counter
                    denominator = num_of_instances

                model[cls][col][uniq_val] = numerator / denominator

    print("model:", model)
    return model


def get_num_of_instance_per_category(data):
    num_of_instances = {}
    for cls in data:
        for col_name in data[cls].keys():
            col_vals = data[cls][col_name]
            cls_num_of_instances = len(col_vals)
            num_of_instances[cls] = cls_num_of_instances
            # logging.debug(f"The number of instances for {cls} class is {cls_num_of_instances}")

    # print("num_of_instances", num_of_instances)
    return num_of_instances


def calc_chances_for_each_cls(frequencies: dict):
    chances_to_cls = {cls: 1 for cls in frequencies}

    for cls in frequencies:
        for i in range(len(frequencies[cls])):
            chances_to_cls[cls] *= frequencies[cls][i]

    # print(f"chances for classes: {chances_to_cls}")
    return chances_to_cls


def get_bigger_chances_cls(chances_for_each_cls) -> str:
    biggest = max(chances_for_each_cls, key = chances_for_each_cls.get)
    # print(biggest)
    return biggest
    # for cls in chances_for_each_cls:



def classify_one_instance(model, filled_data, instance):
    num_of_instances_per_cls = get_num_of_instance_per_category(filled_data)
    frequencies = {cls: [] for cls in model}
    print("instance", instance)

    for cls in frequencies:
        for col in instance:
            col_val = instance[col]
            frequencies[cls].append(model[cls][col][col_val])

    total_instances = sum([num_of_instances_per_cls[cls] for cls in num_of_instances_per_cls])
    # print(total_instances)
    for cls in frequencies:
        cls_frequncy = num_of_instances_per_cls[cls] / total_instances
        frequencies[cls].append(cls_frequncy)

    print("frequencies:", frequencies)

    chances_for_each_cls = calc_chances_for_each_cls(frequencies)

    return chances_for_each_cls

    # logging.debug(f"")
    #
    # biggest_chances_cls = get_biggest_chances_cls(chances_for_each_cls)
    #
    # # biggest_chances_cls
def get_num_of_instances(instances):
    counter = 0
    for instance in instances:
        counter += 1
    logging.info(f"number of instances: {counter}")
    return counter


def get_uniq_vals_per_col(filled_data, col_names):
    uniq_vals = {col_name: set() for col_name in col_names}
    for cls in filled_data:
        for col_name in filled_data[cls]:
            cur_col = filled_data[cls][col_name]
            for val in cur_col:
                uniq_vals[col_name].add(val)

    # print(f"unique vals: {uniq_vals}")
    return uniq_vals


def build_model_struct(empty_data: dict, uniq_vals: dict):
    model = copy.deepcopy(empty_data)
    for cls in model:
        for col_name in model[cls]:
            col_uniq_vals = uniq_vals[col_name]
            model[cls][col_name] = {uniq_val: 0 for uniq_val in col_uniq_vals}

    return model


def check_one_instance(model, filled_data, instance_file):
    instance = get_one_instances_from_csv(instance_file)
    chances_for_each_cls = classify_one_instance(model, filled_data, instance)
    output_instance_results(chances_for_each_cls)

def output_model_accuracy(is_model_correct_list):
     num_of_true = is_model_correct_list.count(True)
     true_ratio = num_of_true / len(is_model_correct_list)

     print(f"The model was correct in {true_ratio:.2%} of cases")



def check_dataset(model, filled_data, dataset_file):
    instances = get_instances_from_csv(dataset_file)
    is_model_correct_list = []
    for instance in instances:
        real_class = instance['class']
        del instance['class']
        chances_for_each_cls = classify_one_instance(model, filled_data, instance)
        model_cls = get_bigger_chances_cls(chances_for_each_cls)
        is_model_correct = model_cls == real_class
        is_model_correct_list.append(is_model_correct)
        # print(f"is model correct list: {is_model_correct_list}")

    output_model_accuracy(is_model_correct_list)

def output_instance_results(chances_for_each_cls):
    for cls in chances_for_each_cls:
        cls_precentages = chances_for_each_cls[cls] * 100
        print(f"The chances for classifier '{cls}' are: {cls_precentages:.3f}%")


def classify_dataset(model, test_data, filled_data):
    pass


def main(train_data_file: str, test_file: str):
    """"build the structure of the data, primary dict, which every value of it is a unique classifier which is another key
    to the possible columns in the data, which are another key to the all the possible values in that column"""
    empty_data = {}
    instances = get_instances_from_csv(train_data_file)
    col_names = get_col_names(instances)

    # num_of_instances = get_num_of_instances(instances)
    add_classes(empty_data, instances)

    add_columns_to_data(empty_data, col_names)

    instances = get_instances_from_csv(train_data_file)
    """" for unknown reason the instancs object is changed in the get_possible_classes so I have to regenerate it"""

    logging.debug(f"data {empty_data}")

    filled_data = copy.deepcopy(empty_data)

    fill_data_with_vals(filled_data, instances)

    uniq_vals = get_uniq_vals_per_col(filled_data, col_names)

    model = build_model_struct(empty_data, uniq_vals)
    logging.debug(f"empty model: {model}")

    logging.debug(filled_data)
    fill_model(filled_data, model, uniq_vals)

    choice = input("Enter i to check classifaction for one instance,\notherwise type 'd' to check model succuss precentages on dataset: ")

    if choice == 'i':
        check_one_instance(model, filled_data, test_file)

    elif choice == 'd':
        check_dataset(model, filled_data, test_file)

    else:
        print("Invalid input exit..")
        return

def get_one_instances_from_csv(instance_file):
    csv_file = open(instance_file)
    instances = csv.DictReader(csv_file, delimiter=',')
    for instance in instances:
        return instance

def get_instances_from_csv(dataset_file):
    csv_file = open(dataset_file)
    instances = csv.DictReader(csv_file, delimiter=',')
    return instances

if __name__ == '__main__':
    # filename = 'mushroom_20.csv'

    comp_train_data_file = 'computer_data.csv'
    mush_train_data_file = 'mushrooms_70%.csv'
    phising_train_data_file = 'phising70.csv'

    comp_instance_file = 'comp_instance.csv'
    mush_dataset_test = '30.csv'
    phish_dataset_test = 'phising30.csv'

    main(comp_train_data_file, comp_instance_file)
    # main(mush_train_data_file, mush_dataset_test)
    # main(phising_train_data_file, phish_dataset_test)

