import getopt
from difflib import SequenceMatcher
from xml.etree.ElementTree import fromstring, tostring

import sys

from LogsReader import LogsReader
from ReaderCacheObserver import ReaderCacheObserver
from XmlReader import XmlReader
from XmlWriter import XmlWriter


class Summerizer(ReaderCacheObserver):
    def __init__(self, _writer_listner):
        super(Summerizer, self).__init__()
        self.reader_cache.subscribe(self, "error")
        self.stack_traces = {}
        self.component_based_unique_stack_traces = {}
        self.writer_listner = _writer_listner
        self.interested_kinds = ['InvalidRead', 'Leak_PossiblyLost' ,'Leak_DefinitelyLost', 'SyscallParam', 'UninitCondition', 'UninitValue'] #, 'Leak_PossiblyLost'

        self.element_count = 0
        #self.interested_kinds = ['Leak_PossiblyLost']

    def update(self, element, component_name):
        stack_trace = Summerizer.construct_stacktrace(element)

        self.element_count += 1

        if self.element_count % 1000 == 0:
            print('# of Elements processed: ' + str(self.element_count))

        kind = element.find("./kind").text

        if (self.is_interested_kind(kind) == False):
            return

        self.writer_listner.on_stack_trace(component_name, kind, element, stack_trace)

        if (self.is_duplicate(stack_trace, kind, component_name) == False):
            self.writer_listner.on_unique_record(component_name, kind, element, stack_trace)
        else:
            self.writer_listner.on_duplicate_record(component_name, kind, element, stack_trace)

    def is_interested_kind(self, kind):
        for _kind in self.interested_kinds:
            if _kind == kind:
                return True
        return False

    def is_duplicate(self, stack_trace, kind, component):
        kind_based_previouse_stack_traces = self.component_based_unique_stack_traces.get(component, None)
        if kind_based_previouse_stack_traces != None:
            previouse_stack_traces = kind_based_previouse_stack_traces.get(kind, None)
            if previouse_stack_traces != None:
                for previouse_stack_trace in previouse_stack_traces:
                    sequence_matcher = SequenceMatcher(None, stack_trace, previouse_stack_trace)

                    ratio = sequence_matcher.ratio()
                    if ratio > 0.8: # not an upper bound
                        return True

        if component not in self.component_based_unique_stack_traces:
            self.component_based_unique_stack_traces[component] = {kind: [stack_trace]}
        elif kind not in self.component_based_unique_stack_traces[component]:
            self.component_based_unique_stack_traces[component][kind] = [stack_trace]
        else:
            self.component_based_unique_stack_traces[component][kind].append(stack_trace)

        return False

    @staticmethod
    def construct_stacktrace(errorElement):
        stack_trace = ""
        frames = errorElement.findall("./stack/frame")

#        s = "-"
#        stack_trace = s.join([str(ip.text) for ip in ips])
#        for ip in ips:
#            stack_trace += str(ip.text) + "\n"

#            print(stack_trace.join(str(ip.text)))

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
    print_number_of_duplicates = True
    _xml_writer = XmlWriter('D:\\Valgrind\\Test with number of duplicates\\ALL_OUT', print_number_of_duplicates)
    _summerizer = Summerizer(_xml_writer)
    _xml_reader.subscribe(_summerizer, "error")
    _logs_reader = LogsReader(_xml_reader)

    _logs_reader.read_files('D:\\Valgrind\\Test with number of duplicates\\ALL_IN_SEPERATED\\ALL_3_IN_1') # ALL_IN_SEPERATED\Sequencer
    _xml_writer.print_duplicate_records();
    _xml_writer.print_unique_records();

    #_xml_writer.generate_duplicates_distribution()

if __name__ == '__main__':
    main()

'''
def main(argv):

    try:
        opts, args = getopt.getopt(argv, "i:o:")
    except getopt.GetoptError:
        print ('test.py -i <input/Log/Path> -o <output/Log/Path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputfiles_dir = arg
        if opt == "-o":
            outputfiles_dir = arg
    print_number_of_duplicates = False
    _xml_reader = XmlReader()
    _xml_writer = XmlWriter(outputfiles_dir, print_number_of_duplicates)
    _summerizer = Summerizer(_xml_writer)
    _xml_reader.subscribe(_summerizer, "error")
    _logs_reader = LogsReader(_xml_reader)
    try:
        _logs_reader.read_files(inputfiles_dir) # D:\val_logs\PTTPS
    except Exception as e:
        print(e)
        sys.exit(2)
    _xml_writer.print_duplicate_records();
    _xml_writer.print_unique_records();

if __name__ == '__main__':
    main(sys.argv[1:])
'''