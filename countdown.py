#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sys import stdout
from time import sleep
from subprocess import call
import threading

time = 2

if len(sys.argv) > 1:
	time_arg = sys.argv[1];
	if time_arg.endswith('m'):
		time = float(time_arg[:-1]) * 60
	elif time_arg.endswith('s'):
		time = float(time_arg[:-1])
	else:
		time = float(time_arg)

total_items = 50
per_item = time / float(total_items)
counter = 0
si = 0;
sign = '';
# signs = ["🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚","🕛"]
signs = ["|","/","-","\\"]
per_tick = .07

def get_sign():
	global si
	global sign
	si = si + 1;
	if (si > len(signs)-1): si = 0;
	sign = signs[si]#.encode('utf-8');

def write_results():
	stdout.write("\r%s  %s%s%s" % (sign, ('*' * (total_items-counter)), ('.' * counter), "|"))
	stdout.flush()

def beep():
	call(["echo", "-n", "\a"])

class IncrementThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global counter
		while counter < total_items:
			counter = counter + 1
			write_results();
			sleep(per_item);
		stdout.flush()

class ClockThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while counter < total_items:
			get_sign();
			write_results();
			sleep(per_tick);

thread1 = IncrementThread()
thread2 = ClockThread()
thread1.start()
thread2.start()

threads = []

threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
    t.join()

beep()
stdout.write("\rDone%s" % (" " * (total_items + 1)))
stdout.flush()
print