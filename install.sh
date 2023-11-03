echo "Installing Python"
sudo apt-get install python3 -y

echo "Installing Pip"
sudo apt-get install python3-pip -y

echo "Installing necessary python modules"
pip install -r requirements.txt

echo ""
echo "Installing necessary camera modules"
sudo apt install python3-picamera2 -y