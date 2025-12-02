# Sistema de Gestão de Transplantes e Logística Hospitalar

Este projeto consiste na implementação de um Sistema de Banco de Dados para o controle de fila de transplantes de órgãos e logística hospitalar. O sistema integra um banco de dados **Oracle** com uma aplicação cliente desenvolvida em **Python**.

## 🚀 Instalação e Configuração

### 1. Configuração do Banco de Dados

Antes de iniciar a aplicação, é necessário criar a estrutura do banco de dados e popular os dados iniciais (incluindo as regras de segurança/RBAC).

1.  Abra seu cliente SQL conectado ao seu usuário Oracle.
2.  Execute os scripts na seguinte ordem estrita (para evitar erros de dependência):
    * **`esquema.sql`**: Criação das tabelas, constraints e triggers.
    * **`dados.sql`**: População dos dados de teste, inserção de usuários, permissões e regras de acesso.

### 2. Configuração da Aplicação Python

1.  Clone ou extraia os arquivos do projeto.
2.  Instale a biblioteca de conexão oficial da Oracle:
    ```bash
    pip install oracledb
    ```
3.  **Configuração de Conexão:** Abra o arquivo `app/sistema.py` e localize a função `conectar()`. Atualize as credenciais conforme o seu ambiente:
    ```python
    user = "SEU_USUARIO"
    pwd = "SUA_SENHA"
    dsn = "orclgrad1.icmc.usp.br/pdb_elaine.icmc.usp.br" # Ou o endereço do seu servidor
    ```

## ▶️ Como Rodar

No terminal, navegue até a pasta onde está o arquivo Python e execute:

```bash
python sistema.py
