cat > ../inventory/inventory.ini <<EOF
[webservers]
skillbox_vm_1 ansible_host=$(terraform output -raw external_ip_address_skillbox_vm_1)

[webservers:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/skillbox_rsa
EOF
