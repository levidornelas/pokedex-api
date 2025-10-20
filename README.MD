## 🧩 **README — Pokédex (Back-End - Django)**

### 📘 Descrição

Este repositório contém o **Back-End da Pokédex**, desenvolvido em **Python com Django**.
Ele centraliza a integração com a **PokeAPI**, fornece endpoints para o **Front-End Angular** e implementa **autenticação JWT**

---

### 🚀 Funcionalidades

- ✅ **Integração direta com a PokeAPI**.
- ✅ **Banco de dados SQLite** com **ORM do Django**.
- ✅ **Autenticação com Token JWT (access e refresh)**.
- ✅ **Painel de administração** para gestão de usuários.
- ✅ **Rota para reset de senha via painel administrativo.**
- ✅ **Containerização completa via Docker.**
- ✅ **Centralização de todas as requisições à PokeAPI no Back-End** — o Front-End consome apenas esta API interna.

---

### 🧱 Estrutura do Projeto

```
back-end/
├── apps/
│   ├── api/            # Endpoints principais da API
│   ├── pokemon/        # Lógica e models de Pokémons
│   └── usuario/        # Models e views de usuários
├── conf/               # Configurações do Django (settings, urls)
├── db.sqlite3          # Banco de dados SQLite
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

### 🧩 Integração com a PokeAPI

Toda comunicação com a **PokeAPI** é feita **exclusivamente pelo servidor Django**.
O **Front-End Angular** consome apenas os **endpoints internos** deste back-end.

🔗 **Documentação oficial da PokeAPI:**
[https://pokeapi.co/docs/v2](https://pokeapi.co/docs/v2)

---

### 🔐 Autenticação JWT

A autenticação utiliza o pacote **`djangorestframework-simplejwt`**

📦 **Detalhes:**

- Tokens são armazenados no **localStorage** no Front-End.
- Todas as rotas protegidas requerem o cabeçalho:
  `Authorization: Bearer <token>`.

---

### Tutorial — Executando a Aplicação com Docker

Siga o passo a passo abaixo para rodar o projeto localmente usando Docker:

#### Clonar o repositório

```bash
git clone https://github.com/seuusuario/pokedex-backend.git
cd pokedex-backend
```

#### Criar e configurar o container

```bash
docker-compose up --build

#### Acessar a aplicação

- 🌍 API: [http://localhost:8000/api/](http://localhost:8000/api/)
- ⚙️ Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- 📘 Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
```
