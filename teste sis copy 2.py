import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
import threading
import time

class TaskManagerApp:
    def __init__(self, root):
        """
        Inicializa a aplicação.

        Args:
            root (tk.Tk): Instância principal da interface gráfica.
        """
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("1000x600")

        self.task_list = []
        self.create_widgets()
        self.scan_directory()
        self.dark_theme = True  # Flag para controle do tema escuro

    def create_widgets(self):
        """
        Cria os widgets da interface.
        """
        # Aplicar um tema mais escuro em toda a janela
        self.style = ttk.Style()
        self.style.configure("Treeview", background="black", foreground="white")
        self.style.map("Treeview", background=[("selected", "blue")])

        # Botão para alternar o tema
        theme_button = tk.Button(self.root, text="Alternar Tema", command=self.toggle_theme)
        theme_button.place(relx=0.9, rely=0.1, anchor=tk.NE)

        # Caixa de pesquisa
        search_label = tk.Label(self.root, text="Pesquisar:")
        search_label.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        # Frame para a lista de tarefas
        task_frame = ttk.Frame(self.root)
        task_frame.pack(fill=tk.BOTH, expand=True)

        # Lista de tarefas com barras de rolagem
        self.task_tree = ttk.Treeview(
            task_frame,
            columns=("Folder", "File Name", "Status", "Completion Date"),
            show="headings"
        )

        self.task_tree.heading("Folder", text="Pasta Local")
        self.task_tree.heading("File Name", text="Nome do Arquivo")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Completion Date", text="Data de Conclusão")

        self.task_tree.pack(fill=tk.BOTH, expand=True)
        self.task_tree.column("Folder", width=200)
        self.task_tree.column("File Name", width=300)
        self.task_tree.column("Status", width=100)
        self.task_tree.column("Completion Date", width=150)

        self.task_tree.tag_configure("done", background="lightgreen")
        self.task_tree.tag_configure("dark", background="black", foreground="white")

        # Bind de dois cliques para marcar/desmarcar conclusão
        self.task_tree.bind("<Double-1>", self.toggle_done)

        # Iniciar thread de atualização
        self.update_thread = threading.Thread(target=self.periodic_update, daemon=True)
        self.update_thread.start()

    def scan_directory(self):
        """
        Escaneia o diretório em busca de arquivos.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        for root_folder, _, files in os.walk(current_directory):
            for file in files:
                file_path = os.path.join(root_folder, file)
                if file.lower().endswith(".dwg"):
                    file_info = os.stat(file_path)
                    creation_time = datetime.fromtimestamp(file_info.st_ctime)
                    if creation_time >= datetime(2023, 11, 1):
                        self.task_list.append((root_folder, file, creation_time, None, False))

        self.task_list.sort(key=lambda x: x[2], reverse=True)
        self.update_task_list()

    def update_task_list(self):
        """
        Atualiza a lista de tarefas no Treeview.
        """
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        for task in self.task_list:
            self.add_task(task)

    def add_task(self, task):
        """
        Adiciona uma tarefa ao Treeview.

        Args:
            task (tuple): Informações sobre a tarefa.
        """
        folder, task_name, creation_time, completion_date, done = task
        status = "Concluído" if done or completion_date else "Pendente"
        completion_date_str = completion_date.strftime("%Y-%m-%d") if completion_date else ""
        self.task_tree.insert("", "end", values=("", folder, task_name, status, completion_date_str), tags=("done" if done else "dark"))
        self.task_tree.tag_bind(task_name, '<Button-1>', lambda event, name=task_name: self.toggle_done(event, name))

    def toggle_done(self, event, task_name):
        """
        Alterna o status de concluído/pendente com um duplo clique.

        Args:
            event: O evento de clique.
            task_name (str): Nome da tarefa.
        """
        selected_item = self.task_tree.selection()
        if selected_item:
            for task in self.task_list:
                if task[1] == task_name:
                    task_index = self.task_list.index(task)
                    if task[4]:
                        self.task_list[task_index] = (task[0], task[1], task[2], None, False)
                    else:
                        self.task_list[task_index] = (task[0], task[1], task[2], datetime.now(), True)
            self.update_task_list()

    def toggle_theme(self):
        """
        Alterna entre temas claro e escuro.
        """
        if self.dark_theme:
            self.style.configure("Treeview", background="white", foreground="black")
            self.style.map("Treeview", background=[("selected", "blue")])
        else:
            self.style.configure("Treeview", background="black", foreground="white")
            self.style.map("Treeview", background=[("selected", "blue")])
        self.dark_theme = not self.dark_theme

    def periodic_update(self):
        """
        Atualiza a lista de tarefas periodicamente.
        """
        while True:
            self.scan_directory()
            self.root.update()
            time.sleep(3600)  # Aguarda 1 hora

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
