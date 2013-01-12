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
import subprocess


def execute( command, verbose = True ):
	if verbose:
		print 'cmd "%s" ...' % command 

	ret = subprocess.call(args = command, shell = True)
	if ret and verbose:
		print 'ret = %i\n' % (ret)

	return ret


def cwd():
	if cwd.path == None:
		cwd.path = os.getcwd()
	return cwd.path
cwd.path = None


def binaries():
	return cwd() + "/binaries/"

def configs():
	return cwd() + "/configs/"

def externals():
	return cwd() + "/externals/"

def generated():
	return cwd() + "/generated/"

# External
def bct_dump():
	return externals() + "cbootimage/bct_dump"

def cbootimage():
	return externals() + "cbootimage/cbootimage"

def nvflash():
	return externals() + "nvflash/nvflash"

def fastboot():
	return externals() + "nvflash/fastboot.bin"


# Binaries
def ac100_bct():
	return binaries() + "ac100.bct"


# Perform cwd initialization	
if __name__ != '__main__': 
	cwd()


