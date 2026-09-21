#!/bin/bash

# Script to configure iptables firewall rules

# Update the package list
sudo apt-get update
# Install packages
sudo apt-get install iptables-persistent > /dev/null

if [ $? -ne 0 ]; then
    echo "Failed to install iptables-persistent, rules not applied"
    exit 1
fi

# Flush existing rules
sudo iptables -F

# Default policies: drop inputs
sudo iptables -P INPUT DROP

# Allow loopback traffic (for internal system communications)
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (port 22)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP (port 80)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow HTTPS (port 443)
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow DNS (port 53) for `apt-get update` and other name resolution
sudo iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
sudo iptables -A INPUT -p udp --sport 53 -j ACCEPT

# Save the rules
sudo netfilter-persistent save

## Enable at statup
sudo systemctl enable netfilter-persistent

# Print active rules for verification
echo "Current iptables rules:"
sudo iptables -L -v