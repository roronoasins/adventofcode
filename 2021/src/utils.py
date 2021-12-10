import logging

def readline_input_file(file_path):
    input_file = open(file_path, 'r')
    file_line = input_file.readline()
    input_file.close()

    return file_line

def readlines_input_file(file_path):
    input_file = open(file_path, 'r')
    file_lines = input_file.readlines()
    input_file.close()

    return file_lines

def matrix_to_str(matrix):
    return  '\n'+'\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix])


def initialize_logging(logging_level):
    levels = {
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    logging.basicConfig(handlers=[logging.StreamHandler()], level=levels[logging_level])
