echo "Updating Repository"

echo "Stopping running service"
sudo systemctl stop bulletTime.service

echo "Disabling service"
sudo systemctl disable bulletTime.service

echo "Pulling latest production build from GitHub"
git stash
git stash drop
git pull

echo "Running install script"
sudo chmod +x ./install.sh
./install.sh