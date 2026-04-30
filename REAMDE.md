# Open Data AI Analytics

## Мета проєкту

Метою даного проєкту є дослідження демографічних змін в Україні на основі відкритих державних даних, а також практичне застосування інструментів аналізу даних, моделювання та системи контролю версій Git.

У межах лабораторної роботи реалізується модульна структура проєкту, що включає завантаження даних, перевірку їх якості, дослідження, візуалізацію результатів, хмарне розгортання, моніторинг та GitOps-розгортання у Kubernetes.

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
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── docker-compose.monitoring.yml
├── gitops/
│   ├── app/
│   │   ├── namespace.yaml
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── argocd/
│       └── application.yaml
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
- `monitoring` — конфігурація моніторингу Prometheus та Grafana;
- `gitops` — Kubernetes YAML-файли та Argo CD Application для GitOps-розгортання;
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
3. Клонувати репозиторій:

```bash
git clone https://github.com/VolodymyrVulchyn/open-data-ai-analytics.git
```

4. Перейти до директорії Terraform:

```bash
cd open-data-ai-analytics/infra/terraform
```

5. Ініціалізувати Terraform:

```bash
terraform init
```

6. Відформатувати та перевірити конфігурацію:

```bash
terraform fmt
terraform validate
```

7. Переглянути план створення ресурсів:

```bash
terraform plan
```

8. Створити інфраструктуру:

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
- `8000` — доступ до веб-інтерфейсу Docker-проєкту;
- `30080` — доступ до застосунку, розгорнутого в Kubernetes через NodePort;
- `30443` — доступ до веб-інтерфейсу Argo CD;
- `9090` — доступ до Prometheus;
- `3000` — доступ до Grafana.

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
az vm list-ip-addresses --resource-group rg-open-data-lab4 --name vm-open-data-lab4 --output table
```

Для підключення до VM:

```bash
ssh -i lab4_vm_key.pem azureuser@PUBLIC_IP
```

Після входу на VM перейти в директорію проєкту:

```bash
cd /open-data-ai-analytics
```

Перевірити стан контейнерів:

```bash
sudo docker ps -a
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

Якщо веб-інтерфейс або інші сервіси не відкриваються через public IP, потрібно перевірити правила Network Security Group:

```bash
az network nsg rule list --resource-group rg-open-data-lab4 --nsg-name nsg-open-data-lab4 --output table
```

Приклад додавання правила для порту `8000`:

```bash
az network nsg rule create \
  --resource-group rg-open-data-lab4 \
  --nsg-name nsg-open-data-lab4 \
  --name Allow-Web-8000 \
  --priority 1004 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes "*" \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 8000
```

---

## Моніторинг за допомогою Prometheus та Grafana

У межах лабораторної роботи до проєкту було додано систему моніторингу контейнеризованого застосунку в Microsoft Azure. Для цього використано Prometheus, Grafana, Node Exporter та cAdvisor.

Моніторингова частина проєкту розміщена в директорії:

```text
monitoring/
```

Структура директорії:

```text
monitoring/
├── prometheus/
│   └── prometheus.yml
└── docker-compose.monitoring.yml
```

Основні компоненти моніторингу:

- `Prometheus` — збір і зберігання метрик;
- `Grafana` — візуалізація метрик і побудова дашбордів;
- `Node Exporter` — збір системних метрик Linux VM;
- `cAdvisor` — збір метрик Docker-контейнерів.

---

## Конфігурація Prometheus

Файл конфігурації Prometheus знаходиться за шляхом:

```text
monitoring/prometheus/prometheus.yml
```

У ньому налаштовано збір метрик із таких джерел:

- `prometheus` — метрики самого Prometheus;
- `node-exporter` — метрики Linux VM;
- `cadvisor` — метрики Docker-контейнерів.

Prometheus опитує налаштовані сервіси кожні 15 секунд.

---

## Запуск сервісів моніторингу

Після запуску основного Docker-проєкту потрібно перейти в директорію моніторингу:

```bash
cd /open-data-ai-analytics/monitoring
```

Запуск сервісів моніторингу:

```bash
sudo docker-compose -f docker-compose.monitoring.yml up -d
```

Перевірка стану контейнерів:

```bash
sudo docker ps -a
```

Очікувані контейнери моніторингу:

```text
monitoring_prometheus
monitoring_grafana
monitoring_node_exporter
monitoring_cadvisor
```

---

## Відкриті порти для моніторингу

Для роботи моніторингу в Azure Network Security Group мають бути відкриті такі порти:

- `9090` — Prometheus;
- `3000` — Grafana;
- `8000` — веб-інтерфейс основного проєкту;
- `22` — SSH-підключення до VM.

Якщо правила для Prometheus і Grafana відсутні, їх можна додати командами:

```bash
az network nsg rule create \
  --resource-group rg-open-data-lab4 \
  --nsg-name nsg-open-data-lab4 \
  --name Allow-Prometheus-9090 \
  --priority 1012 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes "*" \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 9090
```

```bash
az network nsg rule create \
  --resource-group rg-open-data-lab4 \
  --nsg-name nsg-open-data-lab4 \
  --name Allow-Grafana-3000 \
  --priority 1013 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes "*" \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 3000
```

---

## Доступ до Prometheus

Prometheus відкривається у браузері за адресою:

```text
http://PUBLIC_IP:9090
```

Сторінка targets доступна за адресою:

```text
http://PUBLIC_IP:9090/targets
```

На сторінці targets мають бути доступні такі job-и:

```text
prometheus
node-exporter
cadvisor
```

---

## Доступ до Grafana

Grafana відкривається у браузері за адресою:

```text
http://PUBLIC_IP:3000
```

Дані для входу:

```text
login: admin
password: admin
```

Після входу в Grafana потрібно додати Prometheus як Data Source.

URL для Prometheus всередині Docker-мережі:

```text
http://prometheus:9090
```

Після підключення потрібно натиснути:

```text
Save & test
```

---

## Grafana dashboard

Для візуалізації метрик було використано dashboard Node Exporter Full.

Його можна імпортувати в Grafana через:

```text
Dashboards → New → Import
```

ID dashboard:

```text
1860
```

На dashboard відображаються такі метрики:

- завантаження CPU;
- використання оперативної пам’яті;
- системне навантаження;
- використання дискового простору;
- мережевий трафік;
- час роботи системи.

---

## Перевірка метрик контейнерів

Метрики Docker-контейнерів збираються через cAdvisor. Їх можна перевірити у Prometheus за допомогою таких PromQL-запитів:

```promql
container_memory_usage_bytes
```

```promql
rate(container_cpu_usage_seconds_total[5m])
```

```promql
count(container_last_seen)
```

---

## GitOps-розгортання за допомогою k3s та Argo CD

У межах лабораторної роботи було реалізовано GitOps-підхід для автоматизованого розгортання застосунку в Kubernetes-середовище. Для цього на Azure Linux VM було встановлено k3s, а як GitOps-інструмент використано Argo CD.

GitOps означає, що бажаний стан застосунку описується у GitHub-репозиторії, а Argo CD автоматично синхронізує Kubernetes-кластер із цим станом. Усі зміни виконуються через commit і push у Git, після чого Argo CD застосовує їх до кластера.

---

## Структура GitOps-директорії

GitOps-конфігурація розміщена в директорії:

```text
gitops/
```

Структура:

```text
gitops/
├── app/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── argocd/
    └── application.yaml
```

Призначення файлів:

- `gitops/app/namespace.yaml` — створює namespace `open-data-app`;
- `gitops/app/deployment.yaml` — описує Deployment застосунку `open-data-web`;
- `gitops/app/service.yaml` — створює Service типу NodePort для доступу до застосунку;
- `gitops/argocd/application.yaml` — описує Argo CD Application, який підключає GitHub-репозиторій до Kubernetes-кластера.

---

## Встановлення k3s на Azure VM

Для встановлення k3s потрібно підключитися до Azure VM:

```bash
ssh -i lab4_vm_key.pem azureuser@PUBLIC_IP
```

Після цього можна встановити k3s:

```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --write-kubeconfig-mode 644" sh -
```

Перевірка роботи Kubernetes-кластера:

```bash
sudo kubectl get nodes
```

Очікуваний результат:

```text
vm-open-data-lab4   Ready   control-plane   ...
```

---

## Встановлення Argo CD

Створити namespace для Argo CD:

```bash
sudo kubectl create namespace argocd
```

Завантажити manifest встановлення Argo CD:

```bash
curl -L https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml -o argocd-install.yaml
```

Встановити Argo CD:

```bash
sudo kubectl apply -n argocd -f argocd-install.yaml --validate=false
```

Якщо під час встановлення виникає помилка з `metadata.annotations: Too long`, manifest можна застосувати через server-side apply:

```bash
sudo kubectl apply --server-side --force-conflicts -n argocd -f argocd-install.yaml --validate=false
```

Перевірити pod-и Argo CD:

```bash
sudo kubectl get pods -n argocd
```

Усі основні pod-и мають перейти у стан `Running`.

---

## Доступ до Argo CD

Для доступу до Argo CD через браузер створюється Service типу NodePort:

```bash
cat <<EOF | sudo kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: argocd-server-nodeport
  namespace: argocd
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: argocd-server
  ports:
    - name: https
      port: 443
      targetPort: 8080
      nodePort: 30443
EOF
```

Argo CD відкривається у браузері:

```text
https://PUBLIC_IP:30443
```

Отримати початковий пароль адміністратора:

```bash
sudo kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Дані для входу:

```text
login: admin
password: пароль із команди
```

---

## Підключення GitHub-репозиторію до Argo CD

Argo CD Application описано у файлі:

```text
gitops/argocd/application.yaml
```

Застосувати його можна командою:

```bash
cd /open-data-ai-analytics
sudo kubectl apply -f gitops/argocd/application.yaml
```

Перевірити Application:

```bash
sudo kubectl get applications -n argocd
```

Очікуваний стан:

```text
open-data-web   Synced   Healthy
```

---

## Перевірка Kubernetes-ресурсів

Після синхронізації Argo CD можна перевірити створені ресурси:

```bash
sudo kubectl get all -n open-data-app
```

Або окремо:

```bash
sudo kubectl get pods -n open-data-app
sudo kubectl get deployment -n open-data-app
sudo kubectl get svc -n open-data-app
```

Очікувано має бути:

```text
pod/open-data-web-...              Running
deployment.apps/open-data-web      1/1
service/open-data-web-service      NodePort 80:30080/TCP
```

---

## Доступ до GitOps-застосунку

Застосунок, розгорнутий через Argo CD, відкривається через NodePort:

```text
http://PUBLIC_IP:30080
```

У демонстраційному варіанті використовується образ `nginx:latest`, тому при відкритті адреси відображається стандартна сторінка `Welcome to nginx!`.

---

## Демонстрація автоматичного оновлення

Для перевірки автоматичного оновлення потрібно змінити файл:

```text
gitops/app/deployment.yaml
```

Наприклад, змінити кількість реплік:

```yaml
replicas: 1
```

на:

```yaml
replicas: 2
```

Після цього виконати commit і push у GitHub.

Перевірити результат на VM:

```bash
sudo kubectl get deployment -n open-data-app
sudo kubectl get pods -n open-data-app
```

Очікуваний результат:

```text
open-data-web   2/2
```

і два pod-и застосунку `open-data-web`.

Також у веб-інтерфейсі Argo CD застосунок має залишатися у стані:

```text
Synced / Healthy
```

---

## Демонстрація rollback

Для rollback потрібно повернути попередній стан у GitHub-репозиторії. Наприклад, змінити:

```yaml
replicas: 2
```

назад на:

```yaml
replicas: 1
```

Після цього виконати commit і push.

Перевірити результат:

```bash
sudo kubectl get deployment -n open-data-app
sudo kubectl get pods -n open-data-app
```

Очікуваний результат:

```text
open-data-web   1/1
```

і один pod застосунку.

---

## Перевірка сумісності GitOps із моніторингом

Після GitOps-розгортання можна повторно запустити моніторинговий стек:

```bash
cd /open-data-ai-analytics/monitoring
sudo docker-compose -f docker-compose.monitoring.yml up -d
sudo docker ps -a
```

Після цього мають працювати контейнери:

```text
monitoring_prometheus
monitoring_grafana
monitoring_node_exporter
monitoring_cadvisor
```

Prometheus можна перевірити локально на VM:

```bash
curl http://localhost:9090
```

Grafana і Prometheus доступні через браузер:

```text
http://PUBLIC_IP:3000
http://PUBLIC_IP:9090
```

Застосунок, розгорнутий через Argo CD, залишається доступним через:

```text
http://PUBLIC_IP:30080
```

---

## Короткий набір команд для запуску GitOps

```bash
ssh -i lab4_vm_key.pem azureuser@PUBLIC_IP

curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --write-kubeconfig-mode 644" sh -

sudo kubectl get nodes

sudo kubectl create namespace argocd

curl -L https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml -o argocd-install.yaml

sudo kubectl apply -n argocd -f argocd-install.yaml --validate=false

sudo kubectl apply --server-side --force-conflicts -n argocd -f argocd-install.yaml --validate=false

sudo kubectl get pods -n argocd

cd /open-data-ai-analytics

sudo kubectl apply -f gitops/argocd/application.yaml

sudo kubectl get applications -n argocd

sudo kubectl get all -n open-data-app
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

Якщо ресурси залишаються в Azure, можна видалити всю Resource Group:

```bash
az group delete --name rg-open-data-lab4 --yes --no-wait
```
