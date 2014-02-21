#!/usr/bin/python2
#-*- coding: utf-8 -*-

#
# Author: Wiktor Wolak
#

import sys
import argparse
from itertools import tee

import numpy as np
import pylab as plt

import base_parser
import validator

def get_data_by_time(data, T_min, T_max):
    """
        Return data raws with time is between T_min, T_max
    """
    return data[np.where((T_min<data[:,0]) * (data[:,0]<T_max))]

if __name__ == '__main__':
    parser = base_parser.BaseParser(
            description="",
            epilog="")
    parser.add_argument('-T', '--delta-time',
            dest='T',
            action='store',
            default=np.inf,
            type=float,
            metavar="<delta-time>",
            help="Set considering time interval to <delta-time> in minutes.")
    parser.add_argument('-n',
            dest='n',
            action='store',
            type=float,
            default=1,
            help= "Set which number of interval should be plotted. This option"
                "can't be used with options --min, --max, --mean, --average,"
                "--std, --standard-deviation, --histogram.")
    parser.add_argument('--mean', '--average',
            dest='mean',
            action='store_true',
            help="Plot averages of second column fot each interval"
                "<delta-time>")
    parser.add_argument('--min',
            dest='min',
            action='store_true',
            help="Plot minimal values of second columnfor each interval"
                "<delta-time>.")
    parser.add_argument('--max',
            dest='max',
            action='store_true',
            help="Plot maximal values of second columnfor each interval"
                "<delta-time>.")
    parser.add_argument('--data',
            dest='data',
            action='store_true',
            help="Plot data of secound column")
    parser.add_argument('--all',
            dest='all',
            action='store_true',
            help="Plot all informationfor each interval <delta-time>.")
    parser.add_argument('--histogram',
            dest='histogram',
            action='store_true',
            help="Plot histogram of data. Minimal, maximal and average valus"
                "will be mark on the plot. Optons like --min, --max, --std,"
                " --all, have no influents on the resulting plot")
    parser.add_argument('--bins',
            dest='bins',
            action='store',
            default=10,
            type=int,
            help="Number of bins in histogram")
    args = parser.parse_args()
    data = validator.get_data_from_file(args.input_file)
    if args.filter_ == 'all':
        pass
    elif args.filter_ == 'valid':
        data = validator.get_valid_data(data)
    elif args.filter_ == 'invalid':
        data = validator.get_invalid_data(data)
    else:
        raise Exception("Wrong argument parsing")
    if args.T <= 0:
        print "Time interval must be > 0"
        sys.exit(1)
    fig = plt.figure()
    ax = fig.gca()
    if args.histogram:
        data = get_data_by_time(data, args.T*(args.n-1), args.T*args.n)
        if args.bins <= 2:
            print "Number of bins must be greater then 2"
            sys.exit(1)
        ax.hist(data[:,1], bins=args.bins)
    else:
        if args.data or args.all:
            ax.plot(data[:,0], data[:,1], '-', label='Data',
                    color=(0.8,0.8,0.8))
        n_intervals = int(np.max(data[:,0])//args.T)+1
        data_intervals = (get_data_by_time(data, args.T*i, args.T*(i+1))[:,1]
            for i in xrange(n_intervals))
        x = np.linspace(0, args.T*n_intervals, n_intervals)
        if args.min or args.all:
            data_intervals, d_i = tee(data_intervals)
            y = map(np.min, d_i)
            ax.plot(x, y, 'b--',
                label='Minimal values')
        if args.max or args.all:
            data_intervals, d_i = tee(data_intervals)
            y = map(np.max, d_i)
            ax.plot(x, y, 'r--',
                label='Maximal values')
        if args.mean or args.all:
            data_intervals, d_i = tee(data_intervals)
            y = map(np.mean, d_i)
            ax.plot(x, y, 'g-',
                label='Average values')
        ax.legend()
    plt.show()
            


    

