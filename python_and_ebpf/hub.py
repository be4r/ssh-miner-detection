#!/usr/bin/python3

#import multiprocessing as mp
import ctypes
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
#import os
#import sys
#import signal
#import stat
from time import sleep

# sess_id | ip | username | docker_id | cgroup_id | process

port = 38393
logs_path = '/home/be4r/bin/bpf/remote/logs'
whitelist = ['127.0.0.1', '85.89.127.33']

class requestHandler(BaseHTTPRequestHandler):
	sessions = []
	cgroups = []
	bpf = None
	trace = {}

	def do_GET(self):
		if self.client_address[0] not in whitelist:
			if self.verbose:
				print('IP not allowed')
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			return
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		d = self.path[1:]
		if d == 'getstats':
			self.getstats()
			return
		if d.startswith('FINISH'):
			if len(d.split('+')) != 2:
				if self.verbose:
					print('Recieved %d args, expected 2' % len(d.split('+')))
			else:
				self.finish_conn(d.split('+')[1])
			return
		else:
			if len(d.split('+')) != 4:
				if self.verbose:
					print('Recieved %d args, expected 4' % len(d.split('+')))
			else:
				self.add_conn(*d.split('+'))
			return
			
	def getstats(self):
		self.wfile.write(str(self.sessions).encode('UTF-8'))

	def finish_conn(self, docker_id):
		ids = [i['docker_id'] for i in self.sessions]
		if docker_id in ids:
			if self.verbose:
				id = ids.index(docker_id)
				print('curr sessions:', self.sessions)
				print('killin %s' % docker_id)
			# os.system('sudo pkill -P %d' % self.sessions[ids.index(id)][4].pid)
			# save to file
			if self.sessions[id]['cgroup_id'] in self.trace:
				# tmp for learning; 
				# can pass trace directly to the tree
				filename = '%s/%s_%s_%.10s.perf' % (logs_path, self.sessions[id]['ip'], self.sessions[id]['username'], docker_id)
				if self.verbose:
					print('writing %s.perf' % filename)
				with open(filename, 'w') as f:
					f.write("%s" % self.trace[self.sessions[id]['cgroup_id']])
				self.trace[self.sessions[id]['cgroup_id']] = []
			else:
				if verbose:
					print('O_o Dumping trace:')
					print(self.trace)
			self.sessions.pop(id)
			self.cgroups.pop(id)
			self.bpf['cgroups'].update(enumerate(self.cgroups + [ctypes.c_uint32(0)]*(255-len(self.cgroups))))

		else:
			if self.verbose:
				print('no such process :/')
		return

	def add_conn(self, sess_id, ip, username, docker_id):
		if docker_id.strip() in [i['docker_id'] for i in self.sessions]:
			if self.verbose:
				print('Already exists!')
			return
		if len(self.sessions)>200:
			with open('%s/last_unsuccessfull_sessions', 'a') as f:
				f.write("%s\n" % self.sessions[:150])
			self.sessions = self.sessions[150:]
			self.cgroups = self.cgroups[150:]
		self.sessions.append({'sess_id': sess_id, 'ip': ip, 'username': username, 'docker_id': docker_id})
		if self.verbose:
			print('Getting cgid: ', end='')
		cgroup_id  = int(subprocess.check_output('ls -di /sys/fs/cgroup/system.slice/docker-%s.scope' % docker_id, shell=True).split(b' ')[0])
		if self.verbose:
			print(cgroup_id)
		self.sessions[-1]['cgroup_id'] = cgroup_id
		if ctypes.c_uint32(cgroup_id) not in self.cgroups:
			self.cgroups.append(ctypes.c_uint32(cgroup_id))
			self.bpf['cgroups'].update(enumerate(self.cgroups))
		return

		
		#def startperf():
		#	os.execlp('bash', 'bash', '-c', 'sudo perf trace -a -G system.slice/docker-%s.scope -o %s/%s_%s_%.10s.perf'
		#		% (docker_id, logs_path, self.sessions[-1][1],self.sessions[-1][2], docker_id))
		#	os.execlp('bash', 'bash', '-c', 'sudo perf trace -a -G docker/%s -o %s/%s_%s_%.10s.perf'
		#		% (docker_id, logs_path, self.sessions[-1][1],self.sessions[-1][2], docker_id))

		#t = mp.Process(target = startperf)
		#self.sessions[-1].append(t)
		if self.verbose:
			print('starting %s' % docker_id)
		#t.start()
		if self.verbose:
			print('started successfully')
		return



def waitforsession(bpf, trace, verbose = 0):
	requestHandler.verbose = verbose
	requestHandler.trace = trace 
	requestHandler.bpf = bpf 
	httpd = HTTPServer(('0',port), requestHandler)
	try:
		print('opened, w8ing')
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()

if __name__ == '__main__':
	waitforsession([], verbose = 1)
