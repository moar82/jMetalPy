"""
.. module:: Count USR devices default
   :platform: Unix, Windows
   synopsis: This script take as input a VAL.* file and counts the
   number of devices from a USR file that we find a solution
.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""

import os, csv


'''Harcoded section'''
USR_file_path = '/home/moar82/jMetalPy/iot/USR.csv'

directory_in_str = '/home/moar82/Documents/iot_miniaturization/'
file_with_default_measurements = 'sunspider_testbed_default.csv'
'''end hardcoded section'''

devices = []


with open(USR_file_path) as f:
    devices = [tuple(line) for line in csv.reader(f)]
devices.pop(0)
print("devices read from USR file:%d" % len(devices))

directory = os.fsencode(directory_in_str)

nbdevices = dict()
'''dictionary of alg.script'''
devices_by_script ={}
#compulsory_features, mem_usage, et =[]

'''initialize nbdevices'''
for dev in devices:
    nbdevices[dev[0]] = 0
with open(directory_in_str+ file_with_default_measurements, 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    ''' skip the header'''
    next(csvreader)
    for line in csvreader:
        try:
            devices_found = 0
            file_size = float(line[2])
            mem_us = float(line[3]) * 1000
            #use_time_improve = float(line[2])*use_time_avg+use_time_avg
            for dev in devices:
                if file_size<=float(dev[3]) and mem_us<= float(dev[2]):
                    devices_found = devices_found + 1
            devices_by_script[line[0]] = devices_found
        except ValueError:
            print("Oops!  That was no valid number in " + file_with_default_measurements)


''' To save the the summary of the results by script'''
new_file = directory_in_str + '/USR_summary_devices_default.csv'
fout = open(new_file, "w")
for s_n in devices_by_script:
    row =[]
    row.append(s_n)
    row.append(str(devices_by_script.get(s_n)))
    fout.write( ','.join(row) )
    fout.write('\n')
fout.close()
