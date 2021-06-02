## Something
Tracing stuff: ./python\_and\_ebpf

Origin of modified module: [docker](https://github.com/containerSSH/docker)

Everything else can be found at [github](https://github.com/containerSSH/containerssh/) or [this website](https://containerssh.io/)


**localhost:38393/getstats** to return currently running sessions

*(also its possible to leave **dangling** sessions by somehow incorrectly closing connection on cli side; may need fixing; for ex, 61.177.173.x usually does this)*


## How to

+ ssh-keygen -f ./config/ssh\_host\_rsa\_key
+ cp -r config /etc/containerssh
+ create dir to mount /tmp into (def: /home/be4r/tmp) and change path in ./docker\_impl.go:193
+ build bineries: 
  + sudo go build -o containerssh-auth cmd/containerssh/main.go
  + sudo go build -o containerssh cmd/containerssh/main.go
  + change paths in ./python\_and\_ebpf/services/
+ cp ./python\_and\_ebpf/services/* to /etc/systemd/system/
+ service tracessh start


----
### makefile incoming
~                           
