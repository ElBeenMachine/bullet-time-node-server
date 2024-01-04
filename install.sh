echo ""

echo "==================== Installing Python ===================="
sudo apt-get install python3 python3-pip -y

echo ""

echo "================= Installing Dependencies ================="
sudo apt-get install python3-socketio python3-aiohttp python3-picamera2 python3-opencv python3-numpy -y

echo ""

echo "==================== Enabling Service ====================="
sudo mkdir -p /etc/btns
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