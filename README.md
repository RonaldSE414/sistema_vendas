
# 🛒 Sistema de Vendas – PostgreSQL, Supabase e Redis

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

O Sistema de Vendas é uma aplicação desktop desenvolvida em Python, com interface gráfica em Tkinter, destinada ao gerenciamento de clientes, produtos, estoque e vendas de uma loja.

O projeto foi desenvolvido inicialmente utilizando PostgreSQL instalado localmente e, nesta nova versão, foi ampliado com a integração de duas tecnologias: **Supabase e Redis**.

O Supabase é utilizado para hospedar o banco de dados PostgreSQL na nuvem, permitindo que os registros sejam armazenados em um servidor remoto.

O Redis é utilizado como mecanismo de cache, armazenando temporariamente os resultados de consultas frequentes para reduzir a necessidade de acessar repetidamente o banco de dados principal.

A interface gráfica original foi preservada, mantendo as cinco abas e suas funcionalidades.

### Problema que o sistema resolve

Em um CRUD simples, regras importantes, como baixar o estoque, validar a disponibilidade de produtos, calcular descontos e consolidar relatórios, podem ficar espalhadas pelo código da aplicação.

Isso aumenta o risco de inconsistências, principalmente quando uma operação envolve várias alterações no banco de dados.

Para solucionar esse problema, o sistema utiliza Views, Function e Procedures do PostgreSQL.

Esses recursos centralizam regras de negócio no banco de dados e permitem que operações, como o registro de uma venda, sejam executadas de forma transacional.

Com a integração ao Supabase, o armazenamento deixou de depender exclusivamente do PostgreSQL local.

A implementação do Redis acrescentou uma camada de cache para consultas, permitindo o reaproveitamento temporário dos resultados.

---

## 🎯 Objetivos

### Objetivo geral

Desenvolver e ampliar um sistema de gerenciamento de vendas, integrando banco de dados relacional na nuvem, mecanismo de cache e interface gráfica.

### Objetivos específicos

- Implementar operações de cadastro, consulta, atualização e exclusão de registros.
- Utilizar PostgreSQL como sistema gerenciador de banco de dados.
- Hospedar o banco PostgreSQL no Supabase.
- Integrar Redis para armazenamento temporário de consultas.
- Aplicar Views, Function e Procedures para execução de operações no banco.
- Garantir a consistência das operações de vendas e atualização do estoque.
- Manter uma interface gráfica desenvolvida em Python.
- Implementar mecanismos de invalidação de cache após modificações nos dados.
- Organizar e documentar o funcionamento do sistema.

---

## ⚙️ Funcionalidades

O sistema apresenta as seguintes funcionalidades:

- Cadastro, listagem e exclusão de clientes.
- Cadastro, listagem e exclusão de produtos.
- Edição de nome e preço dos produtos.
- Reposição de estoque.
- Registro de vendas com vários produtos.
- Carrinho de compras.
- Aplicação de descontos percentuais.
- Baixa automática do estoque após uma venda.
- Relatório consolidado de vendas.
- Consulta detalhada dos itens vendidos.
- Cálculo automático do valor final da venda.
- Alerta visual para produtos com estoque baixo.
- Armazenamento temporário de consultas no Redis.
- Invalidação do cache após operações de alteração no banco.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3 | Desenvolvimento da aplicação |
| Tkinter / ttk | Interface gráfica desktop |
| PostgreSQL | Banco de dados relacional |
| Supabase | Hospedagem do PostgreSQL na nuvem |
| Redis Cloud | Armazenamento temporário de consultas |
| psycopg2 | Comunicação entre Python e PostgreSQL |
| redis-py | Comunicação entre Python e Redis |
| python-dotenv | Carregamento das configurações do ambiente |
| SQL / PLpgSQL | Consultas, Views, Function e Procedures |
| Git / GitHub | Versionamento e armazenamento do projeto |
| VS Code | Desenvolvimento e execução |

---

## 📁 Estrutura do repositório

```text
sistema_vendas/
│
├── src/
│   └── sistema_vendas.py
│
├── database/
│   ├── tabelas/
│   │   └── tabelas.sql
│   │
│   ├── views/
│   │   ├── vw_relatorio_vendas.sql
│   │   └── vw_itens_venda.sql
│   │
│   ├── functions/
│   │   └── fn_calcular_total_venda.sql
│   │
│   ├── procedures/
│   │   ├── sp_registrar_venda_multipla.sql
│   │   └── sp_repor_estoque.sql
│   │
│   └── inserts/
│       └── inserts_teste.sql
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

O arquivo `.env`, utilizado para armazenar as credenciais reais, não deve ser publicado no GitHub.

---

## 🖥️ Interface gráfica

A aplicação mantém as cinco abas presentes na versão original.

### 1. Clientes

Permite cadastrar clientes informando nome e e-mail, visualizar os registros existentes e excluir clientes selecionados.

Os dados são armazenados no PostgreSQL hospedado no Supabase.

A consulta de clientes pode utilizar o cache Redis.

<img width="1920" height="1020" alt="Tela de clientes" src="https://github.com/user-attachments/assets/d619aad0-c419-4215-9324-f119c2e2975f" />

### 2. Produtos

Permite cadastrar, listar, editar e excluir produtos.

Cada produto possui nome, preço e quantidade disponível em estoque.

O sistema destaca visualmente os produtos com estoque igual ou inferior a cinco unidades.

A reposição de estoque utiliza a Procedure `sp_repor_estoque`.

Após alterações nos produtos, o cache do sistema é invalidado para que consultas posteriores obtenham informações atualizadas.

<img width="1920" height="1020" alt="Tela de produtos" src="https://github.com/user-attachments/assets/7456b75c-2c1c-4051-becb-afda4259132b" />

### 3. Nova venda (Procedure)

O usuário seleciona um cliente, escolhe os produtos, informa as quantidades e adiciona os itens ao carrinho.

Também é possível informar um desconto percentual.

Ao finalizar a venda, o sistema chama a Procedure `sp_registrar_venda_multipla`.

A Procedure registra a venda, grava os itens e atualiza o estoque.

Após o registro, a Function `fn_calcular_total_venda` calcula o valor final.

<img width="1920" height="1020" alt="Tela de nova venda" src="https://github.com/user-attachments/assets/5bf4941a-1f44-47c2-b1b2-34d773579441" />

### 4. Relatório (View)

Apresenta um relatório consolidado das vendas registradas.

São exibidas informações como:

- Número da venda.
- Cliente.
- Data.
- Quantidade de itens.
- Subtotal.
- Desconto percentual.

A listagem utiliza a View `vw_relatorio_vendas`.

Ao clicar duas vezes em uma venda, o sistema consulta a View `vw_itens_venda` para apresentar os produtos vendidos.

<img width="1920" height="1020" alt="Relatório de vendas" src="https://github.com/user-attachments/assets/5f11de6e-1783-4bda-99af-55558d0913b5" />

<img width="1920" height="1020" alt="Detalhamento dos itens da venda" src="https://github.com/user-attachments/assets/5c977f0b-c670-4e06-be11-3f02ba590ba7" />

### 5. Total da venda (Function)

Permite selecionar uma venda já registrada e calcular seu valor final.

O cálculo utiliza a Function `fn_calcular_total_venda`, que considera os itens vendidos e o desconto aplicado.

<img width="1920" height="1020" alt="Tela de cálculo do total da venda" src="https://github.com/user-attachments/assets/34ff77e0-aa77-441e-88a5-c2cc3074ebca" />

### 6. Tabelas sincronizadas dentro do supabase

<img width="1825" height="496" alt="Captura de tela 2026-10-25 202929" src="https://github.com/user-attachments/assets/4af263bb-8894-4ba1-bb29-dbbd8b9181e0" />


### 7. Redis integrado no sistema

<img width="1638" height="632" alt="Captura de tela 2026-10-25 205310" src="https://github.com/user-attachments/assets/aa20cb5b-7a70-4ab9-8414-c4750f815a95" />


### 8. Testes de conexão com Supabase e Redis Cloud no terminal do VS Code, com confirmação do funcionamento do cache Redis

Os testes confirmaram a conexão com o PostgreSQL hospedado no Supabase e com o Redis Cloud. Também foi verificado o armazenamento de consultas no cache, com três chaves registradas no Redis durante a execução.

<img width="1555" height="340" alt="Captura de tela 2026-10-25 205953" src="https://github.com/user-attachments/assets/dca7eae1-7978-41a8-b23c-8e01b43583f0" />

---

## 🗄️ Banco de dados PostgreSQL no Supabase

### Implementação anterior

Na versão inicial, o sistema utilizava PostgreSQL instalado localmente, com o banco `loja_db`, administrado por ferramentas como o pgAdmin 4.

A conexão Python era realizada por meio do endereço `localhost`.

### Implementação atual

Na versão atualizada, o banco PostgreSQL está hospedado no Supabase.

O Supabase permite armazenar os registros remotamente e executar as mesmas estruturas SQL utilizadas anteriormente.

A conexão é realizada utilizando `psycopg2` e uma string PostgreSQL configurada por meio de variável de ambiente.

### Principais tabelas

| Tabela | Descrição | Colunas principais |
|---|---|---|
| `clientes` | Clientes cadastrados | `id`, `nome`, `email`, `criado_em` |
| `produtos` | Produtos disponíveis | `id`, `nome`, `preco`, `estoque` |
| `vendas` | Registro geral das vendas | `id`, `cliente_id`, `data_venda`, `desconto_pct` |
| `itens_venda` | Produtos de cada venda | `id`, `venda_id`, `produto_id`, `quantidade`, `preco_unitario` |

### Relacionamentos

- Um cliente pode possuir várias vendas.
- Uma venda pode conter vários itens.
- Um produto pode aparecer em diferentes vendas.
- Cada item registra o preço unitário no momento da venda.

O armazenamento do preço unitário permite preservar o histórico financeiro, mesmo que o preço de um produto seja alterado posteriormente.

---

## 👁️ Views

### View 1 — vw_relatorio_vendas

**Arquivo:** `database/views/vw_relatorio_vendas.sql`

Consolida as informações das vendas realizadas.

Utiliza as tabelas:

- `vendas`
- `clientes`
- `itens_venda`

Retorna dados como número da venda, cliente, data, quantidade de itens, subtotal e desconto.

É utilizada na aba Relatório.

A aplicação executa:

```sql
SELECT *
FROM vw_relatorio_vendas
ORDER BY venda_id DESC;
```

### View 2 — vw_itens_venda

**Arquivo:** `database/views/vw_itens_venda.sql`

Apresenta informações detalhadas sobre os produtos de cada venda.

Utiliza as tabelas:

- `itens_venda`
- `produtos`

Retorna o nome do produto, quantidade, preço unitário e subtotal.

É utilizada quando o usuário abre o detalhamento de uma venda.

---

## ⚙️ Function

### fn_calcular_total_venda(p_venda_id INT)

**Arquivo:** `database/functions/fn_calcular_total_venda.sql`

A Function calcula o valor total da venda considerando o subtotal dos itens e o desconto percentual.

O cálculo segue a expressão:

```text
Total = Subtotal × (1 - Desconto / 100)
```

Exemplo:

Uma venda com subtotal de R$ 200,00 e desconto de 10% terá valor final de R$ 180,00.

A Function recebe o identificador da venda e retorna um valor numérico com duas casas decimais.

Também verifica se a venda informada existe.

Exemplo de utilização:

```sql
SELECT fn_calcular_total_venda(1);
```

---

## 🔁 Procedures

### Procedure 1 — sp_registrar_venda_multipla

**Arquivo:** `database/procedures/sp_registrar_venda_multipla.sql`

Responsável pelo registro de vendas com um ou vários produtos.

Recebe:

- Identificador do cliente.
- Lista de produtos.
- Lista de quantidades.
- Percentual de desconto.
- Parâmetro de saída com o identificador da venda.

A Procedure executa as seguintes operações:

1. Verifica se o cliente existe.
2. Valida a lista de produtos.
3. Cria o registro da venda.
4. Verifica os produtos e suas quantidades.
5. Confere a disponibilidade do estoque.
6. Registra os itens vendidos.
7. Atualiza o estoque.
8. Retorna o identificador da venda.

As operações fazem parte de uma transação.

Se algum produto não possuir estoque suficiente, a transação é revertida, evitando o registro parcial de uma venda.

### Procedure 2 — sp_repor_estoque

**Arquivo:** `database/procedures/sp_repor_estoque.sql`

Responsável por aumentar a quantidade disponível de determinado produto.

Recebe:

- Identificador do produto.
- Quantidade a adicionar.

A Procedure verifica se a quantidade é válida e se o produto existe.

Exemplo:

```sql
CALL sp_repor_estoque(1, 10);
```

Esse comando adiciona dez unidades ao estoque do produto de ID 1.

---

## ☁️ Integração com Supabase

O Supabase foi utilizado como serviço de hospedagem do banco PostgreSQL.

A estrutura original do projeto foi reproduzida no SQL Editor do Supabase, incluindo:

- Quatro tabelas.
- Duas Views.
- Uma Function.
- Duas Procedures.

A aplicação Python realiza a conexão com o banco remoto por meio da biblioteca `psycopg2`.

A string de conexão fica armazenada na variável `DATABASE_URL`, configurada no arquivo `.env`.

### Funcionamento

```text
Interface Tkinter
       |
       v
Aplicação Python
       |
       v
psycopg2
       |
       v
Supabase (PostgreSQL)
       |
       v
Tabelas, Views, Function e Procedures
```

Essa integração permite executar operações SQL no banco hospedado na nuvem, sem depender do PostgreSQL local.

---

## ⚡ Integração com Redis Cloud

### O que é Redis?

Redis é um banco de dados que pode manter informações em memória e é frequentemente utilizado como mecanismo de cache.

No projeto, ele não substitui o PostgreSQL.

O PostgreSQL continua responsável pelo armazenamento principal e persistente das informações.

O Redis funciona como uma camada intermediária para reaproveitar temporariamente resultados de consultas.

### Por que utilizar Redis?

Quando uma aplicação acessa um banco remoto, cada consulta envolve comunicação pela rede.

Consultas frequentes e repetidas podem aumentar o tempo de resposta.

O Redis permite armazenar temporariamente os resultados e recuperá-los sem realizar novamente a mesma consulta no PostgreSQL.

### Funcionamento do cache

O sistema utiliza uma estratégia de cache para consultas de leitura.

O processo ocorre da seguinte forma:

1. A aplicação recebe uma solicitação de consulta.
2. Verifica se o resultado está armazenado no Redis.
3. Se estiver, recupera os dados do cache.
4. Se não estiver, consulta o PostgreSQL no Supabase.
5. Armazena temporariamente o resultado no Redis.
6. Retorna os dados para a interface.

### Cache HIT

Acontece quando os dados solicitados já estão armazenados no Redis.

Nesse caso, o resultado é recuperado do cache.

### Cache MISS

Acontece quando o resultado não está disponível no Redis.

Nesse caso, a aplicação consulta o PostgreSQL e pode armazenar o resultado para consultas posteriores.

### Tempo de expiração

A variável `CACHE_TTL` determina por quanto tempo os resultados permanecem armazenados.

Exemplo:

```env
CACHE_TTL=300
```

Nesse caso, o cache possui tempo de expiração de 300 segundos, equivalente a cinco minutos.

### Invalidação do cache

O sistema invalida as chaves de cache relacionadas à aplicação após operações de alteração no PostgreSQL.

Isso inclui:

- Cadastro de clientes.
- Exclusão de clientes.
- Cadastro de produtos.
- Edição de produtos.
- Exclusão de produtos.
- Reposição de estoque.
- Registro de vendas.

A invalidação impede que a própria aplicação continue reutilizando resultados anteriores após essas alterações.

### Tratamento de indisponibilidade

O Redis é utilizado como mecanismo auxiliar.

Se o Redis estiver indisponível, a aplicação poderá continuar consultando o PostgreSQL diretamente.

As operações de venda e atualização de estoque continuam dependendo das regras transacionais do PostgreSQL.

---

## 🔗 Arquitetura integrada

```text
                 USUÁRIO
                    |
                    v
             PYTHON + TKINTER
                    |
                    v
              APLICAÇÃO
                    |
          CONSULTA DE LEITURA
                    |
                    v
                  REDIS
                 /     \
                /       \
           CACHE HIT   CACHE MISS
              |            |
              v            v
        Retorna dados   SUPABASE
                            |
                            v
                       POSTGRESQL
                            |
                            v
                      Retorna dados
                            |
                            v
                      Atualiza cache
```

Nas operações de escrita, a aplicação utiliza o PostgreSQL e invalida o cache após a confirmação da alteração.

---

## 🔐 Configuração das conexões

O sistema utiliza variáveis de ambiente para evitar que credenciais sejam escritas diretamente no código-fonte.

Crie um arquivo `.env` na pasta principal do projeto, utilizando `.env.example` como referência.

Exemplo:

```env
DATABASE_URL=postgresql://USUARIO:SENHA@SERVIDOR:5432/postgres
REDIS_URL=redis://USUARIO:SENHA@SERVIDOR:PORTA
CACHE_TTL=300
```

Substitua os valores de exemplo pelas configurações reais dos serviços.

### Segurança

- Nunca publique o arquivo `.env`.
- Não compartilhe senhas do PostgreSQL.
- Não compartilhe senhas do Redis.
- Utilize o arquivo `.gitignore`.
- Não coloque credenciais diretamente no código Python.

**Observação sobre Redis Cloud Free:** o plano gratuito utilizado nesta implementação não oferece TLS para a conexão Redis. Por isso, esta configuração deve ser tratada como ambiente de demonstração acadêmica, sem dados sensíveis. Aplicações de produção devem utilizar transporte criptografado, autenticação e controles de acesso apropriados.

---

## ▶️ Como executar o projeto

### Pré-requisitos

- Python 3.10 ou superior.
- Tkinter disponível na instalação Python.
- Projeto criado no Supabase.
- Banco Redis Cloud configurado.
- VS Code ou outro editor.
- Conexão com a internet.

### 1. Clonar o repositório

```bash
git clone https://github.com/RonaldSE414/sistema_vendas.git
```

Entre na pasta:

```bash
cd sistema_vendas
```

### 2. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

As principais dependências são:

```text
psycopg2-binary
redis
python-dotenv
```

### 3. Criar as estruturas no Supabase

Acesse o SQL Editor do projeto Supabase e execute os arquivos nesta ordem:

1. `database/tabelas/tabelas.sql`
2. `database/views/vw_relatorio_vendas.sql`
3. `database/views/vw_itens_venda.sql`
4. `database/functions/fn_calcular_total_venda.sql`
5. `database/procedures/sp_repor_estoque.sql`
6. `database/procedures/sp_registrar_venda_multipla.sql`

Opcionalmente, execute `database/inserts/inserts_teste.sql` para inserir registros fictícios.

### 4. Configurar o ambiente

Crie o arquivo `.env` na pasta principal do projeto.

Preencha:

```env
DATABASE_URL=SUA_CONEXAO_POSTGRESQL
REDIS_URL=SUA_CONEXAO_REDIS
CACHE_TTL=300
```


### 5. Executar a aplicação

```bash
python src/sistema_vendas.py
```

A janela principal será aberta com as cinco abas do sistema.

---

## 🧪 Testes de funcionamento

### Teste 1 — Conexão com Supabase

1. Abra a aplicação.
2. Cadastre um cliente fictício.
3. Acesse o Table Editor do Supabase.
4. Abra a tabela `clientes`.
5. Confirme que o registro foi armazenado.

Esse teste verifica a comunicação entre a interface Python e o banco PostgreSQL remoto.

### Teste 2 — Conexão com Redis

Execute no terminal, com o arquivo `.env` configurado:

```bash
python -c "import os,redis; from dotenv import load_dotenv; load_dotenv(); r=redis.from_url(os.environ['REDIS_URL']); print('Redis conectado:',r.ping())"
```

Resultado esperado:

```text
Redis conectado: True
```

### Teste 3 — Armazenamento no cache

Com o terminal aberto na pasta principal do projeto, execute:

```bash
python -c "import sistema_vendas as s; q='SELECT id, nome, email FROM clientes ORDER BY id /* teste redis */'; s.executar(q,fetch=True); print('Cache gravado:',bool(s.cache.exists(s.cache_key(q,None)))); s.executar(q,fetch=True); print('Cache disponível:',bool(s.cache.exists(s.cache_key(q,None))))"
```

Uma consulta repetida poderá gerar Cache HIT, confirmando a recuperação de informações do Redis.

### Teste 4 — Invalidação do cache

1. Abra o sistema de vendas.
2. Consulte os clientes ou produtos.
3. Cadastre um novo registro.
4. Atualize a listagem.
5. Confirme que o novo registro aparece.
6. Verifique o mesmo registro no Supabase.

Esse procedimento ajuda a validar a atualização das informações após operações de escrita.

### Teste 5 — Registro de venda

1. Cadastre um cliente.
2. Cadastre produtos com estoque disponível.
3. Abra a aba Nova venda.
4. Adicione produtos ao carrinho.
5. Informe um desconto, se desejar.
6. Finalize a venda.
7. Verifique o estoque atualizado.
8. Abra a aba Relatório.
9. Confira a venda registrada no Supabase.

Esse teste verifica a integração da interface com a Procedure de vendas e o cálculo do valor final.

---

## 🔄 Evolução do projeto

### Versão 1 — PostgreSQL local

A primeira versão utilizava:

- Python.
- Tkinter.
- PostgreSQL local.
- psycopg2.
- Views.
- Function.
- Procedures.
- pgAdmin 4.

O banco era acessado por meio de conexão local.

### Versão 2 — Supabase e Redis

A segunda versão acrescentou:

- Hospedagem do PostgreSQL no Supabase.
- Conexão remota utilizando variáveis de ambiente.
- Redis Cloud para cache.
- Expiração automática das entradas de cache.
- Invalidação após alterações no banco.
- Tratamento de indisponibilidade do Redis.
- Atualização das dependências e da documentação.

A estrutura das tabelas e a interface gráfica original foram mantidas.

---

## 📊 Resultados da implementação

A integração do Supabase permitiu substituir a conexão ao banco local por uma conexão ao PostgreSQL hospedado na nuvem.

A integração com Redis acrescentou uma camada de cache para consultas, com armazenamento temporário dos resultados e mecanismo de invalidação.

A aplicação continua utilizando as regras de negócio implementadas no PostgreSQL por meio de Views, Function e Procedures.

Os testes de conexão realizados durante a configuração confirmaram a comunicação do Python com o Supabase e o Redis Cloud, além da criação de entradas de cache.

O desempenho depende de fatores como latência da rede, localização dos servidores, tempo de expiração do cache e frequência das consultas.

O uso do Redis não elimina a necessidade de consultar o PostgreSQL em operações de escrita ou em situações de Cache MISS.

---

## 🎥 Vídeo demonstrativo

### Demonstração da versão atualizada — Supabase e Redis 

[Assistir ao vídeo no Google Drive](https://drive.google.com/file/d/1YJB2CpyHNNqElXhb6uu-zWLvbBtZNNMS/view?usp=sharing).

### Demonstração da versão original — PostgreSQL local

[Assistir ao vídeo no Google Drive](https://drive.google.com/file/d/1cw7ScubP6mJPa8e_FWyvAA3suQHkgdWi/view?usp=sharing)


---

## 👤 Autor

**Ronald Machado**

Disciplina: Projeto de Banco de Dados

Professor: Anderson Soares

Curso: 4º semestre

---

## 📚 Documentação das tecnologias

- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Supabase](https://supabase.com/docs)
- [Redis](https://redis.io/docs/latest/)
- [psycopg2](https://www.psycopg.org/docs/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [GitHub](https://github.com/)

---

## ✅ Considerações finais

O desenvolvimento do Sistema de Vendas permitiu aplicar conhecimentos de modelagem de dados, SQL, relacionamentos, transações, Views, Function e Procedures.

A ampliação do projeto com Supabase e Redis possibilitou trabalhar com banco de dados hospedado na nuvem e armazenamento temporário de consultas.

A solução demonstra a integração de diferentes tecnologias em uma aplicação desktop, preservando as funcionalidades existentes e acrescentando novos recursos de gerenciamento de dados e cache.
