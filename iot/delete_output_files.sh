#!/bin/bash
###receives as parameter the name of the js file without extension
rm -f values_achieved_$1*
rm -f VAR.NSGAII.$1*
rm -f FUN.NSGAII.$1*
rm -f HV.$1*
rm -f benchmark_$1*.log

