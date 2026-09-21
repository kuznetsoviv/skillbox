# Запуск web-приложения skillbox 

## Используемые пакеты

- ansible

## Алгоритм

- Скопировать файлы в корень проекта с сервисом (проверить ansible/inventory.ini)
- Добавить переменные в gitlab:
    - DOCKER_USERNAME
    - DOCKER_PERSONAL_ACCESS_TOKEN
    - TEST_SSH_PRIVATE_KEY
    - PROD_SSH_PRIVATE_KEY
