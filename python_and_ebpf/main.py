from threading import Thread
from bcc import BPF
from time import sleep
import hub
import load_bpf
import training

trace = {}

print('Loading BPF . . . ')
b = BPF('prog.c')
print('DONE')

def f1():
	hub.waitforsession(b, trace, verbose = 1)

def f2():
	load_bpf.trace = trace
	load_bpf.b = b 
	load_bpf.listen()


# containerssh -> python
t1 = Thread(target = f1)
# python <-> bpf
t2 = Thread(target = f2)

t1.start()
t2.start()

while True:
	for sess_id in trace:
		if len(trace[sess_id]) >= 25 * 300:
			if training.predict_on_trace(trace[sess_id], 0.9):
				# logout and ban here:
		    #   import os or something... 
				#	TODO: get   sessions   from hub.py for username/ip
				#
		    # loginctl kill-session %sessname%
				# os.system('iptables -t mangle -A INPUT --src %s -j DROP' % ip)
		    # os.system('pkill -u %s && skill -u %s && killall -u %s' % ((username,)*3))
		    # os.system('usermod -L -s /usr/sbin/nologin %s' % username)
			else:
				# TODO: add last_check_time, sort by last_check_time, always view the oldest; 
				# TODO: remove next line
				trace[sess_id] = {}
		    pass
	sleep(5)
				

t1.join()
t2.join()
