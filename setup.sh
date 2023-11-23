echo This wizard will run you through the setup of the bullet-time node server

echo "What is the ID of this node (101 - 150)"
read nodeNum

echo ""

echo "============ System Configuration (10.0.0.$nodeNum) ============"
sudo hostnamectl set-hostname btns-node-$nodeNum
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