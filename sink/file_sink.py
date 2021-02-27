from json import dumps
from time import strftime

from sink.sink import Sink


class FileSink(Sink):
    def __init__(self, path, file_name_pattern, unique_id, max_size):
        self.file_name_pattern = file_name_pattern
        self.unique_id = unique_id
        self.max_size = max_size
        self.path = path

        self.file = None
        self.file_size = 0

        self._open_file()

        Sink.__init__(self)

    def write(self, data):
        string = dumps(data) + "\n"

        self.file.write(string)
        self.file_size += len(string)

        if self._should_reopen_file():
            self._reopen_file()

    def close(self):
        self._close_file()

    @staticmethod
    def _get_timestamp():
        return strftime("%d%m%Y_%H%M%S")

    def _open_file(self):
        file_name = self.file_name_pattern.format(unique_id=self.unique_id,
                                                  timestamp=FileSink._get_timestamp())
        file_path = "{}/{}".format(self.path, file_name)

        self.file = open(file_path, "w")

    def _close_file(self):
        self.file.close()
        self.file_size = 0

    def _reopen_file(self):
        self._close_file()
        self._open_file()

    def _should_reopen_file(self):
        if self.file_size >= self.max_size:
            return True

        return False
