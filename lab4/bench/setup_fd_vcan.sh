sudo modprobe vcan

sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 mtu 72
sudo ip link set up vcan0


sudo ip link add dev vcan1 type vcan
sudo ip link set vcan1 mtu 72
sudo ip link set up vcan1
