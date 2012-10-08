ac100-repart
============

ac100 repartitioning helper script. It is used to generate new MBR, EM1 and EM2 partitions after repartitioning.
MBR, EM1 and EM2 partititons are used by tegrapart code in linux kernel.

For more information see http://ac100.wikispaces.com/tegrapart (in russian)


Usage
=====
./update.py partitiontable.txt

Result:
Dumped partitions and .gen files

Note: script was checked on python 2.6/2.7
