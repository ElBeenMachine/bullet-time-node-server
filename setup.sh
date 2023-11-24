echo This wizard will run you through the setup of the bullet-time node server

echo "What is the ID of this node (101 - 150)"
read nodeNum

echo ""

echo "============ System Configuration (10.0.0.$nodeNum) ============"

echo ""

echo Updating system
sudo apt-get update -y && sudo apt-get upgrade -y

sudo hostnamectl set-hostname btns-node-$nodeNum

echo "127.0.1.1               btns-node-$nodeNum" | tee /etc/hosts
echo "127.0.0.1       localhost" | tee -a /etc/hosts
echo "::1             localhost ip6-localhost ip6-loopback" | tee -a /etc/hosts
echo "ff02::1         ip6-allnodes" | tee -a /etc/hosts
echo "ff02::2         ip6-allrouters" | tee -a /etc/hosts

echo Hostname set to btns-node-$nodeNum

mkdir -p /etc/network/interfaces.d

echo ""

echo "Configuring Static IP Address:"

echo "" | sudo tee /etc/network/interfaces.d/eth0
echo "allow-hotplug eth0" | sudo tee -a /etc/network/interfaces.d/eth0
echo "iface eth0 inet static" | sudo tee -a /etc/network/interfaces.d/eth0
echo "address 10.0.0.$nodeNum" | sudo tee -a /etc/network/interfaces.d/eth0
echo "network 10.0.0.0/24" | sudo tee -a /etc/network/interfaces.d/eth0
echo "netmask 255.255.255.0" | sudo tee -a /etc/network/interfaces.d/eth0
echo "gateway 10.0.0.1" | sudo tee -a /etc/network/interfaces.d/eth0

echo ""

echo "Static IP Set"

echo ""

sudo chmod +x ./install.sh
sudo chmod +x ./update.sh

./install.sh

sudo reboot now