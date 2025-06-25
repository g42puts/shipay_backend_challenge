# Documentação das Rotas

⬅ [Voltar](/README.md)

## Auth

| Método | Rota                | Descrição                     |
| ------ | ------------------- | ----------------------------- |
| POST   | /auth/login         | Login e obtenção de token JWT |
| POST   | /auth/refresh_token | Gera novo token JWT (refresh) |
| POST   | /auth/logout        | Logout e blacklist do token   |

## User

| Método | Rota                                    | Descrição                 |
| ------ | --------------------------------------- | ------------------------- |
| POST   | /user                                   | Cria novo usuário         |
| GET    | /user                                   | Lista usuários            |
| GET    | /user/{user_id}                         | Busca usuário por ID      |
| PUT    | /user/{user_id}                         | Atualiza usuário          |
| DELETE | /user/{user_id}                         | Deleta usuário            |
| POST   | /user/claims/{user_id}/claim/{claim_id} | Adiciona claim ao usuário |
| DELETE | /user/claims/{user_id}/claim/{claim_id} | Remove claim do usuário   |

## Role

| Método | Rota            | Descrição         |
| ------ | --------------- | ----------------- |
| POST   | /role           | Cria novo role    |
| GET    | /role           | Lista roles       |
| GET    | /role/{role_id} | Busca role por ID |
| PUT    | /role/{role_id} | Atualiza role     |
| DELETE | /role/{role_id} | Deleta role       |

## Claim

| Método | Rota              | Descrição          |
| ------ | ----------------- | ------------------ |
| POST   | /claim            | Cria novo claim    |
| GET    | /claim            | Lista claims       |
| GET    | /claim/{claim_id} | Busca claim por ID |
| DELETE | /claim/{claim_id} | Deleta claim       |

---

Todas as rotas estão sob o prefixo `/api/v1`.
