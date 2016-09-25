#! /bin/bash

# Linux kernel version > 3.10 is required
kernel_version=`uname -r`
kernel_version=`echo $kernel_version | sed 's/\([0-9+]\.[0-9+]\).*/\1/'`

sudo apt-get install -y bc

if [ `echo $kernel_version'<'3.1 | bc -l` -eq 1 ]
then
    echo "Linux kernel version > 3.10 is required to install docker"
    exit 1
fi

sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update

sudo apt-get install -y docker-engine

sudo echo -e "[Unit]\nDescription=Docker Socket for the API\n[Socket]\nListenStream=2375\nBindIPv6Only=both\nService=docker.service\n\n[Install]\nWantedBy=sockets.target" > /etc/systemd/system/docker-tcp.socket

sudo systemctl enable docker-tcp.socket
sudo systemctl stop docker
sudo systemctl start docker-tcp.socket
sudo systemctl start docker

# Allow the user to use docker without sudo, but system needs to be rebooted
sudo usermod -aG docker $(whoami)

# Accept traffic on port TCP/5000 for the API 
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT

