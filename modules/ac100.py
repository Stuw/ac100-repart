#!/bin/env python

import os.path
import shutil
import sys

from common import ac100_bct, binaries, configs, generated
from bct import gen_bct
from update import generate_new_partitions
from nvflash import init, repart, backup_partitiontable, push_part


class AC100:
	def __init__(self):
		print "AC100 class init"
		return None


	def repart_gpt(self, bootloader, config):
		print "AC100 repartition for GPT"

		self.bootloader = binaries() + bootloader
		self.config = configs() + config

		(res, self.bct) = gen_bct(self.bootloader)
		if res != 0:
			return res

		return self.repart()


	def repart_vendor(self, bootloader, config):
		print "AC100 repartition for vendor scheme"
		self.bootloader = binaries() + bootloader
		self.config = configs() + config

		(res, self.bct) = gen_bct(self.bootloader)
		if res != 0:
			return res

		res = self.repart()
		if res != 0:
			return res

		part_table = generated() + "partitiontable.txt"
		res = backup_partitiontable(part_table)
		if res != 0:
			return res

		res = generate_new_partitions(part_table)
		if res != 0:
			return res

		#TODO: generate_new_partitions shoud return file names and IDs
		push_part(7, "MBR.gen")
		push_part(7, "EM1.gen")
		push_part(7, "EM2.gen")

		return 0


	def check_files(self):
		if  not os.path.isfile(self.bootloader) or \
			not os.path.isfile(self.bct) or \
			not os.path.isfile(self.config):
				return False
		return True


	def prepare_bootloader(self):
		try:
			new_bl = generated() + "bootloader.bin"
			print "Copy %s to %s" % (self.bootloader, new_bl)
			shutil.copyfile(self.bootloader, new_bl)
			self.bootloader = new_bl
		except shutil.Error as e:
			print e
			return False
		except IOError as e:
			print "I/O error({0}): {$1}".format(e.errno, e.strerror)
			return False
		except:
			print "Error: %s" % (sys.exc_info()[1])
			return False

		return True


	def repart(self):
		print "AC100 repartition:"
		print "  bl:  %s" % self.bootloader
		print "  bct: %s" % self.bct
		print "  cfg: %s" % self.config

		if not self.check_files():
			print "Error: not all files are exist"
			return 2

		if not self.prepare_bootloader():
			print "Error: can't prepare bootloader for config"
			return 3

		# chdir to ./generated, otherwise nvflash will not find bootloader.bin
		os.chdir(generated())

		res = repart(self.bct, self.config)
		if res != 0:
			print "Error: failed to repart using nvflash"
			return res

		return 0

