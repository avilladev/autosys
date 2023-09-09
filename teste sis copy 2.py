import tkinter as tk
from tkinter import ttk
from openpyxl import Workbook
from tkinter import messagebox
from ttkthemes import ThemedStyle
from tkinter.simpledialog import askstring
from datetime import datetime
from PIL import Image, ImageTk  # Para trabalhar com imagens e imagens em GUIs

def adicionar_dados():
    altura = entry_altura.get()
    largura = entry_largura.get()
    cod_material = entry_cod_material.get()
    item = entry_item.get()
    obs = entry_obs.get()

    # Verifica se todos os campos estão preenchidos
    if altura and largura and cod_material and item and obs:
        numero_ordinal = len(tree.get_children()) + 1  # Número ordinal com base na posição da linha
        tree.insert("", "end", values=(numero_ordinal, altura, largura, cod_material, item, obs))
        # Limpa as entradas após adicionar os dados à tabela
        entry_altura.delete(0, "end")
        entry_largura.delete(0, "end")
        entry_cod_material.delete(0, "end")
        entry_item.delete(0, "end")
        entry_obs.delete(0, "end")
        # Mova o foco para o primeiro campo na nova linha
        entry_altura.focus()
    else:
        messagebox.showerror("Erro", "Preencha todos os campos antes de adicionar.")

def salvar_xlsx():
    global titulo_planilha  # Declare a variável global para acessá-la

    # Se não houver título definido, solicita ao usuário que insira um título
    if not titulo_planilha:
        titulo_planilha = askstring("Título da Planilha", "Digite um título para a planilha:")
        if not titulo_planilha:
            return

    nome_arquivo = f"{titulo_planilha}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Número", "Altura", "Largura", "Cod. Material", "Item", "Obs"])

    for row in tree.get_children():
        item = tree.item(row)
        valores = item['values']
        ws.append(valores)

    wb.save(nome_arquivo)
    messagebox.showinfo("Salvar", f"Tabela salva em {nome_arquivo}")

    # Reiniciar o programa após salvar
    root.quit()
    root.destroy()
    iniciar_programa()

def solicitar_titulo():
    global titulo_planilha
    titulo_planilha = askstring("Título da Planilha", "Digite um título para a planilha:")

def iniciar_programa():
    global root
    # Iniciar a aplicação
    root = tk.Tk()
    root.title("Tabela com XLSX")

    # Configurar as colunas para redimensionar
    for i in range(7):
        root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(2, weight=1)

    # Chamar a função para solicitar o título ao iniciar a aplicação
    solicitar_titulo()

    # Aplicar um tema
    style = ThemedStyle(root)
    style.set_theme("plastik")  # Você pode experimentar outros temas disponíveis

    # Definir cores personalizadas
    root.configure(bg='#333333')  # Fundo cinza escuro
    style.configure("TLabel", foreground='lightblue', background='#333333')  # Letras azuis claras para rótulos
    style.configure("TButton", foreground='#333333', background='gray')  # Botões cinza
    style.configure("Treeview", fieldbackground='#333333', background='#333333', foreground='lightblue')  # Treeview

    # Frames para organizar os widgets
    entries_frame = ttk.Frame(root)
    entries_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    tree_frame = ttk.Frame(root)
    tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Rótulos acima dos campos de preenchimento
    rótulos = ["Número", "Altura", "Largura", "Cod. Material", "Item", "Obs"]
    for i, rótulo in enumerate(rótulos):
        ttk.Label(entries_frame, text=rótulo).grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

    # Entradas de texto para preenchimento das colunas
    global entry_altura, entry_largura, entry_cod_material, entry_item, entry_obs
    entry_altura = ttk.Entry(entries_frame, width=10)
    entry_largura = ttk.Entry(entries_frame, width=10)
    entry_cod_material = ttk.Entry(entries_frame, width=10)
    entry_item = ttk.Entry(entries_frame, width=10)
    entry_obs = ttk.Entry(entries_frame, width=10)

    entry_altura.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    entry_largura.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    entry_cod_material.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
    entry_item.grid(row=1, column=4, padx=5, pady=5, sticky="ew")
    entry_obs.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

    # Botão para adicionar dados à tabela
    btn_adicionar = ttk.Button(entries_frame, text="Adicionar", command=adicionar_dados)
    btn_adicionar.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

    # Criar a árvore para exibir a tabela
    global tree
    tree = ttk.Treeview(tree_frame, columns=("Número", "Altura", "Largura", "CodMaterial", "Item", "Obs"))
    tree.heading("#1", text="Número")
    tree.heading("#2", text="Altura")
    tree.heading("#3", text="Largura")
    tree.heading("#4", text="Cod. Material")
    tree.heading("#5", text="Item")
    tree.heading("#6", text="Obs")

    # Configurar as colunas para redimensionar
    for i in range(1, 7):
        tree.column(f"#{i}", width=100, anchor="center")  # Define uma largura inicial para cada coluna

    tree.pack(expand=True, fill="both")

    # Botão para salvar a tabela em XLSX
    btn_salvar = ttk.Button(root, text="Salvar", command=salvar_xlsx)
    btn_salvar.grid(row=3, column=0, padx=10, pady=10, sticky="we")

    root.mainloop()

iniciar_programa()
