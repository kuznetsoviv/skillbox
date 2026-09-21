## Создание виртуальной машины в yc

1. установить [CLI для yc](https://yandex.cloud/ru/docs/cli/quickstart)
2. сгенерировать ssh ключ[^ssh-keygen]
3. получить список доступных образов виртуальных машин: `yc compute image list --folder-iwd standard-images`  
4. получить список зон[^zone]: `yc compute zone list`
5. получить список виртуальных подсетей: `yc vpc subnet list`
6. создать экземпляр виртуальной машины: [`yc create compute instance`](https://yandex.cloud/ru/docs/compute/cli-ref/instance/create)
7. пример команды для создания виртуальной машины:
   ```bash
   yc compute instance create \
      --name pki-instance \
      --zone ru-central1-a  \
      --cores 2 \
      --memory 4 \
      --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-24-04-lts,size=20 \
      --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \
      --ssh-key ~/.ssh/id_rsa.pub 
   ```
8. получение ip созданной виртуальной машины `yc compute instance list`, поле `EXTERNAL IP`
9. подключение к виртуальной машине `ssh yc-user@<EXTERNAL IP>`

## Настройки безопасности, которые можно применить к созданной виртуальной машине

1. запретить все входящие соединения, кроме соединений по tcp портам 22,80,443, скритп [./secure_firewall.sh](../scripts/secure_firewall.sh)[^secure-firewall-link]
2. возможно заменить порт для ssh соединения, а также запретить использование паролей для подключения к виртуальной машине
3. использовать rkhunter и проанализировать результат выполнения

## Результаты выполнения

[результаты выполнения](../results/vm-creation-results.md)

[^ssh-keygen]: для этого можно использовать, например, утилиту: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
[^zone]: зона - физическое место расположения сервера
[^secure-firewall-link]: команда для получения скрипта: `curl -O https://raw.githubusercontent.com/kuznetsoviv/system-administration-final-work/refs/heads/main/scripts/secure_firewall.sh`