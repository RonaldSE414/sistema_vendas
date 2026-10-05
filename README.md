# 🛒 Sistema de Vendas – View, Function e Procedure

## 📌 Identificação

- **Aluno:** Ronald Machado
- **Disciplina:** Projeto de Banco de Dados
- **Professor:** Anderson Soares

## 📖 Sobre o projeto

Aplicação de terminal em Python para gerenciar clientes, produtos e vendas de uma loja. O projeto evolui um CRUD simples para uma aplicação que delega ao banco de dados parte do processamento, usando **View**, **Function** e **Procedure** em PostgreSQL.

**Problema que resolve:** centraliza no banco as regras de negócio (baixa de estoque, cálculo de total e relatório consolidado), garantindo consistência e evitando duplicar lógica na aplicação.

## 🛠️ Tecnologias utilizadas

- Python 3
- psycopg2 (conexão com PostgreSQL)
- Rich (interface de terminal)
- python-dotenv (configuração via `.env`)
- PostgreSQL + pgAdmin 4
- Git / GitHub
- VS Code

## 🗄️ Banco de dados

**SGBD:** PostgreSQL

### Principais tabelas

| Tabela | Descrição |
|---|---|
| `clientes` | Dados dos clientes |
| `produtos` | Produtos, preço e estoque |
| `vendas` | Cabeçalho da venda (cliente, data, desconto) |
| `itens_venda` | Itens vendidos (produto, quantidade, preço) |

### View – `vw_relatorio_vendas`
- **Por que existe:** consolidar vendas, clientes e itens em uma consulta pronta para relatório.
- **Como funciona:** faz JOIN entre `vendas`, `clientes` e `itens_venda`, agrupando por venda.
- **Onde é usada:** menu **6 – Relatório de vendas**.

### Function – `fn_calcular_total_venda(p_venda_id)`
- **Por que existe:** padronizar o cálculo do valor final de uma venda.
- **Como funciona:** soma `quantidade × preço` dos itens e aplica o desconto da venda.
- **Onde é usada:** menu **7 – Total de uma venda**.

### Procedure – `sp_registrar_venda(...)`
- **Por que existe:** registrar uma venda como uma única operação atômica.
- **Como funciona:** valida cliente e produto, verifica estoque, insere a venda e o item, e baixa o estoque. Se algo falhar, nada é gravado.
- **Onde é usada:** menu **5 – Registrar venda**.

## 📁 Estrutura do repositório

```
sistema_vendas/
├── src/
│   └── main.py         # aplicação (arquivo único)
├── database/
│   ├── tables/         # criação das tabelas
│   ├── inserts/        # dados de teste
│   ├── views/          # View
│   ├── functions/      # Function
│   └── procedures/     # Procedure
├── docs/
├── .env.example        # modelo de configuração
├── requirements.txt
└── README.md
```

## ▶️ Como executar

**Pré-requisitos:** Python 3.10+, PostgreSQL e pgAdmin 4 instalados.

1. **Clone o repositório**
```bash
   git clone https://github.com/SEU_USUARIO/projeto-vendas.git
   cd projeto-vendas
```

2. **Crie o banco no pgAdmin 4:** botão direito em *Databases → Create → Database* e nomeie como `loja_db`.

3. **Execute os scripts no pgAdmin** (*Tools → Query Tool* com `loja_db` selecionado), **nesta ordem**:
   1. `database/tables/01_tables.sql`
   2. `database/inserts/02_inserts.sql`
   3. `database/views/03_view_relatorio_vendas.sql`
   4. `database/functions/04_fn_calcular_total_venda.sql`
   5. `database/procedures/05_sp_registrar_venda.sql`

4. **Crie o ambiente virtual e instale as dependências**
```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Linux/Mac
   pip install -r requirements.txt
```

5. **Configure a conexão:** copie `.env.example` para `.env` e preencha com seus dados (principalmente `DB_PASSWORD`).

6. **Execute a aplicação**
```bash
   python src/main.py
```
##  Interface
-
-
-
-

## 🎥 Vídeo explicativo

[Link do vídeo aqui]
