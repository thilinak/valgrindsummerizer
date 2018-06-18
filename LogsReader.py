import os

class LogsReader():

    def __init__(self, reader_listner):
        self._reader_listner = reader_listner
        pass

    def read_files(self, directory='.', file_extension='log'):
        file_names = LogsReader.get_log_file_paths(directory, file_extension)

        if (len(file_names) == 0):
            raise RuntimeError('No files found', directory, file_extension) from os.error

        for file_name in file_names:
            file_data = self.read_file(file_name)

            if (len(file_data) == 0):
                raise  RuntimeError('No data in file', file_name) from os.error
            self._reader_listner.on_read_data(file_data)

    @staticmethod
    def get_log_file_paths(directory: str, file_extention: str) -> list:
        file_names = []

        for filename in os.listdir(directory):
            file_full_path = os.path.join(directory, filename)
            if os.path.isdir(file_full_path):
                file_names.extend(LogsReader.get_log_file_paths(file_full_path, file_extention))

            if filename.endswith(file_extention):
                file_names.append(file_full_path)

        return file_names

    def read_file(self, filename) -> str:
        print("Reading ", filename)

        with open(filename, 'r') as logFile:
            file_data = logFile.read()
            logFile.close()

        return file_data