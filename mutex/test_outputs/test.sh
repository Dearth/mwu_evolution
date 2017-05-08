#!/bin/bash
# $1 = EXE 
# $2 = test name  
# $3 = port 
# exit 0 = success

rm -rf inc_out.txt inc2_out.txt output.txt
for i in {1..5}
do
	case $2 in
		p1) timeout 1 $1 $i
		if [ $? -eq 124 ]; then
			exit 1
		else
			exec diff inc_out.txt inc_out_$i.txt  > /dev/null 2>&1
		fi;;

		p2) timeout 1 $1 $i
		if [ $? -eq 124 ]; then
			exit 1
		else
			exec diff inc2_out.txt inc2_out_$i.txt  > /dev/null 2>&1
		fi;;

		p3) timeout 1 $1 $i
		if [ $? -eq 124 ]; then
			exit 1
		else 
			if [ `cat inc_out.txt | wc -l` -eq `cat inc2_out.txt | wc -l` ]; then 
				exit 0
			else 
				exit 1
			fi
		fi;;

		p4) timeout 1 $1 $i
		if [ $? -eq 124 ]; then
			exit 1
		else 
			exec diff inc2_out.txt output.txt > /dev/null 2>&1
		fi;;

		n1) timeout 1 $1 $i >& output.txt
		if [ $? -eq 124 ]; then
			exit 1
		else
			exec diff output.txt output_$i.txt > /dev/null 2>&1
		fi;;

		*) exit 2;;        
	esac
done
exit 1
