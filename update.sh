echo "Switching to non-production directory"

echo "Updating Repository"

echo "Stopping running service"
sudo systemctl stop bulletTime

echo "Disabling service"
sudo systemctl disable bulletTime

echo "Pulling latest production build from GitHub"
git stash
git stash drop
git checkout production
git pull

echo "Running install script"
sudo chmod +x ./install.sh
./install.sh