#!/bin/bash

mkdir -p ./inventory

cat > ./inventory/inventory.ini <<EOF
[test_webserver]
test_webserver_1 ansible_host=$(terraform -chdir=./terraform output -raw external_ip_address_skillbox_service_test)

[prod_webserver]
prod_webserver_1 ansible_host=$(terraform -chdir=./terraform output -raw external_ip_address_skillbox_service_prod)

[gitlabrunner]
gitlabrunner_1 ansible_host=$(terraform -chdir=./terraform output -raw external_ip_address_skillbox_gitlab_runner)

[monitoring]
monitoring_1 ansible_host=$(terraform -chdir=./terraform output -raw external_ip_address_skillbox_monitoring)

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[test_webserver:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/test_skillbox_rsa

[prod_webserver:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/prod_skillbox_rsa

[gitlabrunner:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/skillbox_rsa

[monitoring:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/skillbox_rsa
EOF

echo "Inventory file generated at ./inventory/inventory.ini"
