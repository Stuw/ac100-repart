#!/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import textwrap

sys.path.insert(0, os.path.relpath("./modules"))
from menu import menu, print_commands
from common import bct_dump, cbootimage, externals, generated
from bct import *
from ac100 import AC100


def quit(): 
	raise SystemExit() 

def repart_gpt_uboot():
	ac100 = AC100()
	res = ac100.repart_gpt("uboot-ac100.bin", "part-gpt-uboot.cfg")
	print "Repartitioning finished with code %d" % res

	return res


main_commands = { 
	'q': [(lambda: quit()), "quit"], 
	'n': [(lambda: None), "no operation, just example"],
	'u': [(lambda: repart_gpt_uboot()), "repartition ac100 to use u-boot"],
} 


def init_externals():
	if not os.path.isdir(generated()):
		os.makedirs(generated())

	if  os.path.isfile(bct_dump()) and \
		os.path.isfile(cbootimage()) and \
		os.path.isfile(externals() + "nvflash/nvflash"):
				return None
	
	print "Initialize externals..."
	res = execute("./init-externals.sh > ./generated/init.log 2>&1")
	if res != 0:
		print "Failed with code %d.\nLog file is ./generated/init.log" % res
		quit()
	else: 
		print "Done.\n"


if __name__ == '__main__':
	init_externals()

	print_commands("Select a command: ", main_commands)
	while True:
		(choice, result) = menu(main_commands)
