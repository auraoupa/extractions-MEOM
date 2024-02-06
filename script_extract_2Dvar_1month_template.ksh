#!/bin/bash

CONFIG=CONFIGURATION
CASE=SIMULATION
REG=REGIONNAME
SREG=REGIONABR
VAR=VARIABLE
VARNAME=VNAME
FREQ=FREQUENCY
YYYY=YEAR
MM=MONTH
TYP=FILETYP
SDIR=SOURCEDIR
STYLE=STYLENOM
XY=XTRACTINDICES

TDIR=SCPATH/${CONFIG}/${CONFIG}-${CASE}/${REG}/${FREQ}
mkdir -p $TDIR
cd $TDIR

echo "We are in " $TDIR

BRODEAU_NST=brodeau_nst
BRODEAU=brodeau
MOLINES=molines

ulimit -s unlimited

if [ "${STYLE}" == "${BRODEAU_NST}" ]; then
	for file in $(ls ${SDIR}/*/NST/${CASE}-${CONFIG}_${FREQ}_${YYYY}${MM}??_${YYYY}${MM}??_${TYP}.nc4); do
		day1=$(basename $file | awk -F_ '{print $3}')
		DD1=$(echo "${day1: -2}")
		day2=$(basename $file | awk -F_ '{print $4}')
                DD2=$(echo "${day2: -2}")
		fileo=${CONFIG}${SREG}-${CASE}_y${YYYY}m${MM}d${DD1}-d${DD2}.${FREQ}_${VAR}.nc
		if [ ! -f  $fileo ]; then
			echo $fileo
			NCOPATH/ncks -O -F ${XY} -v ${VARNAME} $file $fileo
		fi
	done
fi

