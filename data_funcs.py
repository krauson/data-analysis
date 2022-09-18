import logging


def add_columns_to_data(data, col_names):
    for cls in data:
        for col_name in col_names:
            data[cls][col_name] = []


def get_col_names(instances):
    for instance in instances:
        col_names = list(instance.keys())
        col_names.remove('class')
        return col_names



def fill_data_with_vals(data, instances):
    for instance in instances:
        instance_cls = instance['class']
        del instance['class']
        for col_name, value in instance.items():
            data[instance_cls][col_name].append(value)

    return data
    # logging.debug(data)