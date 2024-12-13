#!/bin/bash

# Exit script on any error
set -e

# Update package lists
echo "Updating package lists..."
sudo apt update > /dev/null

# Install prerequisites for Docker
echo "Installing prerequisites for Docker..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common > /dev/null

# Install Git
echo "Installing Git..."
sudo apt install -y git > /dev/null

echo "Git version: $(git --version)"

# Add Docker's official GPG key and repository
echo "Adding Docker GPG key and repository..."
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y > /dev/null

# Install Docker
echo "Installing Docker..."
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y > /dev/null

echo "Docker version: $(docker --version)"

# Add current user to the Docker group
echo "Adding current user to Docker group..."
sudo usermod -aG docker $USER

# Enable and start Docker service
echo "Enabling and starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

# Clone the GitHub repository
echo "Cloning repository..."
REPO_URL="https://github.com/HellowLab/HellowLabBackend_Django.git"
git clone $REPO_URL

echo "Setup complete! Please log out and back in for Docker permissions to take effect."
