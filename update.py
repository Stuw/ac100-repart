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
import struct

print "AC100 repartitioning helper"
print "WARNING: this is test version! Be careful!"

if len(sys.argv) < 2:
	print "Usage: ", sys.argv[0], " <partitiontable.txt>"
	exit(1)

src_file_name = sys.argv[1]


# Partition array indexes names
ID=0
NAME=1
START=2
SIZE=3
SECT_SIZE=4

def add_partition(table, id, name, start, size, sect_size):
	table.append([id, name, start, size, sect_size])

def parse_partitiontable(partitions_file):
	id=""
	name=""
	start=""
	size=""
	sect_size=""
	
	#PartitionId=9
	#Name=CAC
	#DeviceId=18
	#StartSector=163584
	#NumSectors=204800
	#BytesPerSector=2048

	partitions=[]

	for line in partitions_file:
		line = line.strip()
		if not line:
			continue
	
		param, value = line.split("=")
		if param == "PartitionId":
			id = value
		if param == "Name":
			name = value
		if param == "StartSector":
			start = value
		if param == "NumSectors":
			size = value
		if param == "BytesPerSector":
			sect_size = value
			add_partition(partitions, id, name, start, size, sect_size)

	return partitions


def parse_config(config_file):
	id=""
	name=""
	start=0
	size=0
	sect_size=""
	
	#[partition]
	#name=BCT
	#id=2
	#type=boot_config_table
	#allocation_policy=sequential
	#filesystem_type=basic
	#size=3145728
	#file_system_attribute=0
	#partition_attribute=0
	#allocation_attribute=8
	#percent_reserved=0

	partitions=[]

	for line in config_file:
		line = line.strip()
		if not line or line == "[device]":
			continue
	
		if line == "[partition]":
			start = start + size
			continue;

		param, value = line.split("=")
		if param == "id":
			id = value
		if param == "name":
			name = value
		if param == "size":
			if "0x" in value:
				size = int(value,  16)
			else:
				size = int(value)
			size = size / 2048
		if param == "percent_reserved":
			sect_size = 2048
			add_partition(partitions, id, name, start, size, sect_size)

	return partitions
 

def get_partition_by_name(partitions, name):
	for partition in partitions:
		if partition[NAME] == name:
			return partition
	return None 
	
def partitions_after_mbr(partitions):
	count=-1
	for partition in partitions:
		if partition[NAME] == "MBR":
			count = 0
			continue
		if count == -1:
			continue
		count += 1;

	return count;

def find_all(partitions, names):
	for partition in partitions:
		if partition[NAME] in names:
			names.remove(partition[NAME])

	return len(names) == 0;




def form_boot_record(base, partitions):
	records = []

	primary_count = 0
	if base[NAME] == "MBR":
		if len(partitions) > 4:
			primary_count = 3
		else:
			primary_count = len(partitions)
	else:
		primary_count = 1
	
	for i in range(0, primary_count):
		p = [i, "0x83", (int(partitions[i][START]) - int(base[START])) * 4, int(partitions[i][SIZE]) * 4]
		records.append(p)

	extended = partitions[primary_count:]
	if len(extended) == 0:
		return records, []

	ex_idx = primary_count
	ex_size = 0
	for part in extended:
		ex_size += int(part[SIZE])
	p = [ex_idx, "0x05", (int(extended[0][START]) - int(base[START])) * 4, ex_size * 4]
	records.append(p)

	return records, extended

def form_boot_records(partitions):
	mbr_records=[]
	em1_records=[]
	em2_records=[]

	mbr = get_partition_by_name(partitions, "MBR")
	mbr_idx = partitions.index(mbr)
	post_mbr = partitions[mbr_idx + 1 : ]
	mbr_records, tmp = form_boot_record(mbr, post_mbr)
	if len(tmp) == 0:
		return mbr_records, em1_records, em2_records

	em1 = tmp[0]
	if em1[NAME] != "EM1":
		print "WARNING: Incorrect partitioning! EM1 is absent, can't store ", tmp
		exit(1)
	post_em1 = tmp[1:]
	em1_records, tmp = form_boot_record(em1, post_em1)
	if len(tmp) == 0:
		return mbr_records, em1_records, em2_records

	em2 = tmp[0]
	if em2[NAME] != "EM2":
		print "WARNING: Incorrect partitioning! EM2 is absent, can't store ", tmp
		exit(1)
	post_em2 = tmp[1:]
	em2_records, tmp = form_boot_record(em2, post_em2)
	if len(tmp) == 0:
		return mbr_records, em1_records, em2_records

	print "WARNING: not all partitons were adopted."
	print "  ", tmp

	return mbr_records, em1_records, em2_records


def print_array(name, arr):
	print "\n", name
	for item in arr:
		print item

#print_array("MBR", mbr_records)
#print_array("EM1", em1_records)
#print_array("EM2", em2_records)
#print " "

PART_TABLE_OFFSET = 446
PART_RECORD_SIZE = 16
TYPE_OFF = 4
START_OFF = 8
SIZE_OFF = 12

def put_partition_record(br, record):
	print record
	idx = record[0]
	offset = PART_TABLE_OFFSET + PART_RECORD_SIZE * idx
	br[offset + TYPE_OFF: offset + TYPE_OFF + 1] = [int(record[1], 16)]
	br[offset + START_OFF: offset + START_OFF + 4] = struct.pack("I", int(record[2]))
	br[offset + SIZE_OFF: offset + SIZE_OFF + 4] = struct.pack("I", int(record[3]))

def write_boot_record(partitions, base_name, base_partitions):
	if len(partitions) == 0:
		print "No partitions for", base_name
		return

	file_name = "%s.gen" % base_name
	print "Forming", file_name

	base = get_partition_by_name(partitions, base_name)
	if base == None:
		print "Can't find", base_name
		return

	f = ""
	try:
		f = open(file_name, "wb")
	except:
		print "Can't open file", file_name, "for writing"
		return

	br = [0] * int(base[SIZE]) * 2048
	br[510:512] = [0x55, 0xaa]

	for part in base_partitions:
		put_partition_record(br, part)
	f.write(bytearray(br))




def update(src_file_name):
	src_f = ""
	try:
		src_f = open(src_file_name, "r")
	except:
		print "Can't open ", src_file_name
		exit(1)

	partitions = []
	if src_file_name.endswith(".cfg") or src_file_name.endswith(".conf"):
		partitions = parse_config(src_f)
	else:
		partitions = parse_partitiontable(src_f)

	if len(partitions) == 0:
		print "ERROR: No partitions found in source file %s." % src_file_name
		exit(1)
	print partitions

	if partitions_after_mbr(partitions) != 7 or not find_all(partitions, ["MBR", "EM1", "EM2"]):
		print "WARNING: Non-standard partitioning is detected! Please, re-check script results"

	mbr_records, em1_records, em2_records = form_boot_records(partitions)

	write_boot_record(partitions, "MBR", mbr_records)
	write_boot_record(partitions, "EM1", em1_records)
	write_boot_record(partitions, "EM2", em2_records)


update(src_file_name)
