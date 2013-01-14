#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013 Andrey Danin

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

import os

from common import execute, bct_dump, cbootimage, generated, binaries

def gen_bct(bootloader, bct):
	bct_config = generated() + "bct.cfg"

	#./bct_dump ./ac100.bct.orig > bct.cfg
	res = execute(bct_dump() + " " + bct + " > " + bct_config)
	if res != 0:
		return res, None

	# Add bootloader at the end of bct.cfg
	res = execute("echo 'BootLoader = " + bootloader + ",0x00108000,0x00108000,Complete;' >> " + bct_config)
	if res != 0:
		return res, None

	new_bct = generated() + "ac100.bct"
	#./cbootimage -d ./bct.cfg ac100.bct.new
	res = execute(cbootimage() + " -d " + bct_config + " " + new_bct)
	if res != 0:
		return res, None

	res = execute("truncate " + new_bct + " -s 4080")
	if res != 0:
		return res, None

	return 0, new_bct

