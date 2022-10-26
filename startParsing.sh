#!/bin/bash





echo "1 - Парсить trust 
2 - Парсить дом.рф
3 - Парсить auction
4 - Парсить osobnyaki
5 - Парсить KF
6 - Парсить ires
7 - Парсить rentavik
8 - Парсить reka
20 - Закончить работу"

read -p "Выберите действие: " input

if [ "$input" = "20" ]; then
    exit 
fi
 
pip3 install -r requirements.txt

if [ "$input" = "1" ]; then
    cd ./trust
    python3 main.py
fi
if [ "$input" = "2" ]; then
    cd ./dom
    python3 main.py
fi
if [ "$input" = "3" ]; then
    cd ./auction-house
    python3 main.py
fi
if [ "$input" = "4" ]; then
    cd ./osobnyaki
    python3 main.py
fi
if [ "$input" = "5" ]; then
    cd ./KF
    python3 main.py
fi
if [ "$input" = "6" ]; then
    cd ./ires
    python3 main.py
fi
if [ "$input" = "7" ]; then
    cd ./rentavik
    python3 main.py
fi
if [ "$input" = "8" ]; then
    cd ./reka
    python3 main.py
fi

