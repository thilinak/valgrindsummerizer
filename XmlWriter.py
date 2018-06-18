import sys
from interface import implements

from WriterListner import WriterListner

class XmlWriter(implements(WriterListner)):

    def __init__(self):
        self.duplicate_counter = {}
        self.unique_counter = {}

    def on_duplicate_record(self, component, kind, record):
        try:
            self.duplicate_counter[kind] += 1
        except KeyError:
            self.duplicate_counter[kind] = 1
        print('[DUPLICATE]', end='')
        for _kind, _count in self.duplicate_counter.items():
            print(_kind + " : " + str(_count), end='; ')
        print('')

    def on_unique_record(self, component, kind, record):
        try:
            self.unique_counter[kind] += 1
        except KeyError:
            self.unique_counter[kind] = 1
        print('[UNIQUE]', end='')
        for _kind, _count in self.unique_counter.items():
            print(_kind + " : " + str(_count), end='; ')
        print('')
        #print("[UNIQUE]: " + component + " : " + kind + " : " + record.decode(sys.stdout.encoding))
