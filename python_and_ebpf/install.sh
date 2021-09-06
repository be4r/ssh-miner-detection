#!/usr/bin/env bash

# not actually a makefile cos theres almost nothing to compile

if [[ ! -f .temp-sshminerdetection-stage1_complete-file ]]; then
#requirements
export DEBIAN_FRONTEND=noninteractive
apt update && apt -y install wget git
# pull go
wget https://golang.org/dl/go1.16.4.linux-amd64.tar.gz -O go.tar.gz && tar -zxf go.tar.gz -C /usr/lib &&  ln -s /usr/lib/go/bin/go /usr/bin/go
rm go.tar.gz
# pull container
git clone https://github.com/containerSSH/containerssh
cd containerssh && go get
cd ..
DOCKER_DIR=`ls ~/go/pkg/mod/github.com/containerssh/docker/* -d`
rm -r $DOCKER_DIR && cp -r .. $DOCKER_DIR
# build binaries
mkdir bin
cd containerssh/
go build -o containerssh cmd/containerssh/main.go
go build -o containerssh-auth cmd/containerssh-testauthconfigserver/main.go
mv containerssh* ../bin
cd ..
# config
# config services
echo 'Now please modify paths in ./services/* to match binaries in ./bin/ (if you wanna relocate them - now`s the time), then start this script again . . .'
touch .temp-sshminerdetection-stage1_complete-file;
else
rm .temp-sshminerdetection-stage1_complete-file
mkdir /etc/containerssh
cp ./services/* /etc/systemd/system/
ssh-keygen -f /etc/containerssh/ssh_host_rsa_key -N `cat /dev/urandom | head | grep -ao '[a-z]' | tr -d '\n'` <<< '\n; y'
echo -e 'To start honeypot, type:\n\tsevice tracessh start'
# dont actually need to modify testserver - functional already present - there's ENV for this purpose
export DEBIAN_FRONTEND=
export CONTAINERSSH_ALLOW_ALL=1
fi;
