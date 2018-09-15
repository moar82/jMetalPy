#!/bin/bash
for ((i = $1; i <= $2; i++)); do python3 nsgaii_full_settings.py $i; done
