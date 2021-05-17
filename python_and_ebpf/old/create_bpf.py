#!/usr/bin/python3

from bcc import BPF

'''
в тупую вешает пробы на все сисколы; еще можно параметры возвращать, но придется заморочиться немного
'''

def create(cg_id, inputfile = 'syscalls2.txt', outputfile = 'syscalls.c'):
	
	b = BPF(text='')

	syscalls = []

	header = '''BPF_PERF_OUTPUT(events);

	struct data_t {
		uint32_t syscall;
		//uint32_t pid; //excessive? process name instead?
		uint32_t cgroup;
	};'''

	print('Reading syscalls from %s . . . ' % inputfile)
	try:
		with open(inputfile, 'r') as f:
			for i in f:
				if i.startswith('#'):
					continue
				id, name = i.rstrip().split(' ')
				print('\r -- %s  %s              ' % (id, name), end='')
				#name = b.get_syscall_fnname(name).decode('UTF-8')
				name = '__x64_sys_' + name
				syscalls.append((name, int(id)))
			print('\r'+' '*70, end='')
			print('\rDONE')

		print('Writing BPF to %s (cg: %d) . . . ' % (outputfile, cg_id))
		with open(outputfile, 'w') as f:
			f.write(header)
			for syscall in syscalls:
				f.write('''
		int kprobe__%s(struct pt_regs* ctx){
			struct data_t data = {};
			data.cgroup = bpf_get_current_cgroup_id();
			data.syscall = %d;
			if (data.cgroup == %d) {
				events.perf_submit(ctx, &data, sizeof(data));
			}
			return 0;
		}''' % (*syscall, cg_id))
		print('DONE')
	except Exception as e:
		print('Something went wrong: %s' % str(e))
		quit()


if __name__ == '__main__':
	create(int(__import__('subprocess').check_output('ls -di  /sys/fs/cgroup/systemd/user.slice/user-1000.slice/session-*', shell=True).split()[0]))