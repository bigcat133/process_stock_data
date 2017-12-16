#! /bin/bash


for file in ./*
do
    if test -f $file ; then
	base=`basename $file`
	if [ $base == "format.sh" ] ; then
	    continue
	fi

	echo $file
	sed -i "s/,/\n/g" $file
	sed -i "s/sh/0/g" $file
	sed -i "s/sz/1/g" $file
    fi
done
