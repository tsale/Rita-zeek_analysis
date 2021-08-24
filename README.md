# Rita-zeek_analysis
Script to install rita and zeek and then analyze related logs. This script is tested to work in Ubuntu 20.04.

### Usage
```
$ python3 rita-zeek_analysis.py -h
usage: rita-zeek_analyzer.py [-h] [-i] [-a] [-d DATASETNAME]

optional arguments:
  -h, --help            show this help message and exit
  -i, --install         [*] Install Rita/Zeek/MongoDB for Ubuntu 20.4
  -a, --analyze         [*] Convert PCAPs to zeek logs and analyze with rita
  -d DATASETNAME, --datasetname DATASETNAME
                        [*] Dataset name of the rita import (Dataset name)
```
