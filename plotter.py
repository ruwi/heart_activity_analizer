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
    parser.add_argument('-T', '--delta-time', '--interval',
            dest='T',
            action='store',
            default=-1.0,
            type=float,
            metavar="<delta-time>",
            help="Set considering time interval to <delta-time> in minutes.")
    parser.add_argument('-s', '--segment-time',
            dest='st',
            action='store',
            default=1.0,
            type=float,
            metavar="<segment-time>",
            help="Segment time"
                "All data are divided into pieces with <segment-time>"
                "Functions like mean, min, max will return value from this"
                "intervals and then data will be plotted")
    parser.add_argument('-n', '--interval-number',
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
            help="Plot averages of second column for each interval"
                "<delta-time>")
    parser.add_argument('--min',
            dest='min',
            action='store_true',
            help="Plot minimal values of second column for each interval"
                "<delta-time>.")
    parser.add_argument('--max',
            dest='max',
            action='store_true',
            help="Plot maximal values of second column for each interval"
                "<delta-time>.")
    parser.add_argument('--data',
            dest='data',
            action='store_true',
            help="Plot data of second column")
    parser.add_argument('--all',
            dest='all',
            action='store_true',
            help="Plot all information for each interval <delta-time>.")
    parser.add_argument('--histogram',
            dest='histogram',
            action='store_true',
            help="Plot histogram of data. Minimal, maximal and average values"
                "will be mark on the plot. Options like --min, --max, --std,"
                " --all, have no influence on the resulting plot")
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
        args.T = np.max(data[:,0])
    fig = plt.figure()
    ax = fig.gca()
    data = get_data_by_time(data, args.T*(args.n-1), args.T*args.n)
    if len(data) == 0:
        print "No data, try change options"
        sys.exit(1)
    if args.histogram:
        ax.set_title('Histogram of %s RR data ' % args.filter_ +
                '- file %s ' % args.input_file.name +
                '- bins %d\n' % args.bins +
                'segment time: %.2f min; segment number: %d' % (args.T, args.n))
        ax.set_xlabel('RR interval in milliseconds')
        ax.set_ylabel('Number of results')
        if args.bins <= 2:
            print "Number of bins must be greater then 2"
            sys.exit(1)
        y, x, hist = ax.hist(data[:,1], bins=args.bins)
        x = (x[:-1] + x[1:])/2 # middle of intervals
        yy = np.max(y)
        xx = x[np.where(y==yy)][0]
        ax.annotate('maximal value of histogram: %d' % yy,
                xy=(xx,yy), xytext=(xx, yy*1.1),
                arrowprops=dict(arrowstyle='->'))
        ax.set_ylim(0, yy*1.3)
        yy2 = np.min(y)
        xx2 = x[np.where(y==yy2)][0]
        ax.annotate('minimal value of histogram: %d' % yy2,
                xy=(xx2,yy2), xytext=(xx2, yy2 + yy*0.1),
                arrowprops=dict(arrowstyle='->'))
        yy3 = np.mean(y)
        xx3 = x[0]
        ax.annotate('average value of histogram: %.02f' % yy3,
                xy=(xx3,yy3), xytext=(xx3, yy3 + yy*0.1),
                arrowprops=dict(arrowstyle='->'))
        ax.plot(x, yy3*np.ones_like(x), 'g--')

    else:
        title =('%s RR - file: %s; '
                % (args.filter_, args.input_file.name))
        if args.min or args.max or args.mean or args.all:
            title += 'segment time: %.02f min' % args.st
        title += ('\nploted interval: %.2f min; interval number: %d'
                % (args.T, args.n))
        ax.set_title(title)
        ax.set_xlabel('Time in minutes')
        ax.set_ylabel('RR interval in milliseconds')
        if args.data or args.all:
            ax.plot(data[:,0], data[:,1], '-', label='Data',
                    color=(0.8,0.8,0.8))
        n_intervals = int(np.max(data[:,0])//args.st)+1
        data_intervals = (get_data_by_time(data, args.st*i, args.st*(i+1))[:,1]
            for i in xrange(n_intervals))
        x = np.linspace(args.st/2,
                args.st*n_intervals - args.st/2, n_intervals)
        try:
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
        except ValueError:
            print "No data in one of the smooth-time intervals"
            print "Try change options"
            sys.exit(1)
        ax.legend()
    if args.output_file == sys.stdout:
        plt.show()
    else:
        fig.savefig(args.output_file)
            


    

