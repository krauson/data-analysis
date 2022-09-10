class Get_input:
    def __init__(self, msg):
        self.train_data = self.get_filename(msg)

    def get_filename(self, msg):
        is_valid = False
        while not is_valid:
            filename = input(msg)
            try:
                with open(filename, 'r') as file:
                    print(file.read())
                    is_valid = True
            except FileNotFoundError:
                print("Couldn't find the file, try again")
        return filename