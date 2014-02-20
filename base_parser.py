import sys
import argparse

class BaseParser(argparse.ArgumentParser):
    """
    It's ArgumentParser with some options:

    COMMON OPTIONS:
        -f <file-name>, --file <file-name>
            Set input file. Default is standard input.
        -o <file-name>, --out <file-name>
            Set output file. Default is standard output.
        -h, --help
            Display help and exit.
        --filter <valid | invalid | all>
            Filtrate data before other operations.
            Default value is 'all'

    Some arguments are required:
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
    """
    def __init__(self, description=None, epilog=None):
        if description == None:
            raise ValueError('Description is required')
        if epilog == None:
            raise ValueError('Epilog is required')
        super(BaseParser, self).__init__(description=description,
            epilog=epilog)
        self.add_argument('-f', '--file',
            dest='input_file',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help="Set input file. Default is standard input.")
        self.add_argument('-o', '--out',
            dest='output_file',
            type=argparse.FileType('w'),
            default=sys.stdout,
            help="Set output file. Default is standard output.")
        self.add_argument('--filter',
            dest='filter_',
            choices=['valid', 'invalid', 'all'],
            default='all')
