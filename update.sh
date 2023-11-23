echo "Updating Repository"

echo "Disabling running service"
sudo systemctl stop bulletTime.service
sudo systemctl disable bulletTime.service

echo "Pulling latest production build from GitHub"
git pull

echo "Running install script"
./install.sh