#!/usr/bin/python

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


def execute( command, verbose = False ):
	if verbose:
		print 'cmd "%s" ...' % command 

	ret = subprocess.call(args = command, shell = True)
	if ret and verbose:
		print 'ret = %i\n' % (ret)

	return ret


def binaries():
	return os.getcwd() + "/binaries/"

def configs():
	return os.getcwd() + "/configs/"

def externals():
	return os.getcwd() + "/externals/"

def generated():
	return os.getcwd() + "/generated/"

# External
def bct_dump():
	return externals() + "cbootimage/bct_dump"

def cbootimage():
	return externals() + "cbootimage/cbootimage"

# Binaries
def ac100_bct():
	return binaries() + "ac100.bct"
