from interface import Interface


class WriterListner(Interface):
    def on_duplicate_record(self, component, kind, record, stack_trace):
        pass

    def on_unique_record(self, component, kind, record, stack_trace):
        pass

    def on_stack_trace(self, component, kind, record, stack_trace):
        pass