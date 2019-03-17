import os
import copy
import subprocess
from pathlib import Path

"""
.. module:: miniaturization
   :platform: Unix, Windows
   :synopsis: This script extracts the execution time from the date registered
   : in the FUN* files generated by JMetalPy into a new subdirectory
     inside directory_in_str, called et_files.
   

.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""

'''Hardcoded settings'''
directory_in_str = '/home/moar82/Documents/iot_miniaturization/results/sunspider/RS_server106_3d-cube-3obj-15000-ev'
prefix = 'FUN'
nbofRuns = 10


directory = os.fsencode(directory_in_str)
os.system('mkdir -p ' + directory_in_str + '/et_files/' )
pathlist = Path(directory_in_str).glob('**/*.Miniaturization')
set_of_scripts = set()
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    ''' from the path we need to extract the script name and put it a set'''
    script_path = path.name.split('.')
    if script_path[0] == prefix:
        script_name = script_path[2]
        algorithm_name = script_path[1]
        if script_name not in set_of_scripts:
            ''' we add it to the set'''
            set_of_scripts.add(script_name)
            et = []
            ''' we start to iterating nbofRuns times over all the runs of this script'''
            for index in range (1, nbofRuns):
                temp_name = copy.deepcopy(script_path)
                temp_name[4] = str(index)
                f1 = ".".join(temp_name)
                temp_name[4] = str(index + 1)
                f2 = ".".join(temp_name)
                ''' now get the difference of time using stat'''
                #diff_succ = get_out( 'echo','`stat','-c%Y',f2,'`','-','`stat','-c%Y',f1,'`','|','bc'  )
                d2 = subprocess.run(['stat','-c',"\"%Y\"",directory_in_str+'/'+f2],
                                    stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\"", "").strip()
                d1 = subprocess.run(['stat', '-c%Y', directory_in_str+'/'+f1 ],
                                    stdout=subprocess.PIPE).stdout.decode('utf-8').replace("\"", "").strip()
                time_diff =float('nan')
                try:
                    time_diff = float(d2) - float(d1)
                except ValueError:
                    print ('Error when computing difference between '+ f1 + ' and ' + f2 )
                print(time_diff)
                et.append(time_diff)
            fileoutname = directory_in_str + '/et_files/' + 'ET.' + algorithm_name + '.' +  script_name  + '.csv'
            fout = open(fileoutname, "w")
            for val in et:
                fout.write(str(val))
                fout.write('\n')
            fout.close()
