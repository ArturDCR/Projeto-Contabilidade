import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import threading

from script.Grecco import Grecco

class Grecco_tela():
    def __init__(self, root):
        self.__frame_botoes = tk.Frame(root)
        self.__frame_botoes.pack(pady=20)

        self.__caminho_grecco = None

        self.__upload_grecco_button = tk.Button(self.__frame_botoes, text='Upload Grecco', command=lambda: self.__upload_file_conferencia_grecco('Grecco'))
        self.__upload_grecco_button.pack(pady=10)

        self.__analyze_button = tk.Button(self.__frame_botoes, text='Resultado da Conferência', command=self.__run_analyzer_conferencia_grecco)
        self.__analyze_button.pack(pady=10)

        self.__barra_progresso = ttk.Progressbar(self.__frame_botoes, orient="horizontal", length=300, mode="determinate")
        self.__barra_progresso.pack(pady=20)
    
    def __upload_file_conferencia_grecco(self, upload_type):
        file_path = filedialog.askopenfilename(
            title=f"Selecione a planilha {upload_type}",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            if upload_type == 'Grecco':
                self.__caminho_grecco = file_path
                
            messagebox.showinfo('Sucesso', f'Arquivo {upload_type} carregado:\n{os.path.basename(file_path)}')
    
    def __run_analyzer_conferencia_grecco(self):
        if not self.__caminho_grecco:
            messagebox.showwarning('Aviso', 'Por favor, faça o Upload da planilha Grecco antes de gerar o resultado.')
            return
        
        def tarefa_em_background():
            try:
                grecco = Grecco(self.__caminho_grecco)
                grecco.iniciar()
                messagebox.showinfo('Sucesso', 'Conferência concluída! Verifique sua pasta de Downloads.')
            except Exception as e:
                messagebox.showerror('Erro', f'Ocorreu um erro durante a análise: {e}')
            finally:
                self.__barra_progresso['value'] = 0

        self.__start_task(tarefa_em_background)
    
    def __start_task(self, func):
        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start()

        self.__barra_progresso['value'] = 0
        def atualizar_barra():
            if thread.is_alive():
                if self.__barra_progresso['value'] < 90:
                    self.__barra_progresso['value'] += 5
                self.__frame_botoes.after(500, atualizar_barra)
            else:
                self.__barra_progresso['value'] = 100

        atualizar_barra()