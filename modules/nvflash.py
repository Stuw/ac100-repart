#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Andrey Danin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# How to download partition table:
#
#ret = init()
#print "init executed with result %i" % ret
#
#part_table = 'tests/partitiontable.txt'
#ret = backup_partitiontable(part_table)
#if ret == 0:
#	detect_storage_size(part_table)
#else:
#	print 'Can\'t backup partition table'


import sys
import struct

from common import execute, nvflash, fastboot


def init():
	return execute('sudo "%s" --bl "%s" --sync' % (nvflash(), fastboot()))


def backup():
	return execute('sudo "%s" -r --rawdeviceread 0 1536 ac100-2.img \
									  --rawdeviceread 1536 256 ac100-3.img \
									  --rawdeviceread 1792 1024 ac100-4.img \
									  --rawdeviceread 2816 2560 ac100-5.img \
									  --rawdeviceread 5376 4096 ac100-6.img \
									  --rawdeviceread 9984 153600 ac100-8.img \
									  --rawdeviceread 163584 204800 ac100-9.img \
									  --rawdeviceread 368384 1024 ac100-10.img \
									  --rawdeviceread 369664 632320 ac100-12.img \
									  --sync' % nvflash())


def backup_partitiontable(partitiontable = 'backup_part_table-`date +%F_%T`.txt'):
	return execute('sudo "%s" -r --getpartitiontable "%s" --sync' % (nvflash(), partitiontable))


def restore():
	mbr = ''
	em1 = ''
	em2 = ''
	return execute('sudo "%s" -r --rawdevicewrite 0 1536 ac100-2.img \
									  --rawdevicewrite 1536 256 ac100-3.img \
									  --rawdevicewrite 1792 1024 ac100-4.img \
									  --rawdevicewrite 2816 2560 ac100-5.img \
									  --rawdevicewrite 5376 4096 ac100-6.img \
									  --rawdevicewrite 9472 512 "%s" \
									  --rawdevicewrite 477184 256 "%s" \
									  --rawdevicewrite 2526464 256 "%s" \
									  --sync' % (nvflash(), mbr, em2, em1))


def repart(bct, config):
	return execute('sudo "%s" --bct "%s" --setbct \
						  --bl "%s" \
						  --configfile "%s" \
						  --create \
						  --sync' % (nvflash(), bct, fastboot(), config))


def push_part(id, file):
	return execute('sudo "%s" -r --download %d "%s" --sync' % (nvflash(), id, file))


if __name__ == '__main__': 
	ret = init()
	print "init executed with result %i" % ret

	part_table = 'tests/partitiontable.txt'
	ret = backup_partitiontable(part_table)
	if ret == 0:
		detect_storage_size(part_table)
	else:
		print 'Can\'t backup partition table'

