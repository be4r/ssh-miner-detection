#!/usr/bin/python3

import multiprocessing as mp
import subprocess
from socket import socket
import os
import signal
import stat
from time import sleep

# sessid | ip | username | dockerid | process

fifopath = '/tmp/_pipe'
logs_path = '/home/be4r/stuff/bpf/logs'

def waitforsession(cgroups, verbose = 0):
	sessions = []
	status = 0
	f = open(fifopath, 'r')
	if verbose:
		print('opened, w8ing')
	while True:
		d = f.read()
		if len(d) == 0:
			sleep(.05)
		else:
			#print(d)
			#continue
			if d.startswith('FINISH'):
				id = d.split(' ')[1]
				ids = [i[3] for i in sessions]
				if id in ids:
					if verbose:
						print('killin %s' % id)
					### KILL HERE ###
					##=#=#=#=#=#=#=#=##
					#      P O P      #
					##=#=#=#=#=#=#=#=##
					# this _might_ not work, but doesnt actually matter cos no syscalls on dead cgroup
					print('curr sessions:', sessions)
					sessions[ids.index(id)][4].terminate()
					print("Killall: %d" % os.system('sudo killall perf'))
                                        #TODO: add wait() here to purge zombie
					try:
						cgroups.pop(ids.index(id))
						sessions.pop(ids.index(id))
					except:
						pass
					### KILL ENDS HERE ###
				else:
					if verbose:
						print('no such process :/')
				#kill perf on {id}
				continue
			else:
				sessions.append(list(d.split(" ")))
				id = sessions[-1][3].strip()
				sessid = sessions[-1][0].strip()
				if verbose:
					print('starting %s' % id)
				# bcc cant cap docker ?? 
				#id_num = int(subprocess.check_output('ls -di /sys/fs/cgroup/systemd/docker/%s' % id, shell=True).split(b' ')[0])

				### START HERE ###
				# sudo perf trace -a -G docker/0e5b8d3079775d759a02a6931e93253d453146e031c8af6958fa388789f121d6 2>&1 | grep --line-buffered -oE '[[:alnum:]]+\('|sed 's/a/b/g'
				
				#continue
				# # # cgroups.append(id_num)

				# create_bpf.create(id_num)
				def startperf():
					#os.execlp('perf', 'perf', 'trace', '-a', '--cgroup', '/docker/%s' % id, '-o', 'perf_%s' % sessid)
                                        # 2>&1 | grep --line-buffered -oE "[[:alnum:]]+\\(.+\\)" >
					os.execlp('bash', 'bash', '-c', 'sudo perf trace -a -G docker/%s -o %s/%s_%s_%.10s.perf'  # 
						% (id, logs_path, sessions[-1][1],sessions[-1][2], id))
					#print(os.system('perf trace -a -G docker/%s 2>&1 | grep --line-buffered -oE "[[:alnum:]]+\\(" > %.10s.perf' % (id, id)))
					#os.execlp('ls', 'ls', '-di', '/sys/fs/cgroup/systemd/docker/%s' % id)
				t = mp.Process(target = startperf)
				sessions[-1].append(t)
				t.start()
				### START ENDS ###
				continue

if not os.path.lexists(fifopath) or not stat.S_ISFIFO(os.stat(fifopath).st_mode):
	os.mkfifo(fifopath)

if __name__ == '__main__':
	waitforsession([])
