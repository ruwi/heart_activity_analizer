#!/usr/bin/python2
#-*- coding: utf-8 -*-

#
# Author: Wiktor Wolak
#

"""
Filtrate data, count number of lines of valid or invalid data.

INPUT FILE FORMAT:
    The file should be built up with the three columns:
     - first column contains the total (accumulated) time of the recording (in
       minutes)
     - second column contains the RR interval (in milliseconds)
     - third column contains the annotation flag - 0 is for valid record and 1
       represents the invalid record 
"""
import sys
import argparse

import numpy as np

import base_parser


def get_data_from_file(file_path):
    """
    Return data from file. Only data with 3 columns are allowed.
    In case of other data AssertionError will be raise.  
    """
    data = np.loadtxt(file_path)
    if len(data.shape) == 1 and data.shape[0] == 3:
        data = data[np.newaxis,:]
    if len(data.shape) != 2:
        raise ValueError("Wrong format of data")
    if data.shape[1] != 3:
        raise ValueError("Wrong format of data."
            "Got %d value per line, 3 expected" % data.shape[1])
    return data
    

def get_valid_data(data):
    """
    Return only valid data. Value of third column is equal to 0 if data
    record is valid.
    """
    return data[np.where(data[:,2]==0)]

def get_invalid_data(data):
    """
    Return only invalid data. Value of third column is equal to 1 if data
    record is invalid.
    """
    return data[np.where(data[:,2]==1)]

def get_number_of_records(data):
    """
    Return number of records of given data
    """
    return len(data)

if __name__ == '__main__':
    parser = base_parser.BaseParser(
        description="""
            Filtrate data.  Each line of data is valid only when value from 3.
            column is equal to 1.
            """,
        epilog="") 
    parser.add_argument('-l',
        dest='line',
        action='store_true',
        help='Write number of filtrated data except just data.')
    args = parser.parse_args()
    data = get_data_from_file(args.input_file)
    if args.filter_ == 'all':
        pass
    elif args.filter_ == 'valid':
        data = get_valid_data(data)
    elif args.filter_ == 'invalid':
        data = get_invalid_data(data)
    else:
        raise Exception("Wrong argument parsing")
    if args.line:
        args.output_file.write('Lines of %s data: %d\n' % (args.filter_,
            len(data)))
    else:
        np.savetxt(args.output_file, data)

    

