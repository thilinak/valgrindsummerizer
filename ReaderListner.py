from interface import Interface


class ReaderListner(Interface):
    def on_read_data(self, file_data):
        pass