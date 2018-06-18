from interface import implements

from LogsReader import LogsReader
from ReaderListner import ReaderListner


class ReaderCache(implements(ReaderListner)):
    def __init__(self):
        self.subscribers = {}
        print("dummy")
        #pass

    def get_subscribers_iterator(self):
        return self.subscribers.items()

    def on_read_data(self, file_data):
        pass

    def subscribe(self, reader_cache_observer, type):
        self.subscribers[type] = reader_cache_observer
        #pass

    def unsubstribe(self, reader_cache_observer):
        pass

    def notify(self):
        pass


'''
if __name__ == '__main__':
    _reader_listner = ReaderCache()
    _logs_reader = LogsReader(_reader_listner)
    _logs_reader.read_files('D:\Valgrind\XML')
    '''