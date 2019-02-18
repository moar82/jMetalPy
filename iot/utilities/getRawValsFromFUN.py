

"""
.. module:: miniaturization
   :platform: Unix, Windows
   synopsis: This script take as input a FUN.* file and retrieves the raw values
   measured based on the original measurements
   xxx.ALG.SCRIPT.js.RUN
.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""
import os, csv, math
from pathlib import Path

'''Hardcoded settings'''
directory_in_str = '/home/moar82/Documents/iot_miniaturization/results/sunspider/tunning_hv_server_173'
directory_for_org_measurements = '/home/moar82/Documents/iot_miniaturization/results/sunspider/default_duktape_measurements'

directory = os.fsencode(directory_in_str)
os.system('mkdir -p ' + directory_in_str + '/val_files/')
pathlist = Path(directory_in_str).glob('**/FUN.*')

for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    ''' from the path we need to extract the script name and put it a set'''
    prefix = path.name.split('.')[1]
    script_name = path.name.split('.')[2]
    consecutive = path.name.split('.')[4]
    '''median_results_original_default_3d-cube.csv'''
    benchmark_file = directory_for_org_measurements + \
                     '/median_results_original_default_' + script_name + '.csv'
    with open (benchmark_file ,'r') as pmeasurescsv:
        csvreader = csv.reader(pmeasurescsv)
        '''skip the header'''
        next(csvreader)
        for row in csvreader:
            try:
                file_size_org = float(row[0])
                mem_us_org = float(row[1])
                use_time_avg = float(row[2])
            except ValueError:
                print("Oops!  That was no valid number in" +benchmark_file)
    if math.isnan(mem_us_org) or math.isnan(use_time_avg) or math.isnan(file_size_org):
        print("Oops!  nan was found in: " + benchmark_file)
        continue
    ''' now let's convert percent to raw values and stored in a new file'''
    fun_file = open(path_in_str ,'r')
    numlines = len(fun_file.readlines())
    fun_file.close()
    with open (path_in_str ,'r') as fun_file:
        #numlines = 16
        csvreader = csv.reader(fun_file,delimiter=' ')
        w, h = 4, numlines
        Matrix = [['' for x in range(w)] for y in range(h)]
        idx = 0
        for line in csvreader:
            try:
                file_size_improv = float(line[0])*file_size_org+file_size_org
                mem_us_improv = float(line[1])*mem_us_org+mem_us_org
                use_time_improve = float(line[2])*use_time_avg+use_time_avg
                usr_rate = float(line[3])
            except ValueError:
                print("Oops!  That was no valid number in" +fun_file)
            Matrix[idx][0] = str(file_size_improv)
            Matrix[idx][1] = str(mem_us_improv)
            Matrix[idx][2] = str(use_time_improve)
            Matrix[idx][3] = str(usr_rate)
            idx = idx+1
    ''' now save the computed raw values in a new file'''
    new_raw_file = directory_in_str + '/val_files/' + 'VAL.' + prefix + '.'  + script_name + '.js.' + str(consecutive)
    fout = open(new_raw_file, "w")
    for row in Matrix:
        fout.write(' '.join(row) )
        fout.write('\n')
    fout.close()

