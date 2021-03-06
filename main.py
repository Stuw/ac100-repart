#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import textwrap

sys.path.insert(0, os.path.relpath("./modules"))
from menu import menu, print_commands
from nvflash import init
from common import bct_dump, cbootimage, externals, generated, log_file
from bct import *
from ac100 import AC100


def quit(): 
	raise SystemExit() 


def repart_gpt_uboot():
	ac100 = AC100()
	res = ac100.repart_gpt("uboot-ac100.bin", "part-gpt-uboot.cfg")
	print "Repartitioning finished with code %d" % res

	return res


def repart_gpt_fastboot(boot_size):
	ac100 = AC100()
	if boot_size == 1:
		res = ac100.repart_gpt("fastboot-ac100-22.bin", "part-gpt-fastboot-1M.cfg")
	else:
		res = ac100.repart_gpt("fastboot-ac100-21.bin", "part-gpt-fastboot-2M.cfg")

	print "Repartitioning finished with code %d" % res

	return res


def repart_android4():
	ac100 = AC100()
	res = ac100.repart_vendor("fastboot-ac100-21.bin", "part-android-4.cfg")
	print "Repartitioning finished with code %d" % res

	return res


def repart_android_ubuntu():
	ac100 = AC100()
	res = ac100.repart_vendor("fastboot-ac100-21.bin", "part-ubuntu-android.cfg")
	print "Repartitioning finished with code %d" % res

	return res


def uboot_sos():
	res = init(externals() + "uboot-sos.img")
	print "Sos image downloaded with code %d" % res
	return res


def dump_bct():
	ac100 = AC100()
	if ac100.check_bct() != 0:
		print "Failed to dump BCT"
	else:
		print "Re-run your ac100 in recovery mode once again"


main_commands = { 
	'q': [(lambda: quit()), "quit"], 
	'd': [(lambda: dump_bct()), "! dump original BCT, required for repartition"],
	'u': [(lambda: repart_gpt_uboot()), "repartition ac100 to use u-boot"],
	'f1': [(lambda: repart_gpt_fastboot(1)), "EXPERIMENTAL repartition ac100 to use gpt and fastboot 2.2 (boot size is 1M)"],
	'f2': [(lambda: repart_gpt_fastboot(2)), "EXPERIMENTAL repartition ac100 to use gpt and fastboot 2.1 (boot size is 2M)"],
	'a4': [(lambda: repart_android4()), "repartition ac100 to use android 4.x"],
	'au': [(lambda: repart_android_ubuntu()), "EXPERIMENTAL repartition ac100 to use ubuntu + android 4.x"],
	's': [(lambda: uboot_sos()), "load uboot sos image to ac100. Could be used to repart ac100 with gpt."],
} 


def init_externals():
	if not os.path.isdir(generated()):
		os.makedirs(generated())

	if  os.path.isfile(bct_dump()) and \
		os.path.isfile(cbootimage()) and \
		os.path.isfile(externals() + "nvflash/nvflash") and \
		os.path.isfile(externals() + "gpt_surgeon.py") and \
		os.path.isfile(externals() + "uboot-sos.img"):
				return None
	
	print "Initialize externals..."
	res = execute("./init-externals.sh \"%s\"" % log_file())
	if res != 0:
		print "Failed with code %d.\nLog file is ./generated/init.log" % res
		quit()
	print


if __name__ == '__main__':
	init_externals()


	print_commands("Select a command: ", main_commands)
	while True:
		(choice, result) = menu(main_commands)
