# AI Task Orchestrator — Arquitetura e Documentação

## 1. Objetivo do Projeto

Este projeto é um **backend de orquestração de tarefas assíncronas**. Ele existe para receber solicitações de execução (tasks), processá-las de forma desacoplada e assíncrona, e manter o estado completo de cada execução.

O foco **não é IA em si**, mas sim a **infraestrutura que permite executar qualquer tipo de tarefa** (IA, scraping, processamento, pipelines, etc.) de forma escalável e observável.

---

## 2. Problema que o projeto resolve

Aplicações síncronas (HTTP) não devem:

* executar tarefas pesadas
* bloquear requests
* depender de processos longos

Este projeto separa claramente:

* **quem recebe pedidos** (API)
* **quem executa trabalho pesado** (workers)
* **quem guarda o estado** (banco)

---

## 3. Visão geral da arquitetura

### Componentes principais

| Componente | Tecnologia     | Responsabilidade                                       |
| ---------- | -------------- | ------------------------------------------------------ |
| API        | Django + DRF   | Receber requisições, validar dados, orquestrar tarefas |
| Banco      | PostgreSQL     | Armazenar estado, histórico e resultados               |
| Fila       | Redis          | Transportar mensagens de tarefas                       |
| Workers    | Celery         | Executar tarefas assíncronas                           |
| Infra      | Docker Compose | Padronizar ambiente local                              |

---

## 4. Fluxo de funcionamento (end-to-end)

1. Cliente faz uma requisição HTTP para criar uma tarefa
2. Django valida e salva a tarefa no PostgreSQL (status = PENDING)
3. Django envia uma mensagem para o Redis via Celery
4. Um worker Celery consome a mensagem
5. O worker executa a tarefa
6. O status e o resultado são atualizados no PostgreSQL
7. O cliente pode consultar o status e o resultado via API

---

## 5. Estrutura de diretórios

```
backend/
├── a_core/               # Configuração central do projeto
│   ├── settings.py       # Django, Celery, Redis, DB
│   ├── urls.py
│   ├── celery.py         # Inicialização do Celery
│   └── wsgi.py
│
├── tasks/                # Domínio de tarefas
│   ├── models.py         # Modelos de Task e TaskRun
│   ├── tasks.py          # Funções executadas pelo Celery
│   ├── views.py          # Endpoints HTTP
│   └── serializers.py
│
├── users/                # Usuários e autenticação (futuro)
│
├── manage.py
└── requirements.txt
```

---

## 6. Responsabilidade de cada camada

### Django (API / Orquestrador)

* Não executa tarefas pesadas
* Apenas coordena
* Dispara tarefas para a fila
* Controla autenticação e autorização

### Celery (Workers)

* Executa tarefas longas
* Pode escalar horizontalmente
* Não expõe HTTP

### Redis (Fila)

* Comunicação rápida entre API e workers
* Não é banco de dados permanente

### PostgreSQL (Estado)

* Fonte da verdade
* Guarda histórico completo

---

## 7. O que este projeto NÃO é (por enquanto)

* Não é um sistema distribuído complexo
* Não usa Kafka
* Não usa RabbitMQ
* Não tem microserviços
* Não tem frontend

Essas decisões são **intencionais** para manter o projeto enxuto e compreensível.

---

## 8. Evoluções planejadas (opcionais)

* Autenticação JWT
* Tipos diferentes de tasks
* Retry e backoff
* Monitoramento (Flower / Prometheus)
* Substituição do Redis por RabbitMQ (se necessário)
* Introdução de Kafka apenas para eventos

---

## 9. Princípios arquiteturais

* Simplicidade antes de abstração
* Estado explícito
* Infra mínima
* Escalabilidade incremental

---

## 10. Status atual

✔ Infra funcionando
✔ Docker Compose validado
✔ Django conectado ao Postgres
✔ Celery conectado ao Redis
✔ Workers ativos

Próximo passo lógico: **consolidar modelo de Task e estados**.
