
def get_one_instances_from_csv(instance_file):
    csv_file = open(instance_file)
    instances = csv.DictReader(csv_file, delimiter=',')
    for instance in instances:
        return instance

if __name__ == '__main__':
    # filename = 'mushroom_20.csv'

    filename = 'computer_data.csv'
    build_data_struct(filename)
