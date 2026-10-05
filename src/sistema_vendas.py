import functools
import tkinter as tk
from decimal import Decimal
from tkinter import messagebox, simpledialog, ttk

import psycopg2
import psycopg2.errors

try:  # deixa a janela nítida no Windows
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "loja_db",
    "user": "postgres",
    "password": "0207",
    "connect_timeout": 5,
}


def conectar():
    return psycopg2.connect(**CONFIG)


def executar(sql, params=None, fetch=False):
    """Executa um comando SQL, faz commit e devolve as linhas se fetch=True."""
    conn = conectar()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if fetch:
                    return cur.fetchall()
    finally:
        conn.close()


# ======================================================================
# AUXILIARES
# ======================================================================
def brl(valor):
    """Formata número como moeda brasileira: R$ 1.234,56"""
    return "R$ " + f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def msg_erro_banco(e):
    if isinstance(e, psycopg2.errors.UniqueViolation):
        return "Já existe um registro com esse valor (e-mail duplicado)."
    if isinstance(e, psycopg2.errors.ForeignKeyViolation):
        return "Não é possível excluir: existem vendas vinculadas a este registro."
    return str(e).strip().splitlines()[0]


def seguro(metodo):
    """Captura erros do banco e mostra numa janela de aviso."""
    @functools.wraps(metodo)
    def wrapper(self, *args, **kwargs):
        try:
            return metodo(self, *args, **kwargs)
        except psycopg2.Error as e:
            messagebox.showerror("Erro no banco de dados", msg_erro_banco(e))
        except ValueError:
            messagebox.showwarning("Dado inválido", "Verifique os valores digitados.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    return wrapper


# ======================================================================
# ESTILO
# ======================================================================
FONTE = "Segoe UI"
AZUL = "#1f3a5f"
AZUL_CLARO = "#2d5a8a"
FUNDO = "#f4f6fa"
VERDE = "#2e7d32"
VERMELHO = "#c62828"


def configurar_estilo(raiz):
    s = ttk.Style(raiz)
    s.theme_use("clam")
    s.configure(".", font=(FONTE, 10), background=FUNDO)
    s.configure("TFrame", background=FUNDO)
    s.configure("TLabel", background=FUNDO)
    s.configure("TLabelframe", background=FUNDO)
    s.configure("TLabelframe.Label", background=FUNDO, foreground=AZUL,
                font=(FONTE, 10, "bold"))
    s.configure("TNotebook", background=FUNDO, borderwidth=0)
    s.configure("TNotebook.Tab", padding=(16, 8), font=(FONTE, 10, "bold"))
    s.map("TNotebook.Tab",
          background=[("selected", AZUL), ("!selected", "#dfe5ee")],
          foreground=[("selected", "white"), ("!selected", AZUL)])
    s.configure("Treeview", rowheight=28, font=(FONTE, 10))
    s.configure("Treeview.Heading", font=(FONTE, 10, "bold"),
                background=AZUL, foreground="white", padding=6)
    s.map("Treeview.Heading", background=[("active", AZUL_CLARO)])
    s.map("Treeview", background=[("selected", AZUL_CLARO)],
          foreground=[("selected", "white")])
    s.configure("Acao.TButton", background=AZUL, foreground="white",
                padding=(16, 7), font=(FONTE, 10, "bold"))
    s.map("Acao.TButton", background=[("active", AZUL_CLARO)])
    s.configure("Perigo.TButton", background=VERMELHO, foreground="white",
                padding=(16, 7), font=(FONTE, 10, "bold"))
    s.map("Perigo.TButton", background=[("active", "#e53935")])
    s.configure("Total.TLabel", font=(FONTE, 34, "bold"), foreground=VERDE)
    s.configure("Ok.TLabel", font=(FONTE, 11, "bold"), foreground=VERDE)
    s.configure("Resumo.TLabel", font=(FONTE, 11, "bold"), foreground=AZUL)
    s.configure("Info.TLabel", foreground="#555555")


def criar_tabela(pai, colunas):
    """colunas: lista de (id, titulo, largura, alinhamento). Retorna (frame, tree)."""
    frame = ttk.Frame(pai)
    tree = ttk.Treeview(frame, columns=[c[0] for c in colunas],
                        show="headings", selectmode="browse")
    for cid, titulo, largura, alinhamento in colunas:
        tree.heading(cid, text=titulo)
        tree.column(cid, width=largura, anchor=alinhamento)
    barra = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=barra.set)
    tree.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    tree.tag_configure("par", background="#eaf0f8")
    tree.tag_configure("baixo", foreground=VERMELHO)
    return frame, tree


def preencher(tree, linhas, destaque=None):
    """Limpa e preenche a tabela. A 1ª coluna de cada linha é o ID."""
    tree.delete(*tree.get_children())
    for i, linha in enumerate(linhas):
        tags = ["par"] if i % 2 else []
        if destaque and destaque[i]:
            tags.append("baixo")
        tree.insert("", "end", iid=str(linha[0]), values=linha, tags=tags)


def carregar_combo(combo, mapa):
    atual = combo.get()
    combo["values"] = list(mapa)
    if atual not in mapa:
        combo.set("")


# ======================================================================
# JANELA PRINCIPAL
# ======================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Vendas - Projeto de Banco de Dados")
        self.geometry("1060x780")
        self.minsize(960, 680)
        self.configure(bg=FUNDO)
        configurar_estilo(self)

        self.mapa_clientes, self.mapa_produtos, self.mapa_vendas = {}, {}, {}
        self.estoques, self.precos, self.nomes = {}, {}, {}
        self.carrinho = {}  # {produto_id: quantidade}

        self._criar_cabecalho()

        self.status = tk.StringVar(value="Conectado ao banco de dados.")
        tk.Label(self, textvariable=self.status, bg=AZUL, fg="white", anchor="w",
                 padx=14, pady=5, font=(FONTE, 9)).pack(fill="x", side="bottom")

        self.abas = ttk.Notebook(self)
        self.abas.pack(fill="both", expand=True, padx=14, pady=(10, 8))
        self._aba_clientes()
        self._aba_produtos()
        self._aba_venda()
        self._aba_relatorio()
        self._aba_total()

        self.atualizar()
        self.abas.bind("<<NotebookTabChanged>>", lambda e: self.atualizar())

    # ------------------------------------------------------------ layout
    def _criar_cabecalho(self):
        topo = tk.Frame(self, bg=AZUL)
        topo.pack(fill="x")
        tk.Label(topo, text="Sistema de Vendas", bg=AZUL, fg="white",
                 font=(FONTE, 20, "bold")).pack(anchor="w", padx=18, pady=(12, 0))
        tk.Label(topo, text="Projeto de Banco de Dados  •  View  •  Function  •  Procedure",
                 bg=AZUL, fg="#b8c7de", font=(FONTE, 10)).pack(anchor="w", padx=18, pady=(0, 12))

    def _nova_aba(self, titulo):
        aba = ttk.Frame(self.abas, padding=16)
        self.abas.add(aba, text=titulo)
        return aba

    def set_status(self, texto):
        self.status.set(texto)

    def _selecionado(self, tree, mensagem):
        """Devolve o ID da linha selecionada ou None (mostrando um aviso)."""
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", mensagem)
            return None
        return int(sel[0])

    # ------------------------------------------------------------ aba Clientes
    def _aba_clientes(self):
        aba = self._nova_aba("  Clientes  ")
        form = ttk.LabelFrame(aba, text="Novo cliente", padding=14)
        form.pack(fill="x")

        self.var_cli_nome, self.var_cli_email = tk.StringVar(), tk.StringVar()
        ttk.Label(form, text="Nome").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_cli_nome, width=34).grid(row=1, column=0, padx=(0, 14))
        ttk.Label(form, text="E-mail").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.var_cli_email, width=34).grid(row=1, column=1, padx=(0, 14))
        ttk.Button(form, text="Cadastrar", style="Acao.TButton",
                   command=self.cadastrar_cliente).grid(row=1, column=2)

        frame, self.tree_cli = criar_tabela(aba, [
            ("id", "ID", 70, "center"), ("nome", "Nome", 340, "w"), ("email", "E-mail", 340, "w")])
        frame.pack(fill="both", expand=True, pady=(14, 8))
        ttk.Button(aba, text="Excluir selecionado", style="Perigo.TButton",
                   command=self.excluir_cliente).pack(anchor="e")

    @seguro
    def cadastrar_cliente(self):
        nome, email = self.var_cli_nome.get().strip(), self.var_cli_email.get().strip()
        if not nome or not email:
            messagebox.showwarning("Campos obrigatórios", "Preencha nome e e-mail.")
            return
        executar("INSERT INTO clientes (nome, email) VALUES (%s, %s)", (nome, email))
        self.var_cli_nome.set("")
        self.var_cli_email.set("")
        self.atualizar()
        self.set_status(f"Cliente '{nome}' cadastrado com sucesso.")

    @seguro
    def excluir_cliente(self):
        cid = self._selecionado(self.tree_cli, "Selecione um cliente na tabela.")
        if cid is None:
            return
        if messagebox.askyesno("Confirmar", "Excluir o cliente selecionado?"):
            executar("DELETE FROM clientes WHERE id = %s", (cid,))
            self.atualizar()
            self.set_status("Cliente excluído.")

    # ------------------------------------------------------------ aba Produtos
    def _aba_produtos(self):
        aba = self._nova_aba("  Produtos  ")
        form = ttk.LabelFrame(aba, text="Novo produto", padding=14)
        form.pack(fill="x")

        self.var_prod_nome = tk.StringVar()
        self.var_prod_preco = tk.StringVar()
        self.var_prod_estoque = tk.StringVar(value="0")
        ttk.Label(form, text="Nome").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_prod_nome, width=30).grid(row=1, column=0, padx=(0, 14))
        ttk.Label(form, text="Preço (R$)").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.var_prod_preco, width=14).grid(row=1, column=1, padx=(0, 14))
        ttk.Label(form, text="Estoque").grid(row=0, column=2, sticky="w")
        ttk.Spinbox(form, from_=0, to=99999, textvariable=self.var_prod_estoque,
                    width=8).grid(row=1, column=2, padx=(0, 14))
        ttk.Button(form, text="Cadastrar", style="Acao.TButton",
                   command=self.cadastrar_produto).grid(row=1, column=3)

        frame, self.tree_prod = criar_tabela(aba, [
            ("id", "ID", 70, "center"), ("nome", "Produto", 340, "w"),
            ("preco", "Preço", 140, "e"), ("estoque", "Estoque", 120, "center")])
        frame.pack(fill="both", expand=True, pady=(14, 4))
        self.tree_prod.bind("<Double-1>", lambda e: self.editar_produto())

        rodape = ttk.Frame(aba)
        rodape.pack(fill="x", pady=(6, 0))
        ttk.Label(rodape, style="Info.TLabel",
                  text="Estoque em vermelho = 5 unidades ou menos. Dois cliques em um produto para editar."
                  ).pack(side="left")
        ttk.Button(rodape, text="Excluir", style="Perigo.TButton",
                   command=self.excluir_produto).pack(side="right")
        ttk.Button(rodape, text="Repor estoque", style="Acao.TButton",
                   command=self.repor_estoque).pack(side="right", padx=8)
        ttk.Button(rodape, text="Editar produto", style="Acao.TButton",
                   command=self.editar_produto).pack(side="right")

    @seguro
    def cadastrar_produto(self):
        nome = self.var_prod_nome.get().strip()
        if not nome:
            messagebox.showwarning("Campos obrigatórios", "Informe o nome do produto.")
            return
        preco = float(self.var_prod_preco.get().replace(",", "."))
        estoque = int(self.var_prod_estoque.get())
        executar("INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)",
                 (nome, preco, estoque))
        self.var_prod_nome.set("")
        self.var_prod_preco.set("")
        self.var_prod_estoque.set("0")
        self.atualizar()
        self.set_status(f"Produto '{nome}' cadastrado com sucesso.")

    @seguro
    def excluir_produto(self):
        pid = self._selecionado(self.tree_prod, "Selecione um produto na tabela.")
        if pid is None:
            return
        if messagebox.askyesno("Confirmar", "Excluir o produto selecionado?"):
            executar("DELETE FROM produtos WHERE id = %s", (pid,))
            self.carrinho.pop(pid, None)
            self.atualizar()
            self.set_status("Produto excluído.")

    # ---- Repor estoque (usa a PROCEDURE sp_repor_estoque)
    @seguro
    def repor_estoque(self):
        pid = self._selecionado(self.tree_prod, "Selecione um produto na tabela.")
        if pid is None:
            return
        qtd = simpledialog.askinteger(
            "Repor estoque",
            f"Quantas unidades adicionar ao estoque de\n'{self.nomes.get(pid, '')}'?",
            parent=self, minvalue=1, maxvalue=100000)
        if qtd is None:
            return
        executar("CALL sp_repor_estoque(%s, %s)", (pid, qtd))
        self.atualizar()
        self.set_status(f"Adicionadas {qtd} unidades ao estoque de '{self.nomes.get(pid, '')}'.")

    # ---- Editar produto (nome e preço)
    @seguro
    def editar_produto(self):
        pid = self._selecionado(self.tree_prod, "Selecione um produto na tabela.")
        if pid is None:
            return
        nome_atual, preco_atual = executar(
            "SELECT nome, preco FROM produtos WHERE id = %s", (pid,), fetch=True)[0]

        janela = tk.Toplevel(self)
        janela.title("Editar produto")
        janela.configure(bg=FUNDO)
        janela.transient(self)
        janela.resizable(False, False)
        janela.geometry(f"+{self.winfo_x() + 260}+{self.winfo_y() + 220}")

        var_nome = tk.StringVar(value=nome_atual)
        var_preco = tk.StringVar(value=f"{preco_atual:.2f}")

        corpo = ttk.Frame(janela, padding=20)
        corpo.pack()
        ttk.Label(corpo, text="Nome").grid(row=0, column=0, sticky="w")
        campo_nome = ttk.Entry(corpo, textvariable=var_nome, width=38)
        campo_nome.grid(row=1, column=0, columnspan=2, pady=(0, 12))
        ttk.Label(corpo, text="Preço (R$)").grid(row=2, column=0, sticky="w")
        ttk.Entry(corpo, textvariable=var_preco, width=14).grid(row=3, column=0, sticky="w", pady=(0, 16))

        botoes = ttk.Frame(corpo)
        botoes.grid(row=4, column=0, columnspan=2, sticky="e")
        ttk.Button(botoes, text="Cancelar", command=janela.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(botoes, text="Salvar", style="Acao.TButton",
                   command=lambda: self._salvar_produto(
                       pid, var_nome.get(), var_preco.get(), janela)).pack(side="right")

        campo_nome.focus()
        janela.grab_set()

    @seguro
    def _salvar_produto(self, pid, nome, preco_txt, janela):
        nome = nome.strip()
        if not nome:
            messagebox.showwarning("Campos obrigatórios", "Informe o nome do produto.", parent=janela)
            return
        preco = float(preco_txt.replace(",", "."))
        if preco <= 0:
            messagebox.showwarning("Atenção", "O preço deve ser maior que zero.", parent=janela)
            return
        executar("UPDATE produtos SET nome = %s, preco = %s WHERE id = %s", (nome, preco, pid))
        janela.destroy()
        self.atualizar()
        self.set_status(f"Produto '{nome}' atualizado.")

    # ------------------------------------------------------------ aba Nova venda (PROCEDURE)
    def _aba_venda(self):
        aba = self._nova_aba("  Nova venda (Procedure)  ")
        self.var_qtd = tk.StringVar(value="1")
        self.var_desc = tk.StringVar(value="0")

        # --- escolha do cliente e dos produtos
        form = ttk.LabelFrame(aba, text="1) Escolha o cliente e adicione produtos ao carrinho",
                              padding=14)
        form.pack(fill="x")

        ttk.Label(form, text="Cliente").grid(row=0, column=0, sticky="w", pady=6)
        self.cb_cliente = ttk.Combobox(form, state="readonly", width=62)
        self.cb_cliente.grid(row=0, column=1, columnspan=4, sticky="w", padx=12)

        ttk.Label(form, text="Produto").grid(row=1, column=0, sticky="w", pady=6)
        self.cb_produto = ttk.Combobox(form, state="readonly", width=46)
        self.cb_produto.grid(row=1, column=1, sticky="w", padx=12)
        self.cb_produto.bind("<<ComboboxSelected>>", self._mostrar_estoque)
        ttk.Label(form, text="Qtd").grid(row=1, column=2, sticky="e")
        ttk.Spinbox(form, from_=1, to=9999, textvariable=self.var_qtd,
                    width=6).grid(row=1, column=3, padx=(6, 12))
        ttk.Button(form, text="Adicionar ao carrinho", style="Acao.TButton",
                   command=self.adicionar_ao_carrinho).grid(row=1, column=4)
        self.lbl_estoque = ttk.Label(form, text="", style="Info.TLabel")
        self.lbl_estoque.grid(row=2, column=1, sticky="w", padx=12)

        # --- carrinho
        caixa = ttk.LabelFrame(aba, text="2) Carrinho", padding=10)
        caixa.pack(fill="both", expand=True, pady=12)
        frame, self.tree_carrinho = criar_tabela(caixa, [
            ("id", "ID", 60, "center"), ("produto", "Produto", 330, "w"),
            ("qtd", "Qtd", 70, "center"), ("preco", "Preço unit.", 130, "e"),
            ("subtotal", "Subtotal", 130, "e")])
        frame.pack(fill="both", expand=True)
        botoes = ttk.Frame(caixa)
        botoes.pack(fill="x", pady=(8, 0))
        ttk.Button(botoes, text="Remover item", style="Perigo.TButton",
                   command=self.remover_do_carrinho).pack(side="left")
        ttk.Button(botoes, text="Limpar carrinho", style="Perigo.TButton",
                   command=self.limpar_carrinho).pack(side="left", padx=8)

        # --- finalizar
        final = ttk.Frame(aba)
        final.pack(fill="x")
        ttk.Label(final, text="Desconto (%)").pack(side="left")
        ttk.Entry(final, textvariable=self.var_desc, width=8).pack(side="left", padx=(8, 24))
        self.lbl_resumo = ttk.Label(final, text="", style="Resumo.TLabel")
        self.lbl_resumo.pack(side="left")
        ttk.Button(final, text="Finalizar venda", style="Acao.TButton",
                   command=self.finalizar_venda).pack(side="right")

        self.lbl_resultado = ttk.Label(aba, text="", style="Ok.TLabel")
        self.lbl_resultado.pack(anchor="w", pady=(10, 0))

        self.var_desc.trace_add("write", lambda *a: self._atualizar_resumo())
        self._atualizar_resumo()

    def _mostrar_estoque(self, _evento=None):
        pid = self.mapa_produtos.get(self.cb_produto.get())
        self.lbl_estoque.config(
            text="" if pid is None else f"Estoque disponível: {self.estoques[pid]} un.")

    def _renderizar_carrinho(self):
        linhas = []
        for pid, qtd in self.carrinho.items():
            preco = self.precos.get(pid, Decimal(0))
            linhas.append((pid, self.nomes.get(pid, "(removido)"), qtd,
                           brl(preco), brl(preco * qtd)))
        preencher(self.tree_carrinho, linhas)
        self._atualizar_resumo()

    def _atualizar_resumo(self):
        subtotal = sum((self.precos.get(pid, Decimal(0)) * q
                        for pid, q in self.carrinho.items()), Decimal(0))
        try:
            desc = Decimal(self.var_desc.get().replace(",", ".") or "0")
        except Exception:
            desc = Decimal(0)
        desc = max(Decimal(0), min(Decimal(100), desc))
        total = (subtotal * (1 - desc / 100)).quantize(Decimal("0.01"))
        self.lbl_resumo.config(
            text=f"Itens: {sum(self.carrinho.values())}   |   Subtotal: {brl(subtotal)}"
                 f"   |   Total com desconto: {brl(total)}")

    @seguro
    def adicionar_ao_carrinho(self):
        pid = self.mapa_produtos.get(self.cb_produto.get())
        if pid is None:
            messagebox.showwarning("Atenção", "Escolha um produto.")
            return
        qtd = int(self.var_qtd.get())
        if qtd <= 0:
            messagebox.showwarning("Atenção", "A quantidade deve ser maior que zero.")
            return
        ja_no_carrinho = self.carrinho.get(pid, 0)
        if ja_no_carrinho + qtd > self.estoques[pid]:
            messagebox.showwarning(
                "Estoque insuficiente",
                f"Disponível: {self.estoques[pid]} un. (já no carrinho: {ja_no_carrinho}).")
            return
        self.carrinho[pid] = ja_no_carrinho + qtd
        self.var_qtd.set("1")
        self._renderizar_carrinho()
        self.set_status(f"'{self.nomes[pid]}' adicionado ao carrinho.")

    def remover_do_carrinho(self):
        pid = self._selecionado(self.tree_carrinho, "Selecione um item do carrinho.")
        if pid is not None:
            self.carrinho.pop(pid, None)
            self._renderizar_carrinho()

    def limpar_carrinho(self):
        self.carrinho.clear()
        self._renderizar_carrinho()

    @seguro
    def finalizar_venda(self):
        if not self.cb_cliente.get():
            messagebox.showwarning("Atenção", "Escolha o cliente.")
            return
        if not self.carrinho:
            messagebox.showwarning("Atenção", "O carrinho está vazio.")
            return
        desconto = float(self.var_desc.get().replace(",", ".") or 0)
        if not 0 <= desconto <= 100:
            messagebox.showwarning("Atenção", "O desconto deve estar entre 0 e 100.")
            return

        cliente_id = self.mapa_clientes[self.cb_cliente.get()]
        produtos = list(self.carrinho.keys())
        quantidades = [self.carrinho[p] for p in produtos]

        resultado = executar(
            "CALL sp_registrar_venda_multipla(%s, %s, %s, %s, NULL::int)",
            (cliente_id, produtos, quantidades, desconto),
            fetch=True,
        )
        venda_id = resultado[0][0]
        total = executar("SELECT fn_calcular_total_venda(%s)", (venda_id,), fetch=True)[0][0]

        qtd_produtos = len(produtos)
        self.carrinho.clear()
        self.var_desc.set("0")
        self.lbl_resultado.config(
            text=f"✔ Venda #{venda_id} registrada: {qtd_produtos} produto(s), total {brl(total)}")
        self.atualizar()
        self.set_status(f"Venda #{venda_id} registrada.")
        messagebox.showinfo("Sucesso", f"Venda #{venda_id} registrada!\nTotal: {brl(total)}")

    # ------------------------------------------------------------ aba Relatório (VIEW)
    def _aba_relatorio(self):
        aba = self._nova_aba("  Relatório (View)  ")
        ttk.Label(aba, style="Info.TLabel",
                  text="Dados da VIEW vw_relatorio_vendas. Dois cliques em uma venda mostram "
                       "os produtos dela (VIEW vw_itens_venda).").pack(anchor="w")
        frame, self.tree_rel = criar_tabela(aba, [
            ("venda", "Venda", 80, "center"), ("cliente", "Cliente", 240, "w"),
            ("data", "Data", 150, "center"), ("itens", "Itens", 80, "center"),
            ("subtotal", "Subtotal", 140, "e"), ("desc", "Desconto", 100, "center")])
        frame.pack(fill="both", expand=True, pady=(10, 8))
        self.tree_rel.bind("<Double-1>", self.detalhar_venda)
        ttk.Button(aba, text="Atualizar relatório", style="Acao.TButton",
                   command=self.atualizar).pack(anchor="e")

    @seguro
    def detalhar_venda(self, _evento=None):
        sel = self.tree_rel.selection()
        if not sel:
            return
        venda_id = int(sel[0])
        itens = executar(
            "SELECT produto, quantidade, preco_unitario, subtotal "
            "FROM vw_itens_venda WHERE venda_id = %s ORDER BY produto",
            (venda_id,), fetch=True)
        linhas = [f"{q}x {nome}  -  {brl(preco)} un.  =  {brl(sub)}"
                  for nome, q, preco, sub in itens]
        messagebox.showinfo(f"Itens da venda #{venda_id}", "\n".join(linhas))

    # ------------------------------------------------------------ aba Total (FUNCTION)
    def _aba_total(self):
        aba = self._nova_aba("  Total da venda (Function)  ")
        form = ttk.LabelFrame(aba, text="Calcular total  -  chama a FUNCTION fn_calcular_total_venda",
                              padding=18)
        form.pack(fill="x")
        ttk.Label(form, text="Venda").grid(row=0, column=0, sticky="w")
        self.cb_venda = ttk.Combobox(form, state="readonly", width=46)
        self.cb_venda.grid(row=0, column=1, padx=12)
        ttk.Button(form, text="Calcular total", style="Acao.TButton",
                   command=self.calcular_total).grid(row=0, column=2)

        self.lbl_total_info = ttk.Label(aba, text="Escolha uma venda para ver o total.",
                                        style="Info.TLabel")
        self.lbl_total_info.pack(pady=(50, 6))
        self.lbl_total = ttk.Label(aba, text="R$ 0,00", style="Total.TLabel")
        self.lbl_total.pack()

    @seguro
    def calcular_total(self):
        if not self.cb_venda.get():
            messagebox.showwarning("Atenção", "Escolha uma venda.")
            return
        venda_id = self.mapa_vendas[self.cb_venda.get()]
        total = executar("SELECT fn_calcular_total_venda(%s)", (venda_id,), fetch=True)[0][0]
        self.lbl_total.config(text=brl(total))
        self.lbl_total_info.config(text=f"Total da venda #{venda_id} (com desconto aplicado)")
        self.set_status(f"Total da venda #{venda_id} calculado pela function.")

    # ------------------------------------------------------------ recarrega dados
    @seguro
    def atualizar(self):
        clientes = executar("SELECT id, nome, email FROM clientes ORDER BY id", fetch=True)
        preencher(self.tree_cli, clientes)

        produtos = executar("SELECT id, nome, preco, estoque FROM produtos ORDER BY id", fetch=True)
        preencher(self.tree_prod,
                  [(p[0], p[1], brl(p[2]), p[3]) for p in produtos],
                  destaque=[p[3] <= 5 for p in produtos])

        relatorio = executar("SELECT * FROM vw_relatorio_vendas ORDER BY venda_id DESC", fetch=True)
        preencher(self.tree_rel,
                  [(v[0], v[1], f"{v[2]:%d/%m/%Y %H:%M}",
                    v[3], brl(v[4]), f"{v[5]}%") for v in relatorio])

        self.mapa_clientes = {f"{c[0]} - {c[1]}": c[0] for c in clientes}
        self.mapa_produtos = {f"{p[0]} - {p[1]} ({brl(p[2])})": p[0] for p in produtos}
        self.mapa_vendas = {f"#{v[0]} - {v[1]}": v[0] for v in relatorio}
        self.estoques = {p[0]: p[3] for p in produtos}
        self.precos = {p[0]: p[2] for p in produtos}
        self.nomes = {p[0]: p[1] for p in produtos}
        carregar_combo(self.cb_cliente, self.mapa_clientes)
        carregar_combo(self.cb_produto, self.mapa_produtos)
        carregar_combo(self.cb_venda, self.mapa_vendas)
        self._mostrar_estoque()
        self._renderizar_carrinho()


def main():
    print("Conectando ao banco...")
    try:
        conectar().close()
    except Exception as e:
        print("ERRO DE CONEXAO:", e)
        raiz = tk.Tk()
        raiz.withdraw()
        raiz.attributes("-topmost", True)
        messagebox.showerror("Erro de conexão",
                             "Não foi possível conectar ao PostgreSQL.\n\n"
                             f"{str(e).strip()[:300]}")
        raiz.destroy()
        return

    print("Conexão OK. Abrindo a janela...")
    app = App()
    app.lift()
    app.attributes("-topmost", True)
    app.after(800, lambda: app.attributes("-topmost", False))
    app.focus_force()
    app.mainloop()


if __name__ == "__main__":
    main()
