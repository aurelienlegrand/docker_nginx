#! /bin/bash

# Change the keyboard layout
sudo dpkg-reconfigure keyboard-configuration

# SSH configuration
sudo apt-get update
sudo apt-get install openssh-server
sudo ufw allow 22
