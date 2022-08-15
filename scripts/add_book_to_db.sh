#!/usr/bin/env bash

if [ $# -lt 2 ]
then
    echo "Insufficient arguments supplied"
    exit 1
fi

ESTC_NO=$1
BOOK_STRING=$2

if [ $# -eq 3 ]
then
  export PRINTER_NAME=$3
else
  echo "Printer name not specified, defaulting to printer name from book string...";
  IFS='_'; SPLIT_BOOK_STRING_ON_UNDERSCORE=(${BOOK_STRING}); unset IFS;
  PRINTER_NAME=${SPLIT_BOOK_STRING_ON_UNDERSCORE[0]}
fi

echo -e "ADDING ===> <ESTC No.: ${ESTC_NO}, Book String: ${BOOK_STRING}, Printer Name: ${PRINTER_NAME}>";
OUTPUT=$(cd /ocean/projects/hum160002p/shared/books/code && python add_book_to_api.py ${ESTC_NO} ${BOOK_STRING} --printer ${PRINTER_NAME})
echo $OUTPUT