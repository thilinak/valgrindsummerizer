from xml.etree import ElementTree
from xml.etree.ElementTree import tostring

from LogsReader import LogsReader
from ReaderCache import ReaderCache


class XmlReader(ReaderCache):

    def _extract_data(self, tag, file_data):

        root = ElementTree.fromstring(file_data)

        self.component_name = root.find("./args/argv/exe").text
        print(self.component_name)

        extractded_data = []
        for _tag in root.iter('error'): #TODO: replace this with tag variable
            extractded_data.append(_tag)


        return extractded_data

    def on_read_data(self, file_data):
        extracted_data = {}

        for type in self.subscribers.items():
            extracted_data[type] = self._extract_data(type, file_data)

        for type, subscriber in self.subscribers.items():
            for _type, _data in extracted_data.items():
                if type in _type:
                    for blocks in _data:
                        subscriber.update(blocks, self.component_name)  # TODO: for a single type there can be more than one subscribers


'''
if __name__ == '__main__':
    _reader_listner = XmlReader()
    _logs_reader = LogsReader(_reader_listner)
    _logs_reader.read_files('D:\Valgrind\XML')
'''