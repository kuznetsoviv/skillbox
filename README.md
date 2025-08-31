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
- инициализация terraform: `terraform -chdir=./terraform init`
- создание инфраструктуры: `terraform -chdir=./terraform apply`
- создание ansible inventory файла: `./terraform/generate_ansible_inventory.sh`
- подготовка инфраструктуры для skillbox сервиса: `ansible-playbook -i inventory/inventory.ini ansible/app/setup-skillbox-devops-service.yml`
- запуск gitlab агента: `ansible-playbook -i inventory/inventory.ini ansible/gitlab-runner/setup-skillbox-gitlab-runner.yml`
- запуск мониторинга: `ansible-playbook -i inventory/inventory.ini ansible/monitoring/setup-monitoring.yml -e app_ip=$(cd ./terraform && terraform output -raw external_ip_address_skillbox_vm_service_dev)`

## Обоснование выбора системы мониторинга
[LADR](https://gitlab.skillbox.ru/igor_kuznetsov_6/infra/-/blob/feature/task-3/ansible/monitoring/README.md)
