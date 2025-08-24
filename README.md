# Подготовка инфраструктуры для запуска web-приложения skillbox 

## Используемые пакеты

- ansible
- terrafrom

## Подготовка terrafrom

```bash
export GITLAB_RUNNER_REGISTRATION_TOKEN=<GITLAB_RUNNER_REGISTRATION_TOKEN>
export YC_TOKEN=$(yc config get token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
```

## Алгоритм

- генерация ssh ключа: `ssh-keygen -t rsa -b 4096 -C "<your_email>" -f ~/.ssh/skillbox_rsa`
- инициализация terraform: `terraform terraform/main.tf init`
- создание инфраструктуры: `terraform terraform/main.tf apply`
- создание ansible inventory файла: `cd terraform && ./generate_ansible_inventory.sh`
- запуск gitlab агента: `ansible-playbook -i inventory/inventory.ini ansible/setup_skillbox_gitlab_runner.yml`
- запуск gitlab сервиса: `ansible-playbook -i inventory/inventory.ini ansible/setup_skillbox_service.yml`
