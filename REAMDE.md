# Open Data AI Analytics

## Мета проєкту

Метою даного проєкту є дослідження демографічних змін в Україні на основі відкритих державних даних, а також практичне застосування інструментів аналізу даних, моделювання та системи контролю версій Git.

У межах лабораторної роботи реалізується модульна структура проєкту, що включає завантаження даних, перевірку їх якості, дослідження та візуалізацію результатів.

---

## Джерело даних

Використано набір відкритих даних з порталу відкритих даних України:

Приріст (скорочення) чисельності населення по регіонах: [посилання на датасет](https://data.gov.ua/dataset/a88b8fad-5119-4edc-a6aa-9b717042e119/resource/27e4d979-100c-410d-ac44-dd088a55c109)

---

## Питання та гіпотези дослідження

1. Які 5 регіонів України мають найбільше скорочення чисельності населення за весь період та які регіони демонструють найгіршу демографічну динаміку у 2021–2022 роках?

2. Що має більший вплив на зміну чисельності населення: природний приріст (народжуваність/смертність) чи міграційні процеси?

3. Чи спостерігається суттєва зміна динаміки демографічних показників після 2022 року?

---

## Структура проєкту

```text

open-data-ai-analytics/

├── data/

├── data_load/

├── data_quality_analysis/

├── data_research/

├── visualization/

├── web/

├── reports/

├── compose.yaml

├── README.md

└── infra/

    └── terraform/

        ├── main.tf

        ├── variables.tf

        ├── outputs.tf

        └── cloud-init.yaml

```

Основні модулі проєкту:

- `data_load` — завантаження та підготовка даних;

- `data_quality_analysis` — перевірка якості даних;

- `data_research` — базовий аналіз і дослідження датасету;

- `visualization` — побудова графіків;

- `web` — веб-інтерфейс для перегляду результатів;

- `infra/terraform` — Terraform-конфігурація для розгортання проєкту в Microsoft Azure.

---

## Локальний запуск через Docker Compose

Для локального запуску проєкту потрібно виконати команду:

```bash

docker compose up -d --build

```

Після запуску веб-інтерфейс буде доступний за адресою:

```text

http://localhost:8000

```

Перевірити стан контейнерів можна командою:

```bash

docker ps -a

```

Зупинити проєкт:

```bash

docker compose down

```

---

## Розгортання в Microsoft Azure через Terraform

У проєкті передбачено можливість розгортання Docker-застосунку в Microsoft Azure за допомогою Terraform, Azure Cloud Shell та cloud-init.

Terraform-конфігурація розміщена в директорії:

```text

infra/terraform/

```

Основні файли:

```text

main.tf          # опис Azure-ресурсів

variables.tf     # змінні Terraform

outputs.tf       # вихідні значення

cloud-init.yaml  # автоматичне налаштування Linux VM

```

---

## Запуск у Azure Cloud Shell

1. Відкрити Azure Portal.

2. Запустити Azure Cloud Shell.

3. Обрати режим Bash або PowerShell.

4. Клонувати репозиторій:

```bash

git clone https://github.com/VolodymyrVulchyn/open-data-ai-analytics.git

```

5. Перейти до директорії Terraform:

```bash

cd open-data-ai-analytics/infra/terraform

```

6. Ініціалізувати Terraform:

```bash

terraform init

```

7. Відформатувати та перевірити конфігурацію:

```bash

terraform fmt

terraform validate

```

8. Переглянути план створення ресурсів:

```bash

terraform plan

```

9. Створити інфраструктуру:

```bash

terraform apply

```

Після запиту підтвердження потрібно ввести:

```text

yes

```

---

## Створювані ресурси Azure

Terraform-конфігурація створює такі ресурси Microsoft Azure:

- Resource Group;

- Virtual Network;

- Subnet;

- Public IP;

- Network Security Group;

- Network Interface;

- Linux Virtual Machine.

Network Security Group використовується для відкриття необхідних портів:

- `22` — SSH-підключення до Linux VM;

- `8000` — доступ до веб-інтерфейсу Docker-проєкту.

---

## Автоматичне налаштування VM через cloud-init

Під час створення Linux VM через Terraform передається файл `cloud-init.yaml`.

Він виконує початкове налаштування віртуальної машини:

- оновлює пакети;

- встановлює Docker;

- встановлює Docker Compose;

- клонує GitHub-репозиторій;

- запускає Docker-проєкт через Docker Compose.

У разі якщо Docker Compose plugin недоступний, можна встановити класичний пакет:

```bash

sudo apt update

sudo apt install -y docker-compose

```

Після цього проєкт можна запустити вручну:

```bash

cd /open-data-ai-analytics

sudo docker-compose up -d

```

---

## Перевірка результату

Після створення інфраструктури потрібно отримати public IP віртуальної машини.

Через Terraform:

```bash

terraform output

```

Або через Azure CLI:

```bash

az vm list-ip-addresses --resource-group lab4-rg --name lab4-vm --output table

```

Для підключення до VM:

```bash

ssh azureuser@PUBLIC_IP

```

Після входу на VM перейти в директорію проєкту:

```bash

cd /open-data-ai-analytics

```

Перевірити стан контейнерів:

```bash

sudo docker ps -a

```

Очікуваний результат:

```text

open_data_web              Up

open_data_db               Up (healthy)

open_data_load             Exited (0)

open_data_quality          Exited (0)

open_data_research         Exited (0)

open_data_visualization    Exited (0)

```

Статус `Exited (0)` для модулів обробки означає, що контейнер успішно виконав свою задачу і завершив роботу без помилки.

Перевірити, що веб-сервіс слухає порт `8000`:

```bash

sudo ss -tulpn | grep 8000

```

Перевірити HTTP-відповідь з VM:

```bash

curl http://localhost:8000

```

Веб-інтерфейс відкривається в браузері за адресою:

```text

http://PUBLIC_IP:8000

```

---

## Перевірка Network Security Group

Якщо веб-інтерфейс не відкривається через public IP, потрібно перевірити правила Network Security Group:

```bash

az network nsg rule list --resource-group lab4-rg --nsg-name lab4-nsg --output table

```

У списку має бути правило для порту `8000`.

Якщо його немає, можна додати вручну:

```bash

az network nsg rule create \\

  --resource-group lab4-rg \\

  --nsg-name lab4-nsg \\

  --name Allow-Web-8000 \\

  --priority 1004 \\

  --direction Inbound \\

  --access Allow \\

  --protocol Tcp \\

  --source-address-prefixes "*" \\

  --source-port-ranges "*" \\

  --destination-address-prefixes "*" \\

  --destination-port-ranges 8000

```

Після цього веб-інтерфейс має бути доступний за адресою:

```text

http://PUBLIC_IP:8000

```

---

## Видалення ресурсів

Після демонстрації лабораторної роботи потрібно видалити створену інфраструктуру, щоб не витрачати Azure-кредит:

```bash

terraform destroy

```

Після запиту підтвердження потрібно ввести:

```text

yes

```

---

## Короткий набір команд для демонстрації

```bash

ssh azureuser@PUBLIC_IP

cd /open-data-ai-analytics

sudo docker ps -a

sudo ss -tulpn | grep 8000

curl http://localhost:8000

```

Після цього у браузері потрібно відкрити:

```text

http://PUBLIC_IP:8000

```
