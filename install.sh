echo ""

echo "==================== Installing Python ===================="
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y

echo ""

echo "================= Installing Dependencies ================="
sudo apt-get install python3-socketio -y
sudo apt-get install python3-aiohttp -y
sudo apt-get install python3-picamera2 -y

echo ""

echo "==================== Enabling Service ====================="
sudo mkdir /etc/btns
sudo cp ./. /etc/btns/. -r
sudo cp ./bulletTime.service /lib/systemd/system/bulletTime.service
sudo chmod 644 /lib/systemd/system/bulletTime.service
chmod +x ./main.py
sudo systemctl daemon-reload
sudo systemctl enable bulletTime.service
sudo systemctl start bulletTime.service

systemctl status bulletTime.service

sudo apt autoremove -y

echo Setting Permissions
cd ../
sudo chown -R admin:admin ./btns