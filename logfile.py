from datetime import datetime


class PresentationLogfile(object):

    created = None

    def __init__(self, fpath):
        self.fpath = fpath

    def read(self):
        with open(self.fpath) as fhandle:
            lines = fhandle.readlines()
        created_string = lines[1][-19:].strip()
        self.created = datetime.strptime(created_string, '%m/%d/%Y %H:%M:%S')
