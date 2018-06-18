from difflib import SequenceMatcher
from xml.etree.ElementTree import fromstring, tostring

from LogsReader import LogsReader
from ReaderCacheObserver import ReaderCacheObserver
from XmlReader import XmlReader
from XmlWriter import XmlWriter


class Summerizer(ReaderCacheObserver):
    def __init__(self, _writer_listner):
        super(Summerizer, self).__init__()
        self.reader_cache.subscribe(self, "error")
        self.stack_traces = {}
        self.writer_listner = _writer_listner
        self.interested_kinds = ['InvalidRead', 'Leak_DefinitelyLost', 'Leak_PossiblyLost', 'SyscallParam', 'UninitCondition', 'UninitValue']

    def update(self, element, component_name):
        stack_trace = Summerizer.construct_stacktrace(element)

        kind = element.find("./kind").text

        if (self.is_interested_kind(kind) == False):
            return

        element_str = tostring(element)
        if (self.is_duplicate(stack_trace, kind) == False):
            self.writer_listner.on_unique_record(component_name, kind, element_str)
        else:
            self.writer_listner.on_duplicate_record(component_name, kind, element_str)

    def is_interested_kind(self, kind):
        for _kind in self.interested_kinds:
            if _kind == kind:
                return True
        return False

    def is_duplicate(self, stack_trace, kind):
        for _kind, previouse_stack_traces in self.stack_traces.items():
            if _kind != kind:
                continue
            for previouse_stack_trace in previouse_stack_traces:
                ratio = SequenceMatcher(None, stack_trace, previouse_stack_trace).ratio()
                if ratio > 0.6:
                    return True
        try:
            self.stack_traces[kind] = [stack_trace] + self.stack_traces[kind]
        except KeyError:
            self.stack_traces[kind] = [stack_trace]
        return False

    @staticmethod
    def construct_stacktrace(errorElement):
        stack_trace = ""
        frames = errorElement.findall("./stack/frame")

        for frame in frames:
            stack_frame = frame.find("./fn")
            if stack_frame is None:
                continue
            else:
                stack_frame = stack_frame.text

            file_name = frame.find("./file")
            if file_name is None:
                file_name = ""
            else:
                file_name = file_name.text

            line_number = frame.find("./line")
            if line_number is None:
                line_number = ""
            else:
                line_number = line_number.text

            stack_trace += stack_frame + " (" + file_name + ":" + line_number + ")\n"

        return stack_trace



def main():
    _xml_reader = XmlReader()
    _xml_writer = XmlWriter()
    _summerizer = Summerizer(_xml_writer)
    _xml_reader.subscribe(_summerizer, "error")
    _logs_reader = LogsReader(_xml_reader)

    _logs_reader.read_files('D:\Valgrind\XML')

if __name__ == '__main__':
    main()