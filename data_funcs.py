from classify import classify_instance
import csv
import copy

def get_col_names(filename:str):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        col_names = list(csv_reader)[0]
        return col_names


def get_col_vals(filename: str):
    file = open(filename, 'r')
    lines_as_dicts = csv.DictReader(file)

    col_names = get_col_names(filename)
    col_values = {}

    for line in lines_as_dicts:
        for col in col_names:
            if col not in col_values:
                col_values[col] = []
            col_values[col].append(line[col])

    del col_values['class']
    return col_values


def get_col_unique_vals(all_vals_in_each_col:dict) ->dict:
    col_unique_vals = copy.deepcopy(all_vals_in_each_col)
    for col_name in col_unique_vals:
        col_unique_vals[col_name] = set(all_vals_in_each_col[col_name])

    return col_unique_vals


def build_data_struct(col_names, unique_vals):
    data = {}
    for name in col_names:
        data[name] = {}

    del col_names[0]  # delete 'class' col name
    for col_name in col_names:
        for unique_val in unique_vals[col_name]:
            data[col_name][unique_val] = {}
    return data

def print_num_of_rows(data_vals):
    edible_vals = data_vals[0]
    poison_vals = data_vals[1]

    edible_rows = len(edible_vals['cap-shape'])
    print("Num of instances in edible:", edible_rows)

    poison_rows = len(poison_vals['cap-shape'])
    print("Num of instances in poison:", poison_rows)
    return

def calc_data(col_values:dict, data: dict):
    num_of_rows = len(col_values['cap-shape'])
    # print("Num of instances:", num_of_rows)
    for col_name in col_values:
        for uniq_val in data[col_name]:
            count_of_uniq_val = col_values[col_name].count(uniq_val)
            if count_of_uniq_val == 0:
                adjusted_count = 1
                adjusted_num_of_rows = num_of_rows + 1
                frequency = adjusted_count / adjusted_num_of_rows
            else:
                frequency = count_of_uniq_val / num_of_rows
            # print(f"In {col_name} count of {uniq_val}: {count_of_uniq_val} frequency:{frequency}")
            data[col_name][uniq_val] = frequency
    return


def check_model(data: tuple[dict], filname: str, data_vals):
    with open(filname) as sample_file:
        lines_to_test = csv.DictReader(sample_file)
        model_check = []

        for line in lines_to_test:
            real_class = line['class']
            del line['class']
            model_class = classify_instance(data, line, data_vals)
            is_model_correct = model_class == real_class
            model_check.append(is_model_correct)

        num_of_true = model_check.count(True)
        succuss_precentages = num_of_true / len(model_check)

        print("model_check:", model_check)
        print("model_check length:", len(model_check))
        print(f"succuss_precentages: {succuss_precentages * 100:.2f}%")


def get_instance(filename):
    with open(filename, 'r') as instance_file:
        instance = csv.DictReader(instance_file)
        instance = list(instance)[0]
        return instance
