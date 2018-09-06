#!/bin/bash
for ((i = 1; i <= $1; i++)); do python3 rs_full_settings.py $i; done
