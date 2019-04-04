#!/bin/bash

source venv/bin/activate > log.txt
nice python3 databaseExtender.py > log.txt
echo $'\r' > log.txt
