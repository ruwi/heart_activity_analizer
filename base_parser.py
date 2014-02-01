import argparse

class BaseParser(argparse.ArgumentParser):
    """
    It's ArgumentParser some options:

    COMMON OPTIONS:
        -f <file-name>, --file <file-name>
            Set input file. Default is standard input.
        -o <file-name>, --out <file-name>
            Set output file. Default is standard output.
        -h, --help
            Display help and exit.
        -v, --valid
            Choose valid data only. Default all data.
        -i, --invalid
            Choose invalid data only. Default all data.

    Some arguments are required:
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
    """
    def __init__(self, description=None, epilog=None):
        if description == None:
            raise ValueError('Description is required')
        if epilog == None:
            raise ValueError('Epilog is required')
        super(self, BaseParser).__init__(description=description,
            epilog=epilog)
#TODO: add arguments
        
