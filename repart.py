#!/usr/bin/python

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

import sys
from nvflash import *

print "AC100 repartitioning helper"
print "WARNING: this is test version! Be careful!"


#ret = init()
#print "init executed with result %i" % ret
#
#part_table = 'tests/partitiontable.txt'
#ret = backup_partitiontable(part_table)
#if ret == 0:
#	detect_storage_size(part_table)
#else:
#	print 'Can\'t backup partition table'
#

part_table = sys.argv[1]
size = detect_storage_size(part_table)
print 'storage size %i Gb' % size

generate_new_partitions(part_table)
