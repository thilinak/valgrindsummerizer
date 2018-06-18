from interface import Interface


class WriterListner(Interface):
    def on_duplicate_record(self, component, kind, record):
        pass

    def on_unique_record(self, component, kind, record):
        pass
