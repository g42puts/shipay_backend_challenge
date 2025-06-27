# Shipay Backend Challenge

## Descrição

Esta API foi desenvolvida como projeto de teste para o desafio para o cargo de Backend Junior na empresa Shipay, sendo a linguagem e frameworks de livre escolha.

Foi utilizado o **model.sql** providenciado no repositório do teste como estrutura base do banco de dados, decidi adicionar o model BlacklistedToken para blacklistar tokens antigas, dando mais segurança para a API e ao usuário.

Foram utilizados algumas boas práticas, como **Adapter and Factory Pattern**, **Dependency Injection**, **Guards**, **Swagger** para documentação, **testes unitários, de integração e e2e**.

---

## Tecnologias Utilizadas

- Framework: FastAPI + Uvicorn
- ORM: SqlAlchemy com Alembic (migrations)
- Database: MySQL + Docker
- Database Validation: Pydantic
- Ferramentas de Teste: Pytest, freezegun, testcontainers (docker)
- Autenticação: PyJWT

---

## Requisitos

- Docker instalado
- Python 3.13
- Poetry

Caso não tenha o poetry instalado, basta instalar ele através do pip: `pip install poetry`

---

## Documentação de rotas

- [Rotas](/docs//routes.md)
- Mais detalhes sobre a rota podem ser encontrados na rota **http://localhost:8000/docs** quando a API for inicializada.

---

### Primeiros passos

- #### Faça o clone do projeto localmente utilizando

    ```bash
    git clone https://github.com/g42puts/shipay_backend_challenge.git
    ```

- #### Crie e ative o ambiente virtual

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

- #### Instale as dependências



    ```bash
    poetry install
    ```

- #### Crie uma cópia do arquivo .env.example com nome .env

- #### Suba os containers Docker

    ```bash
    poetry run task docker
    ```

- #### Inicialize as migrations do Alembic (apenas se necessário)

    ```bash
    alembic init migrations
    ```

- #### Gere e aplique as migrations no ambiente local

    ```bash
    poetry run task generate
    poetry run task migrate
    ```

- #### Execute o seed para criar os cargos "user" e "admin" e um usuário admin

    ```bash
    poetry run task seed
    ```

- #### Execute a API localmente

    ```bash
    poetry run task dev
    ```

### Como executar o projeto em ambiente local

- #### Clone o repositório

    ```bash
    git clone https://github.com/g42puts/shipay_backend_challenge.git
    ```

- #### Crie e ative o ambiente virtual

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

- #### Crie o arquivo .env ou crie uma cópia com o seguinte comando

    ```bash
    cp .env.example .env
    ```

- #### Instale as dependências

    ```bash
    poetry install
    ```

- #### Suba o Container do MySQL no D (banco de dados)

    ```bash
    poetry run task mysql_docker
    ```

- #### Gere e aplique as migrations

    ```bash
    poetry run task generate
    poetry run task migrate
    ```

- #### Execute o seed para criar os cargos e o usuário admin

    ```bash
    poetry run task seed
    ```

- #### Rode a aplicação localmente

    ```bash
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

A API estará disponível em http://localhost:8000/api/v1

---

### Como realizar o deploy em ambiente produtivo

1. Configure as variáveis de ambiente necessárias (exemplo: `DATABASE_URL`, `SECRET_KEY`, etc).
2. Certifique-se de que o banco de dados esteja acessível pelo ambiente de produção.
3. Instale as dependências de produção:

    ```bash
    poetry install --no-dev
    ```

- #### Gere e aplique as migrations no banco de produção

    ```bash
    poetry run task generate
    poetry run task migrate
    ```

- #### Execute o seed apenas se necessário (atenção para não sobrescrever dados em produção)

    ```bash
    poetry run task seed
    ```

--- 

Há a possibilidade de executar o servidor diretamente pelo terminal ou utilizando um Docker, caso queira utilizar o Docker, siga o passo 2:


1. #### Executar o servidor através do terminal com um gerenciador de processos (exemplo: Gunicorn + Uvicorn Worker)

    **Windows**:

    ```bash
    poetry run task prod_win
    ```

    **Linux**:

    ```bash
    poetry run task prod_linux
    ```

2. #### Executar o servidor utilizando o Docker

    - Crie a imagem do docker e faça o build da aplicação:
   
        ```bash
        poetry run task create_api_docker
        ```

    - Execute o servidor:

        ```bash
        poetry run task prod_docker
        ```

- ### Configure um proxy reverso (ex: Nginx) para expor a aplicação externamente, se necessário

---

Esses passos garantem que o projeto rode tanto localmente quanto em produção de forma segura e escalável.

### Opinião Pessoal

- A linguagem escolhida foi Python, mesmo sendo Javascript/Typescript a tecnologia que mais tenho familiaridade no momento do desenvolvimento desse teste, sendo essa escolha definida levando em consideração os requisitos para a vaga.
- O código está organizado para facilitar a manutenção e a escrita de testes.
- Qualquer dúvida ou sugestão, fique à vontade para entrar em contato!
