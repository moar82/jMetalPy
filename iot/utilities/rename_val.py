import os
from pathlib import Path

"""
.. module:: miniaturization
   :platform: Unix, Windows
   synopsis: This script rename values_achieved files to use JmetalPy naming
   xxx.ALG.SCRIPT.js.RUN
.. moduleauthor:: Rodrigo Morales <rodrigomorales2@acm.org>
"""

'''Hardcoded settings'''
directory_in_str = '/home/moar82/Documents/iot_miniaturization/results/sunspider/crypto-md5_To_string-validate-input_values_achieved'
prefix = 'NSGAII'

directory = os.fsencode(directory_in_str)
os.system('mkdir -p ' + directory_in_str + '/val_files/')
pathlist = Path(directory_in_str).glob('**/values_achieved_*')

for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    ''' from the path we need to extract the script name and put it a set'''
    val_path = path.name.split('.')[0]
    val_file = val_path.split('_')[2]
    if val_file[len(val_file)-2].isdigit():
        idx = len(val_file)-2
    else:
        idx = len(val_file) - 1
    consecutive = int(val_file[idx:])
    script_name = val_file[0:idx]
    newname = 'VAL.'+ prefix + '.' + script_name + '.js.' + str(consecutive)
    print (newname)
    os.system('cp -f ' + path_in_str + ' ' + directory_in_str + '/val_files/' + newname )

