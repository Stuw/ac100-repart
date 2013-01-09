#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import textwrap


def print_commands(prompt, commands): 
	sys.stdout.write(textwrap.dedent("%s\n") % prompt) 
	for cmd in commands:
		print "%s - %s" % (cmd, commands[cmd][1])


def quit(): 
	raise SystemExit() 

def nop():
	return 0

def menu(commands):
	choice = None
	res = None
	while choice == None: 
		choice = raw_input("Command: ") 
		if choice in commands: 
			res = commands[choice][0]() 
		else: 
			choice = None 
			print_commands("Valid commands are:", commands)

	return (choice, res)

if __name__ == '__main__':
	main_commands = { 
		'q': [(lambda: quit()), "quit from script"], 
		'n': [(lambda: nop()), "nop"], 
	} 

	while True:
		(c, r) = menu(main_commands)
		print "Choise: ", c
		print "Result: ", r
