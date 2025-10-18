## 🧩 **README — Pokédex (Back-End - Django)**

### 📘 Descrição

Este repositório contém o **Back-End da Pokédex**, desenvolvido em **Python com Django**.
Ele centraliza a integração com a **PokeAPI**, fornece endpoints para o **Front-End Angular** e implementa **autenticação JWT**, além de funcionalidades administrativas.

---

### 🚀 Funcionalidades

- ✅ **Integração direta com a PokeAPI** (consulta e cache local de Pokémons).
- ✅ **Banco de dados SQLite** com **ORM do Django**.
- ✅ **Autenticação com Token JWT (access e refresh)**.
- ✅ **Painel de administração** para gestão de usuários.
- ✅ **Rota para reset de senha via painel administrativo.**
- ✅ **Containerização completa via Docker**.
- ✅ **Centralização de todas as requisições à PokeAPI no Back-End** — o Front-End consome apenas esta API interna.

---

### 🧱 Tecnologias Utilizadas

- **Python 3.12+**
- **Django 5+**
- **Django REST Framework**
- **djangorestframework-simplejwt**
- **SQLite (padrão do Django)**
- **Requests (para integração com PokeAPI)**
- **Docker / Docker Compose**

---

### ⚙️ Estrutura do Projeto

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

Toda comunicação com a PokeAPI é feita pelo servidor Django.
O Front-End consome endpoints internos.

🔗 **Documentação da PokeAPI:**
[https://pokeapi.co/docs/v2](https://pokeapi.co/docs/v2)

---

### 🔐 Autenticação JWT

Utiliza `djangorestframework-simplejwt` com os seguintes endpoints:

```
POST /api/auth/register/     → Registro de novo usuário
POST /api/auth/login/        → Login e geração de tokens
POST /api/auth/token/refresh/      → Atualização de token
```

- Tokens armazenados no Front-End via **localStorage**.
- Todas as rotas protegidas requerem **Authorization: Bearer <token>**.

---

### 🐳 Docker

O Back-End já vem containerizado. Exemplo:

```bash
# Build e inicializa o container
docker-compose up --build

# Acessar o container
docker exec -it django_api bash
```

---

### 📄 Admin / Gestão de Usuários

- `python manage.py createsuperuser` para criar usuário admin.
- Painel administrativo disponível em `/admin/` para:

---
