import difflib
import xml.etree.cElementTree as ET
from io import BytesIO

class XmlTemplate:

    def __init__(self, _component, _kind, _file_path = '.', _print_number_of_duplicates = False):
        self.component = _component
        self.kind = _kind
        self.print_number_of_duplicates = _print_number_of_duplicates
        self.file_path = _file_path + '\\' + str(_component) + "_" + str(_kind) + ".val_xml.log"

        self.ROOT = 'valgrindoutput'
        self.STATUS = 'status'
        self.STATE = 'state'
        self.NUM_OF_DUPLICATES = 'number_of_duplicates'

    def re_order_records_based_on_number_of_duplicates(self, error_records, all_stack_traces):
        number_of_duplicates_vs_element = []
        for record_tuple in error_records:
            number_of_duplicates = len(
                difflib.get_close_matches(record_tuple[1], all_stack_traces[self.component][self.kind],
                                          len(all_stack_traces[self.component][self.kind]), 0.8))
            number_of_duplicates_vs_element.append((number_of_duplicates, record_tuple[0]))

        number_of_duplicates_vs_element.sort(key=self.takeFirst, reverse=True)
        return number_of_duplicates_vs_element


    def takeFirst(self, elem):
        return elem[0]

    def write_records(self, error_records, all_stack_traces):
        root = ET.Element(self.ROOT)

        status = ET.SubElement(root, self.STATUS)
        ET.SubElement(status, self.STATE).text = "RUNNING"

        if self.print_number_of_duplicates == False:
            for error_record in error_records:
                root.append(error_record[0])
        else:
            ordered_error_records = self.re_order_records_based_on_number_of_duplicates(error_records, all_stack_traces)

            for error_record_tuple in ordered_error_records:
                error_record_tuple[1].find('./tid').text = str(error_record_tuple[0])
                root.append(error_record_tuple[1])

        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding='utf-8', xml_declaration=True)

