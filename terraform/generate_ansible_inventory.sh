#!/bin/bash

mkdir -p ../inventory

cat > ../inventory/inventory.ini <<EOF
[webserver]
skillbox_vm_service ansible_host=$(terraform output -raw external_ip_address_skillbox_vm_service)

[gitlabrunner]
skillbox_vm_gitlab_runner ansible_host=$(terraform output -raw external_ip_address_skillbox_vm_gitlab_runner)

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/skillbox_rsa
EOF

echo "Inventory file generated at ../inventory/inventory.ini"
