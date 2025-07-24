class Printable:

    # Define what is outputted when print this class object
    def __repr__(self):
        return str(self.__dict__)