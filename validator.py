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


def get_data_from_file(file_path):
    """
    Return data from file. Only data with 3 columns are allowed.
    In case of other data AssertionError will be raise.  
    """
    data = np.loadtxt(file_path)
    assert len(data.shape) == 2 and data.shape[1] == 3
    return data
    

def get_valid_data(data):
    """
    Return only valid data. Value of third column is equal to 1 if data
    record is valid.
    """
    return data[np.where(data[:,2]==1)]

def get_invalid_data(data):
    """
    Return only invalid data. Value of third column is equal to 0 if data
    record is invalid.
    """
    return data[np.where(data[:,2]==0)]

def get_number_of_records(data):
    """
    Return number of records of given data
    """
    return len(data)

if __name__ == '__main__':
    pass #TODO: argparse

