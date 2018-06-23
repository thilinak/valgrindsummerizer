import difflib
import sys
from interface import implements

from WriterListner import WriterListner
from XmlTemplate import XmlTemplate


class XmlWriter(implements(WriterListner)):

    def __init__(self, _output_path='.', _print_number_of_duplicates = False):
        self.duplicate_counter = {}
        self.unique_counter = {}
        self.print_number_of_duplicates = _print_number_of_duplicates

        self.component_based_unique_counter = {}
        self.component_based_duplicate_counter = {}

        self.component_based_unique_records = {}
        self.component_based_duplicate_records = {}
        self.component_based_all_stack_traces = {}
        self.component_based_unique_stack_traces = {}
        self.output_path = _output_path;

    def on_stack_trace(self, component, kind, record, stack_trace):
        if self.print_number_of_duplicates == True:
            if component not in self.component_based_all_stack_traces:
                self.component_based_all_stack_traces[component] = {kind: [stack_trace]}
            elif kind not in self.component_based_all_stack_traces[component]:
                self.component_based_all_stack_traces[component][kind] = [stack_trace]
            else:
                self.component_based_all_stack_traces[component][kind].append(stack_trace)

    def on_unique_stack_trace(self, component, kind, stack_trace):
        if component not in self.component_based_unique_stack_traces:
            self.component_based_unique_stack_traces[component] = {kind: [stack_trace]}
        elif kind not in self.component_based_unique_stack_traces[component]:
            self.component_based_unique_stack_traces[component][kind] = [stack_trace]
        else:
            self.component_based_unique_stack_traces[component][kind].append(stack_trace)

    def on_duplicate_record(self, component, kind, record, stack_trace):

        if component not in self.component_based_duplicate_counter:
            self.component_based_duplicate_counter[component] = {kind: 1}
        elif kind not in self.component_based_duplicate_counter[component]:
            self.component_based_duplicate_counter[component][kind] = 1
        else:
            self.component_based_duplicate_counter[component][kind] += 1

        if component not in self.component_based_duplicate_records:
            self.component_based_duplicate_records[component] = {kind: [(record, stack_trace)]}
        elif kind not in self.component_based_duplicate_records[component]:
            self.component_based_duplicate_records[component][kind] = [(record, stack_trace)]
        else:
            self.component_based_duplicate_records[component][kind].append((record, stack_trace))

    def on_unique_record(self, component, kind, record, stack_trace):

        if component not in self.component_based_unique_counter:
            self.component_based_unique_counter[component] = {kind: 1}
        elif kind not in self.component_based_unique_counter[component]:
            self.component_based_unique_counter[component][kind] = 1
        else:
            self.component_based_unique_counter[component][kind] += 1

        if component not in self.component_based_unique_records:
            self.component_based_unique_records[component] = {kind: [(record, stack_trace)]}
        elif kind not in self.component_based_unique_records[component]:
            self.component_based_unique_records[component][kind] = [(record, stack_trace)]
        else:
            self.component_based_unique_records[component][kind].append((record, stack_trace))

    def print_unique_records(self):
        for component, kind_based_records in self.component_based_unique_records.items():
            for kind, error_records in kind_based_records.items():
                self.generate_xml_output(component, kind, error_records)

        print("__UNIQUE RECORDS__")
        for component, kind_based_count in self.component_based_unique_counter.items():
            print(component)
            for kind, count in kind_based_count.items():
                print("%20s : %5d" %(kind, count))
        print("__________________")

    def print_duplicate_records(self):
        print("__DUPLICATE RECORDS__")
        for component, kind_based_count in self.component_based_duplicate_counter.items():
            print(component)
            for kind, count in kind_based_count.items():
                print("%20s : %5d" %(kind, count))
        print("_____________________")

    def generate_xml_output(self, component, kind, error_records):
        xml_template = XmlTemplate(component, kind, self.output_path, self.print_number_of_duplicates)
        xml_template.write_records(error_records, self.component_based_all_stack_traces)

