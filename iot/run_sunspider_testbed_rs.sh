#!/bin/bash

for file in *.js
do
	for ((i = $1; i <= $2; i++))
	 do 
		python3 rs_full_settings.py $i ${file}
	done
done
