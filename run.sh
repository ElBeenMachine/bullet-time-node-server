echo "Installing Pip"
sudo apt-get install python3-pip

echo "Installing necessary python modules"
pip install -r requirements.txt

echo ""
echo "Installing necessary camera modules"
sudo apt install -y python3-picamera2

echo ""
echo "Running Server"
python main.py