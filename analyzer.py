#!/usr/bin/python2
#-*- coding: utf-8 -*-

#
# Author: Wiktor Wolak
#
import sys
import argparse

import numpy as np

import base_parser
import validator


if __name__ == '__main__':
    parser = base_parser.BaseParser(
            description="",
            epilog="")
    parser.add_argument('--mean', '--average',
            dest='mean',
            action='store_true',
            help="Display average of second column.")
    parser.add_argument('--min',
            dest='min',
            action='store_true',
            help="Display minimal value of second column.")
    parser.add_argument('--max',
            dest='max',
            action='store_true',
            help="Display maximal value of second column.")
    parser.add_argument('--std', '--standard-deviation',
            dest='std',
            action='store_true',
            help="Display standard deviation of second column.")
    parser.add_argument('--all',
            dest='all',
            action='store_true',
            help="Display all information.")
    parser.add_argument('-p', '--pprint',
            dest='pprint',
            action='store_true',
            help="Display information in readable form with descriptions.")
    args = parser.parse_args()
    data = validator.get_data_from_file(args.input_file)
    if args.filter_ == 'all':
        if args.pprint:
            print "All data analyzed."
    elif args.filter_ == 'valid':
        if args.pprint:
            print "Valid data analyzed."
        data = validator.get_valid_data(data)
    elif args.filter_ == 'invalid':
        if args.pprint:
            print "Invalid data analyzed."
        data = validator.get_invalid_data(data)
    else:
        raise Exception("Wrong argument parsing")
    if args.mean or args.all:
        if args.pprint:
            print "Mean:                ",
        print np.mean(data)
    if args.min or args.all:
        if args.pprint:
            print "Min:                 ",
        print np.min(data)
    if args.max or args.all:
        if args.pprint:
            print "Max:                 ",
        print np.max(data)
    if args.std or args.all:
        if args.pprint:
            print "Standard deviation:  ",
        print np.std(data)
    




