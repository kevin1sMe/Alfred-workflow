#!/bin/bash

query={query}
result=""

echo ${query} | egrep "^[0-9]{9,10}$"
if [ $? -eq 0 ]
then
    result=`date -r "${query}" "+%Y-%m-%d %H:%M:%S"`
else
    if [ ${query} == "now"  ]
    then
        result=`date +%s`
    else
        result=`date -j -f "%Y-%m-%d %H:%M:%S" "${query}" +%s`
    fi
fi

echo "<?xml version=\"1.0\"?>"
echo "<items>"
echo "  <item uid=\"1\" arg=\"${result}\">"
echo "      <title> ${result} </title>"
echo "      <subtitle>select to copy to clipboard</subtitle>"
echo "  </item>"
echo "</items>"
