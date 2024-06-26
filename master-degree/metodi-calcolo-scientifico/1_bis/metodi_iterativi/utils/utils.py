import logging
from scipy.io import mmread

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read(filename):
    with open(filename) as mass_file:
        m = mmread(mass_file)
    return m.tocsr()

def write_report_and_logs(path_report, file_report, string):
    report = open(path_report + file_report, 'a')
    report.write(string)
    logging.info(string)
    report.close()
