#!/bin/bash

for file in *.js
do
	for ((i = $1; i <= $2; i++))
	 do 
		python3 min_iot_sway.py $i ${file}
	done
done
