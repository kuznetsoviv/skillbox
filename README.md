# Подготовка инфраструктуры для запуска web-приложения skillbox 

## Используемые пакеты

- ansible
- terrafrom

## Подготовка terrafrom

```bash
export YC_TOKEN=$(yc config get token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
```

## Алгоритм

- terraform terraform/main.tf init
- terraform terraform/main.tf apply
- cd terraform && ./generate_ansible_inventory.sh
- ansible-playbook -i inventory/inventory.ini ansible/install_docker.yml
