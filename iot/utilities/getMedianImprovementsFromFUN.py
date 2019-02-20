

"""
.. module:: Get median improvement values from FUN files (percentage improvement)
   :platform: Unix, Windows
.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""
import os, csv
from statistics import median
from pathlib import Path

'''Hardcoded settings'''
directory_in_str = '/home/moar82/Documents/iot_miniaturization/results/sunspider/all_RS_FUN_250_ev'

directory = os.fsencode(directory_in_str)
os.system('mkdir -p ' + directory_in_str + '/median_improvement_files/')
pathlist = Path(directory_in_str).glob('**/FUN.*')
values_file_size ={}
values_mem_us ={}
values_run_time ={}
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    ''' from the path we need to extract the script name and put it a set'''
    prefix = path.name.split('.')[1]
    script_name = path.name.split('.')[2]
    consecutive = path.name.split('.')[4]

    ''' now let's open the FUN files and compute median'''
    file_size = memory_usage =  run_time = 0.0
    with open (path_in_str ,'r') as fun_file:
        csvreader = csv.reader(fun_file,delimiter=' ')
        for line in csvreader:
            file_size = float(line[0])
            memory_usage = float(line[1])
            run_time =float(line[2])
            if script_name not in values_file_size:
                values_file_size[script_name] = [file_size]
                values_mem_us[script_name] = [memory_usage]
                values_run_time[script_name] = [run_time]
            else:
                values_file_size.get(script_name).append(file_size)
                values_mem_us.get(script_name).append(memory_usage)
                values_run_time.get(script_name).append(run_time)

''' now compute the median values and save it into a new file'''

new_output_file = directory_in_str + '/median_improvement_files/median_improvements.csv'
print('saving files in ' + new_output_file)
fout = open(new_output_file, "w")
row = []
for key in values_file_size:
    row.append(key)
    row.append(str(median(values_file_size[key])))
    row.append(str(median(values_mem_us[key])))
    row.append(str(median(values_run_time[key])))
    fout.write(','.join(row) )
    fout.write('\n')
fout.close()

