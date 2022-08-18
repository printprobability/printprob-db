#!/usr/bin/env bash

if [ $# -lt 1 ]
then
    echo "Missing argument!"
    echo "Usage: ./add_book.sh <book_string> <optional-printer-name-override>"
    exit 1
fi

BOOK_STRING=$1
IFS='_'; SPLIT_BOOK_STRING_ON_UNDERSCORE=(${BOOK_STRING}); unset IFS;
ESTC_NO=${SPLIT_BOOK_STRING_ON_UNDERSCORE}[1]

if [ $# -eq 2 ]
then
  export PRINTER_NAME=$2
else
  echo "Printer name not specified, defaulting to printer name from book string...";
  PRINTER_NAME=${SPLIT_BOOK_STRING_ON_UNDERSCORE[0]}
fi

echo -e "ADDING ===> <ESTC No.: ${ESTC_NO}, Book String: ${BOOK_STRING}, Printer Name: ${PRINTER_NAME}>";
OUTPUT=$(cd /ocean/projects/hum160002p/shared/books/code && python add_book_to_api.py ${ESTC_NO} ${BOOK_STRING} --printer ${PRINTER_NAME})
echo $OUTPUT
