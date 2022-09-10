def classify_one_instance(data, instance: list[dict], data_vals):
    edible_vals = data_vals[0]
    poison_vals = data_vals[1]

    edible_rows = len(edible_vals['cap-shape'])
    # print("Num of instances in edible:", edible_rows)

    poison_rows = len(poison_vals['cap-shape'])
    # print("Num of instances in poison:", poison_rows)

    edible_precentages = edible_rows / (edible_rows + poison_rows)
    poison_precentages = poison_rows / (edible_rows + poison_rows)

    edible_data = data[0]
    poisonous_data = data[1]
    chance_to_be_edible = []
    chance_to_be_poison = []

    # print("instance:",instance)

    # build edible model
    for col_name in edible_data:
        possible_vals = edible_data[col_name]
        for uniq_val in possible_vals:
            if uniq_val == instance[col_name]:
                uniq_val_precentages = edible_data[col_name][uniq_val]
                chance_to_be_edible.append(uniq_val_precentages)

    # build edible model

    for col_name in poisonous_data:
        possible_vals = poisonous_data[col_name]
        for uniq_val in possible_vals:
            if uniq_val == instance[col_name]:
                uniq_val_precentages = poisonous_data[col_name][uniq_val]

                chance_to_be_poison.append(uniq_val_precentages)

    chance_to_be_edible.append(edible_precentages)
    chance_to_be_poison.append(poison_precentages)

    edible_chances = 1
    for chance in chance_to_be_edible:
        edible_chances *= chance

    poisonous_chances = 1
    for chance in chance_to_be_poison:
        poisonous_chances *= chance

    print(f"chance to be edible: {edible_chances}")
    print(f"chance to be poison: {poisonous_chances}")

    if chance_to_be_edible >= chance_to_be_poison:
        return 'e'
    else:
        return 'p'

def classify_instance(data, instance: list[dict], data_vals):

    edible_vals = data_vals[0]
    poison_vals = data_vals[1]

    edible_rows = len(edible_vals['cap-shape'])
    # print("Num of instances in edible:", edible_rows)

    poison_rows = len(poison_vals['cap-shape'])
    # print("Num of instances in poison:", poison_rows)

    edible_precentages = edible_rows / (edible_rows + poison_rows)
    poison_precentages = poison_rows / (edible_rows + poison_rows)


    edible_data = data[0]
    poisonous_data = data[1]
    chance_to_be_edible = []
    chance_to_be_poison = []

    # print("instance:",instance)

    # build edible model
    for col_name in edible_data:
        possible_vals = edible_data[col_name]
        for uniq_val in possible_vals:
            if uniq_val == instance[col_name]:
                uniq_val_precentages = edible_data[col_name][uniq_val]
                chance_to_be_edible.append(uniq_val_precentages)

    # build edible model

    for col_name in poisonous_data:
        possible_vals = poisonous_data[col_name]
        for uniq_val in possible_vals:
            if uniq_val == instance[col_name]:
                uniq_val_precentages = poisonous_data[col_name][uniq_val]

                chance_to_be_poison.append(uniq_val_precentages)

    chance_to_be_edible.append(edible_precentages)
    chance_to_be_poison.append(poison_precentages)

    edible_chances = 1
    for chance in chance_to_be_edible:
        edible_chances *= chance


    poisonous_chances = 1
    for chance in chance_to_be_poison:
        poisonous_chances *= chance

    # print("poisonous_chances:", poisonous_chances)
    # print("edible_chances:", edible_chances)
    #
    # print(f"chance to be edible: {chance_to_be_edible}")
    # print(f"chance to be poison: {chance_to_be_poison}")

    if chance_to_be_edible >= chance_to_be_poison:
        return 'e'
    else:
        return 'p'
