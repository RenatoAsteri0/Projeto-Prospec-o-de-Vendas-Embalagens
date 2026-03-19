# 🚀 Data Pipeline de Prospecção Industrial com Airflow

## 📌 Visão Geral

Pipeline de dados desenvolvido para automatizar a coleta, processamento e armazenamento de leads industriais para um cliente especifico que é representante de vendas do ramo de embalagens plásticas.

O projeto utiliza **Apache Airflow como orquestrador**, **Pandas para transformação de dados** e **PostgreSQL para persistência**, simulando um fluxo real de engenharia de dados.

---

## 🏗️ Arquitetura do Pipeline

O pipeline segue o padrão clássico de engenharia de dados:

**Extract → Transform → Load (ETL)**

* **Orquestração**: Apache Airflow (DAG)
* **Processamento**: Pandas
* **Armazenamento**: PostgreSQL

---

## ⚙️ Orquestração com Airflow

A pipeline é gerenciada por uma DAG (`leads_pipeline.py`) que organiza e executa as etapas de forma automatizada e rastreável:

* Controle de execução
* Monitoramento de status (RUNNING, SUCCEEDED)
* Reexecução em caso de falha
* Separação clara de tarefas

Essa abordagem simula pipelines produtivos utilizados em ambientes corporativos.

---

## 🔄 Etapas do Pipeline

### 1. Extract

Coleta de dados de empresas via API (Google Maps Scraper), com geração dinâmica de buscas por cidade e segmento industrial.

### 2. Transform (Pandas)

Tratamento e padronização dos dados:

* Normalização de colunas (`nome`, `endereco`, `telefone`, `notas`)
* Garantia de schema consistente
* Remoção de duplicidades
* Estruturação em DataFrame

### 3. Load (SQL / PostgreSQL)

Persistência dos dados no banco:

* Inserção estruturada via `psycopg2`
* Tabela relacional (`industrial_companies`)
* Preparação para consumo analítico

---

## 🧱 Stack Tecnológica

* **Apache Airflow** → Orquestração de pipeline
* **Python (Pandas)** → Transformação de dados
* **PostgreSQL** → Armazenamento relacional
* **SQL** → Modelagem e inserção de dados
* **Docker** → Ambiente isolado e reproduzível

---

## 📂 Estrutura do Projeto

```id="projstruct1"
.
├── dags/
│   └── leads_pipeline.py        # Orquestração (Airflow)
├── src/
│   ├── extract_data_google_scrapy.py
│   ├── tranform_data_pandas.py # Transformações com Pandas
│   ├── load_postgres.py        # Carga em banco via SQL
│   └── export_results.py
├── sql/
│   └── create_tables.sql       # Estrutura do banco
├── docker-compose.yaml         # Infraestrutura
```

---

## 🗄️ Modelagem de Dados

Tabela principal:

**industrial_companies**

* nome
* endereco
* telefone
* notas

Estrutura simples, porém adequada para ingestão e consultas inicais.

---

## 🚀 Execução do Projeto

```bash id="run1"
# subir ambiente com Airflow + Postgres
docker-compose up -d

# acessar Airflow
http://localhost:8080

# executar DAG
leads_pipeline
```

---

## 📊 Resultados

* Pipeline automatizado e reexecutável
* Dados estruturados em banco relacional
* Entrega consistente dos resultados para o cliente

---

## 💡 Pontos de Engenharia

* Separação clara entre etapas (ETL)
* Uso de Airflow para controle e observabilidade
* Transformação estruturada com Pandas
* Persistência via SQL em banco relacional
* Pipeline desacoplado e escalável


---

## 👨‍💻 Autor

Renato Asterio
