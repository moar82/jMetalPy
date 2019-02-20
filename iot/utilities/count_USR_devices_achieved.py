"""
.. module:: Count USR devices achieved
   :platform: Unix, Windows
   synopsis: This script take as input a VAL.* file and counts the
   number of devices from a USR file that we find a solution
.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""

import os, csv
from statistics import median
from pathlib import Path


'''Harcoded section'''
USR_file_path = '/home/moar82/jMetalPy/iot/USR.csv'
algo_prefixes = ['NSGAII','RS','SWAY']
directory_in_str = '/home/moar82/Documents/iot_miniaturization/results/sunspider/val_files_250ev/all_vals'
'''end hardcoded section'''

devices = []
'''Open a VAL file for a algorithm.project'''

with open(USR_file_path) as f:
    devices = [tuple(line) for line in csv.reader(f)]
devices.pop(0)
print("devices read from USR file:%d" % len(devices))

directory = os.fsencode(directory_in_str)
os.system('mkdir -p ' + directory_in_str + '/USR_achieved/')

nbdevices = dict()
'''dictionary of alg.script'''
alg_script = dict()
script_names =set()

# To remove thew word 'FUN.' for the RS files this bash's one-line script works:
# for file in VAL.RS.FUN.*; do  mv "$file" "${file/FUN./}"; done


for algo in algo_prefixes:
    pathlist = Path(directory_in_str).glob('**/VAL.'+ algo +'.*')
    for path in pathlist:
    # because path is object not string
        path_in_str = str(path)
        print (path_in_str)
        ''' from the path we need to extract the script name and put it a set'''
        script = path.name.split('.')[2]
        consecutive = path.name.split('.')[4]
        script_names.add(script)
        '''initialize nbdevices'''
        for dev in devices:
            nbdevices[dev[0]] = 0
        ''' some files have space as delimiter some files have , . So it is better to run
            sed  -i 's/,/ /g' VAL*  to normalize them'''
        with open(path_in_str, 'r') as val_file:
            csvreader = csv.reader(val_file, delimiter=' ')
            for line in csvreader:
                try:
                    file_size_improv = float(line[0])
                    mem_us_improv = float(line[1])
                    #use_time_improve = float(line[2])*use_time_avg+use_time_avg
                    for dev in devices:
                        if file_size_improv<=float(dev[3]) and mem_us_improv<= float(dev[2]):
                            nbdevices[dev[0]] = 1
                except ValueError:
                    print("Oops!  That was no valid number in" + val_file)
        devices_found = 0
        for dev in nbdevices.keys():
            if nbdevices[dev] == 1:
                devices_found = devices_found + 1
        dkey = algo + '.' + script
        if dkey not in alg_script:
            alg_script[dkey] = [devices_found]
        else:
            alg_script[dkey].append(devices_found)
''' now we save the results in a single file for each alg.script combination'''


median_alg_script = dict()
for alg_script_key in alg_script.keys():
    nb_list =[]
    new_file = directory_in_str + '/USR_achieved/' + 'NBD.' + alg_script_key + '.txt'
    fout = open(new_file, "w")
    for nb in alg_script.get(alg_script_key):
        fout.write(str(nb) )
        fout.write('\n')
        nb_list.append(nb)
    median_alg_script[alg_script_key] = median(nb_list)
    fout.close()

''' To save the the summary of the results by script'''
new_file = directory_in_str + '/USR_achieved/' + 'USR_summary_devices_achieved.csv'
fout = open(new_file, "w")
for s_n in script_names:
    row =[]
    row.append(s_n)
    for alg in algo_prefixes:
        row.append(str(median_alg_script.get(alg+'.'+s_n)))
    fout.write( ','.join(row) )
    fout.write('\n')
fout.close()
