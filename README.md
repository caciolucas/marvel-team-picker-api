# marvel-team-picker-api

Para rodar o projeto, é preciso do Poetry e o Python 3.10, além de uma instância local do Postgres.

- Instale as dependências
- Crie um arquivo .env na raiz do projeto com as variáveis de ambiente (PUBLIC_API_KEY e PRIVATE_API_KEY da api da marvel)
- Crie um banco de dados no Postgres (nome sugerido: marvel)
- Execute com o uviicorn uvicorn main:app --reload

Pronto! O projeto está rodando na porta 8000.