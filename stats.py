#!/usr/bin/python
import sys
import re
import glob
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt

def get_ignore_from_argv():
    args = sys.argv[1:] # first argument is this file
    if len(args) > 0 and (args[0] == '--ignore'or args[0] == '-i'):
        print('All phone numbers matching the following patterns \nget ignored:', args[1:],'\n')
        return args[1:]

def get_months(logfiles_list):
    m = []
    for f in logfiles_list:
        s = f.strip('_log.txt')
        m.append(s[4:]+'-'+s[:4])
    return m

################################################################################

log_files_per_month = sorted(glob.glob('logs/*_log.txt'))
months = get_months(log_files_per_month)

print('###################################################')
print('##                                               ##')
print('##      cgcall logs from', months[0], 'to', months[-1],'     ##')
print('##                                               ##')
print('###################################################\n')

ignore_phonenumbers = get_ignore_from_argv()

calls_datetime = [None]*len(log_files_per_month)
calls_phonenumber = [None]*len(log_files_per_month)
calls_duration = [None]*len(log_files_per_month)

i = 0
for f in log_files_per_month:
    calls_datetime[i] = []
    calls_phonenumber[i] = []
    calls_duration[i] = []

    with open(f) as fin:
        for line in fin:
            date, phone, duration = line.strip().split('\t')

            # ignore calls from command line params
            for pattern in ignore_phonenumbers:
                regex = re.compile(pattern)
                if regex.match(phone):
                    #print('MATCH:', phone)
                    continue

            d = datetime.strptime(date, '%Y-%m-%d_%H:%M:%S')
            min, sec = duration.split(':')
            dur = int(min) * 60 + int(sec)

            calls_datetime[i].append(d)
            calls_phonenumber[i].append(phone)
            calls_duration[i].append(dur)
    i += 1

np_calls_datetime = np.array(calls_datetime)
np_calls_phonenumber = np.array(calls_phonenumber)
np_calls_duration = np.array(calls_duration)


print('|---------------------------------------------------------------|')
print('|', '       ', '|', '     ', '|', 'unique ', '|', 'average ', '\t|', 'median  ', '|', 'max     ', '\t|')
print('|', 'month  ', '|', 'calls', '|', 'callers', '|', 'duration', '\t|', 'duration', '|', 'duration', '\t|')
print('|---------------------------------------------------------------|')
for i in range(len(log_files_per_month)):
    print('|', \
          months[i], '|', \
          len(np_calls_datetime[i]), '\t  |', \
          len(set(np_calls_phonenumber[i])), ' \t    |', \
          round(np.mean(np_calls_duration[i])/60, 1),'min', '\t|', \
          round(np.median(np_calls_duration[i])/60, 1),'min', ' |', \
          round(np.max(np_calls_duration[i])/60, 1),'min', '\t|', \
          )
print('|---------------------------------------------------------------|')
#print('|', ' total ', '|', 15, '|', len(set(np_calls_phonenumber.flatten())), '|')
#print('|-----------------------------------------------------------------------|')

