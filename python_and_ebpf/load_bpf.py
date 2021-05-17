from threading import Thread
from socket import socket
import ctypes
#import numpy as np
#import os
from time import sleep
#from tree import *
#from pprint import pprint
#from bcc import BPF
import subprocess
#import create_bpf

shutdown_time = -1
output_path = '/home/be4r/bin/bpf/remote/logs/'
trace = {}
flag = True
b = None
# have file pathname as one of args
path_syscalls = [2, 6, 21, 59, 85, 87, 94, 254, 257, 258, 259, 260, 261, 263, 267, 268, 269, 280, 303]


def event_listener(cpu, data, size):
	d = b['events'].event(data)
	if d.cg not in trace.keys():
		trace[d.cg] = []
#	print(d.cg, d.comm, d.id)
	trace[d.cg].append((d.comm,d.id))
	'''
		if d.id in path_syscalls:
			print(d.id, d.cg, d.path)
		else:
			print(d.id, d.cg)
	'''
	return

def listen():
	b['events'].open_perf_buffer(event_listener)
	def set_timer():
		if shutdown_time == -1:
			return
		sleep(shutdown_time)
		global flag
		flag = False

	t = Thread(target = set_timer)

	print('Created %d kprobes' % len(b.kprobe_fds))
	print('Listening', ' for %d seconds . . .' % shutdown_time if shutdown_time != -1 else '. . .')

	t.start()
	while flag:
		try:
			b.perf_buffer_poll()
		except ValueError:
			continue
		except KeyboardInterrupt:
			break



if __name__ == '__main__':
	cgroups = list(enumerate(
		map(lambda x: ctypes.c_uint32(int(x)), 
			subprocess.check_output('ls -di /sys/fs/cgroup/system.slice/docker-*.scope', shell=True).split()[::2])))
	b['cgroups'].update(cgroups)
	listen()
