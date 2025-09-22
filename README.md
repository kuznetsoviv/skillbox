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

- генерация ssh ключей: 
  - для окружения тестирования: `ssh-keygen -t rsa -b 4096 -C "<your_email>" -f ~/.ssh/test_skillbox_rsa`
  - для окружения продакшена: `ssh-keygen -t rsa -b 4096 -C "<your_email>" -f ~/.ssh/prod_skillbox_rsa`
  - для ci/cd и мониторинга: `ssh-keygen -t rsa -b 4096 -C "<your_email>" -f ~/.ssh/prod_skillbox_rsa`

- инициализация terraform: `terraform -chdir=./terraform init`
- создание инфраструктуры: `terraform -chdir=./terraform apply`
- создание ansible inventory файла: `./terraform/generate_inventory.sh`
- настройка развернутых серверов: 
    ```
      ansible-playbook -i inventory/inventory.ini ./ansible/site.yml \
      -e test_application_ip=$(terraform -chdir=./terraform output -raw external_ip_address_skillbox_service_test) \
      -e prod_application_ip=$(terraform -chdir=./terraform output -raw external_ip_address_skillbox_service_prod)
    ```

## Обоснование выбора системы мониторинга
[LADR](https://gitlab.skillbox.ru/igor_kuznetsov_6/infra/-/blob/feature/task-3/ansible/monitoring/README.md)