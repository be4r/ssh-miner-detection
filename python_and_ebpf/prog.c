#include <linux/sched.h>
#define MAX_CGROUPS 5
struct data {
	char comm[TASK_COMM_LEN];
	long id;
	long cg;
};


BPF_PERF_OUTPUT(events);
BPF_ARRAY(cgroups, u32, MAX_CGROUPS);

TRACEPOINT_PROBE(raw_syscalls, sys_enter) {
	u32 cg = bpf_get_current_cgroup_id();
	u32 *cg_ptr;
	u32 i = 0;
	bool flag = false;
	for(i = 0; i < MAX_CGROUPS; ++ i) {
		u32 i_secure = i; //avoid potential inf loop
		if (cg_ptr = cgroups.lookup(&i_secure)) {
			if (*cg_ptr == cg) {
				flag = true;
			}
		}
	}
	if (!flag) return 0;
	struct data data;
	bpf_get_current_comm(&data.comm, sizeof(data.comm));
	data.cg = cg;
	data.id = args->id;
	events.perf_submit((struct pt_regs *)args, &data, sizeof(data));

	return 0;
}
