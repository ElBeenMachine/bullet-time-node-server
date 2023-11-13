echo "Installing Python"
sudo apt-get install python3 -y

echo "Installing Pip"
sudo apt-get install python3-pip -y

echo "Installing necessary python modules"
sudo apt install python3-flask

echo ""
echo "Installing necessary camera modules"
sudo apt install python3-picamera2 -y

echo ""
echo "Making update script executable"
chmod +x ./update.sh

echo "Copying to system folder"
<<<<<<< Updated upstream
=======
sudo mkdir /etc/bullet-time
>>>>>>> Stashed changes
sudo cp ./. /etc/bullet-time/.

echo ""
echo "Copying service file to /lib/systemd/system/"
sudo cp ./bulletTime.service /lib/systemd/system/bulletTime.service

echo "Enabling service"
sudo chmod 644 /lib/systemd/system/bulletTime.service
chmod +x ./main.py
sudo systemctl daemon-reload
sudo systemctl enable bulletTime.service
sudo systemctl start bulletTime.service