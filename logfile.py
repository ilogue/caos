from datetime import datetime
import pandas, io


class PresentationLogfile(object):

    created = None

    def __init__(self, fpath):
        self.fpath = fpath

    def read(self):
        with open(self.fpath) as fhandle:
            lines = fhandle.readlines()
        lines = [l.strip() for l in lines]
        created_string = lines[1][-19:]
        self.created = datetime.strptime(created_string, '%m/%d/%Y %H:%M:%S')
        self.lines = lines

    def to_dataframe(self):
        """Return the events from the logfile as a pandas DataFrame

        Returns:
            pandas.DataFrame: One row per event with all Neurobs columns
        """
        ## awkwardly, these files sometimes contain two tables;
        ## we need to find the end of table 1
        empty_line_idx = []
        for l, line in enumerate(self.lines):
            if len(line) < 3:
                empty_line_idx.append(l)
        if len(empty_line_idx) > 2:
            ## two tables in file
            end_of_table = empty_line_idx[2] ## 0-based index of first blank line
        else:
            ## one table in file
            end_of_table = len(self.lines)

        ## remove space in stim names
        preproc_lines = []
        for line in self.lines[:end_of_table]:
            line = line.replace(' cross', '_cross')
            line = line.replace('\tcross', '_cross')
            line = line.replace('\t_3.bmp', '_3.bmp')
            line = line.replace('Event Type', 'Event_Type')
            line += '\n'
            preproc_lines.append(line)
        
        with io.StringIO() as tempfile:
            tempfile.writelines(preproc_lines)
            tempfile.seek(0)
            df = pandas.read_csv(
                tempfile,
                engine='python',          ## c engine doesnt support regex seperators
                skip_blank_lines=True,
                sep='\t',             ## either space or tab
                header=2,               ## blank lines already skipped
                # nrows=end_of_table-5    ## 5 lines in header
            )
        return df
