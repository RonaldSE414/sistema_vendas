# 🛒 Sistema de Vendas – View, Function e Procedure com PostgreSQL

> Trabalho Avaliativo – Projeto de Banco de Dados

---

## 📌 Identificação

| | |
|---|---|
| **Aluno** | Ronald Machado |
| **Disciplina** | Projeto de Banco de Dados |
| **Professor** | Anderson Soares |

---

## 📖 Sobre o projeto

Aplicação desktop com interface gráfica para gerenciar **clientes, produtos e vendas** de uma loja.

**Problema que resolve:** em um CRUD simples, regras importantes (baixar o estoque, validar a disponibilidade, calcular o total com desconto, consolidar relatórios) ficam espalhadas pelo código da aplicação, e uma falha no meio de uma venda pode deixar os dados inconsistentes. Neste projeto essas regras foram levadas para dentro do banco de dados, usando **Views**, **Function** e **Procedures**, o que garante consistência (a venda é gravada por inteiro ou não é gravada) e evita duplicar lógica no sistema.

### Principais funcionalidades

- Cadastro, listagem e exclusão de **clientes**
- Cadastro, listagem, exclusão, **edição** (nome e preço) e **reposição de estoque** de produtos
- **Venda com vários produtos** (carrinho), com desconto percentual
- **Relatório de vendas** consolidado e detalhamento dos itens de cada venda
- **Cálculo do total** de uma venda com desconto
- Alerta visual de **estoque baixo** (5 unidades ou menos)

---

## 🛠️ Tecnologias utilizadas

```
Python 3
Tkinter / ttk (interface gráfica)
psycopg2 (conexão com o PostgreSQL)
PostgreSQL
pgAdmin 4
Git / GitHub
VS Code
```

---

## 📁 Estrutura do repositório

```
sistema_vendas/
│
├── src/
│   └── sistema_vendas.py              # código-fonte da aplicação
│
├── database/
│   ├── tabelas/
│   │   └── tabelas.sql              # criação das tabelas
│   ├── views/
│   │   ├── vw_relatorio_vendas.sql
│   │   └── vw_itens_venda.sql
│   ├── functions/
│   │   └── fn_calcular_total_venda.sql
│   ├── procedures/
│   │   ├── sp_registrar_venda_multipla.sql
│   │   └── sp_repor_estoque.sql
│   └── inserts/
│       └── inserts_teste.sql       # clientes e produtos de teste
│
└── README.md
```

---

## 🖥️ Telas da aplicação

A janela principal possui 5 abas.

### 1. Clientes
Cadastro de clientes (nome e e-mail), listagem e exclusão.

<img width="1920" height="1020" alt="Captura de tela 2026-10-05 181539" src="https://github.com/user-attachments/assets/d619aad0-c419-4215-9324-f119c2e2975f" />


### 2. Produtos
Cadastro, listagem, exclusão, **edição de nome e preço** (botão ou dois cliques) e **reposição de estoque**. Produtos com estoque baixo aparecem em vermelho.

- Botão **Repor estoque** → chama a Procedure `sp_repor_estoque`.

<img width="1920" height="1020" alt="Captura de tela 2026-10-05 181559" src="https://github.com/user-attachments/assets/7456b75c-2c1c-4051-becb-afda4259132b" />


### 3. Nova venda (Procedure)
O usuário escolhe o cliente, adiciona **vários produtos ao carrinho**, informa o desconto e finaliza a venda.

- Botão **Finalizar venda** → chama a Procedure `sp_registrar_venda_multipla`.
- Ao concluir, o total exibido é calculado pela Function `fn_calcular_total_venda`.

<img width="1920" height="1020" alt="Captura de tela 2026-10-05 181715" src="https://github.com/user-attachments/assets/5bf4941a-1f44-47c2-b1b2-34d773579441" />


### 4. Relatório (View)
Lista todas as vendas (cliente, data, quantidade de itens, subtotal e desconto). Com **dois cliques em uma venda**, são exibidos os produtos que a compõem.

- Listagem → consulta a View `vw_relatorio_vendas`.
- Detalhe da venda → consulta a View `vw_itens_venda`.

<img width="1920" height="1020" alt="Captura de tela 2026-10-05 181741" src="https://github.com/user-attachments/assets/5f11de6e-1783-4bda-99af-55558d0913b5" />

<img width="1920" height="1020" alt="Captura de tela 2026-10-05 183459" src="https://github.com/user-attachments/assets/5c977f0b-c670-4e06-be11-3f02ba590ba7" />


### 5. Total da venda (Function)
O usuário escolhe uma venda e o sistema mostra o valor final, já com o desconto aplicado.

- Botão **Calcular total** → chama a Function `fn_calcular_total_venda`.

<img width="1920" height="1020" alt="Captura de tela 2026-10-05 181803" src="https://github.com/user-attachments/assets/34ff77e0-aa77-441e-88a5-c2cc3074ebca" />

---

## 🗄️ Banco de dados

**SGBD:** PostgreSQL (administrado pelo pgAdmin 4)  
**Banco:** `loja_db`

### Principais tabelas

| Tabela | Descrição | Colunas principais |
|---|---|---|
| `clientes` | Clientes da loja | `id`, `nome`, `email` (único), `criado_em` |
| `produtos` | Produtos à venda | `id`, `nome`, `preco`, `estoque` |
| `vendas` | Cabeçalho de cada venda | `id`, `cliente_id` (FK), `data_venda`, `desconto_pct` |
| `itens_venda` | Itens de cada venda | `id`, `venda_id` (FK), `produto_id` (FK), `quantidade`, `preco_unitario` |

**Relacionamentos:** um cliente tem várias vendas; uma venda tem vários itens; um produto aparece em vários itens. O `preco_unitario` é gravado no item, então alterar o preço de um produto **não muda vendas antigas**.

---

### 👁️ View 1 – `vw_relatorio_vendas`

| | |
|---|---|
| **Arquivo** | `database/views/01_vw_relatorio_vendas.sql` |
| **Por que foi criada** | Para entregar o relatório de vendas já consolidado, sem montar JOINs e agrupamentos dentro do código Python |
| **Tabelas envolvidas** | `vendas`, `clientes`, `itens_venda` |
| **Informação retornada** | Uma linha por venda: número, cliente, data, quantidade total de itens, subtotal e desconto |
| **Onde é utilizada** | Aba **Relatório (View)** |
| **Problema que resolve** | Centraliza a regra de consolidação em um único lugar; a aplicação só faz `SELECT * FROM vw_relatorio_vendas` |

### 👁️ View 2 – `vw_itens_venda`

| | |
|---|---|
| **Arquivo** | `database/views/02_vw_itens_venda.sql` |
| **Por que foi criada** | Para detalhar o que foi vendido em cada venda (a View 1 mostra só o total) |
| **Tabelas envolvidas** | `itens_venda`, `produtos` |
| **Informação retornada** | Para cada item: venda, nome do produto, quantidade, preço unitário e subtotal do item |
| **Onde é utilizada** | Aba **Relatório (View)**, ao dar dois cliques em uma venda |
| **Problema que resolve** | Permite conferir os produtos de uma venda com vários itens sem repetir JOINs na aplicação |

---

### ⚙️ Function – `fn_calcular_total_venda(p_venda_id INT)`

| | |
|---|---|
| **Arquivo** | `database/functions/01_fn_calcular_total_venda.sql` |
| **O que faz** | Soma `quantidade × preço` dos itens da venda e aplica o desconto percentual da venda |
| **Parâmetros** | `p_venda_id` (INT): número da venda |
| **Retorno** | `NUMERIC`: valor final da venda, arredondado em 2 casas. Gera erro se a venda não existir |
| **Onde é utilizada** | Aba **Total da venda (Function)** e mensagem de confirmação ao finalizar uma venda na aba **Nova venda** |
| **Problema que resolve** | Garante que o cálculo do valor final seja sempre o mesmo, vindo de uma única regra no banco |

---

### 🔁 Procedure 1 – `sp_registrar_venda_multipla(...)`

| | |
|---|---|
| **Arquivo** | `database/procedures/01_sp_registrar_venda_multipla.sql` |
| **O que faz** | Registra uma venda completa com um ou vários produtos |
| **Parâmetros** | `p_cliente_id` (INT), `p_produtos` (INT[]), `p_quantidades` (INT[]), `p_desconto_pct` (NUMERIC) e `p_venda_id` (INOUT, devolve o número da venda criada) |
| **Operações realizadas** | 1) valida o cliente; 2) valida a lista de produtos; 3) cria a venda; 4) para cada item: trava o produto, confere o estoque, grava o item com o preço atual e baixa o estoque |
| **Tela que chama** | Aba **Nova venda (Procedure)**, botão **Finalizar venda** |
| **Problema que resolve** | Torna a venda **atômica**: se qualquer item falhar (ex.: estoque insuficiente), nada é gravado, evitando venda pela metade e estoque inconsistente |

### 🔁 Procedure 2 – `sp_repor_estoque(p_produto_id, p_quantidade)`

| | |
|---|---|
| **Arquivo** | `database/procedures/02_sp_repor_estoque.sql` |
| **O que faz** | Soma uma quantidade ao estoque de um produto |
| **Parâmetros** | `p_produto_id` (INT), `p_quantidade` (INT, deve ser maior que zero) |
| **Operações realizadas** | Valida a quantidade, atualiza o estoque e gera erro se o produto não existir |
| **Tela que chama** | Aba **Produtos**, botão **Repor estoque** |
| **Problema que resolve** | Padroniza a entrada de mercadoria com validação feita no banco |

---

### 🔗 Funcionamento integrado

```
VENDA
Tela "Nova venda"  →  botão Finalizar venda  →  psycopg2: CALL sp_registrar_venda_multipla(...)
   →  Procedure grava venda + itens e baixa o estoque
   →  Function fn_calcular_total_venda calcula o total
   →  Total exibido na aplicação

RELATÓRIO
Tela "Relatório"  →  SELECT * FROM vw_relatorio_vendas  →  tabela exibida na tela
(dois cliques)    →  SELECT ... FROM vw_itens_venda     →  itens da venda exibidos

TOTAL
Tela "Total da venda"  →  SELECT fn_calcular_total_venda(id)  →  valor exibido na tela

ESTOQUE
Tela "Produtos"  →  botão Repor estoque  →  CALL sp_repor_estoque(...)  →  estoque atualizado
```
---

## ▶️ Como executar

**Pré-requisitos:** Python 3.10+ (com Tkinter), PostgreSQL e pgAdmin 4.

1. **Clone o repositório**

2. **Crie o banco no pgAdmin 4:** 

3. **Execute os scripts**

4. **Instale a dependência**

5. **Configure a conexão:** 

6. **Execute a aplicação**
```bash
   python src/sistema_vendas.py
```

---

## 🎥 Vídeo Demostrativo

🔗 **Link do vídeo:  ** 



O vídeo demonstra o funcionamento da aplicação e o uso dos recursos de banco de dados:


## 👤 Autor

**Ronald Machado**  
   [Projeto de Banco de Dados] – [Anderson Soares] – [ 4º Semestre]
