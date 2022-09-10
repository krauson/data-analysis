from classify import classify_one_instance
from file_funcs import delete_classified_files, split_csv_by_classification, create_two_csv_files
from data_funcs import *
from get_input_class import Get_input


def main():
    # get file names
    
    # intial_msg = "Enter the name of the data file to train the Naive baysian model: "
    # data_obj = Get_input(intial_msg)
    # data_file = data_obj.train_data

    data_file = "mushrooms_70%.csv"
    data_to_test_file = "mushrooms 30%.csv"

    # data_file = 'data_20.csv'
    # data_to_test_file = 'data_test5.csv'

    # split data to two classified files
    edible, poisonous = split_csv_by_classification(data_file)
    classified_files = create_two_csv_files(edible, poisonous, data_file)

    # build data structures:
    col_names = get_col_names(data_file)
    # print('col_names', col_names)
    edible_vals = get_col_vals('edible.csv')
    poisonous_vals = get_col_vals('poisonous.csv')
    data_vals = (edible_vals, poisonous_vals)
    col_values = get_col_vals(data_file)
    unique_vals = get_col_unique_vals(col_values)
    print_num_of_rows(data_vals)
    # print("edible-vals",edible_vals)
    # print("poison-vals",poisonous_vals)
    # print("uniquie values", unique_vals)
    edible_data = build_data_struct(col_names, unique_vals)
    poisonous_data = copy.deepcopy(edible_data)
    data = (edible_data, poisonous_data)
    # print(f"edible_data {edible_data}")
    # print(f"poisonous_data {poisonous_data}")

    # build model:
    calc_data(edible_vals, edible_data)
    calc_data(poisonous_vals, poisonous_data)
    # print("edible_data", edible_data)
    # print("poisonous_data", poisonous_data)

    choice = input("For checking classifactiob for one instance type 'i',\
otherwise type 'd' to check model succuss precentages: ")

    if choice == 'i':
        instance_file = "instance.csv"
        # instance_msg = "Enter the filename with one entity to classify according to the model: "
        # instance_file = data_obj.get_filename(instance_msg)
        instance = get_instance(instance_file)
        classify_one_instance(data, instance, data_vals)

    else:
        check_model(data, data_to_test_file, data_vals)

    delete_classified_files(classified_files)
    return


if __name__ == '__main__':
    main()
