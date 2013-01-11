ac100-repart
============

ac100 repartitioning helper script.
Contains logic to:
- repartition ac100 for u-boot + gpt
- generate new MBR, EM1 and EM2 partitions after repartitioning.
  MBR, EM1 and EM2 partititons are used by tegrapart code in linux kernel.
  For more information see http://ac100.wikispaces.com/tegrapart (in russian)


Usage
=====
./main.py

Note: script was checked on python 2.6/2.7


TODO
====
- integrate fastboot + gpt to menu
- integrate MBR, EM1, EM2 generation to menu
- integrate other repartitioning options
- integrate backup/restore
