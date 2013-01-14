ac100-repart
============

ac100 repartitioning helper script.
Contains logic to:
- repartition ac100 for u-boot + gpt
- repartition ac100 for fastboot + gpt
- repartition ac100 to use android 4.x + ubuntu
- run uboot sos image on ac100

Checked:
- u-boot+gpt case - works fine.
- android+ubuntu case - repartition works fine
(generated MBR, EM1, EM2 was not checked yet)
- sos image is loaded on ac100

Usage
=====
./main.py

Note: script was checked on python 2.6/2.7


TODO
====
- integrate backup/restore
