import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import shutil
import subprocess
import threading
import time

class Screen_xml:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Gerador XML")
        self.janela.geometry("400x300")
        self.janela.resizable('false','false')

        # Criando um frame invisível no centro para alinhar os widgets
        self.__frame_central = tk.Frame(self.janela)
        self.__frame_central.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza

        # Botões dentro do frame centralizado
        self.__upload_base_button = tk.Button(self.__frame_central, text='Upload dados', command=lambda: self.__upload_file('Dados'))
        self.__upload_base_button.pack(pady=10)

        self.__analyze_button = tk.Button(self.__frame_central, text='Resultado', command=self.__run_analyzer)
        self.__analyze_button.pack(pady=10)

        # Barra de progresso também dentro do frame
        self.__barra_progresso = ttk.Progressbar(self.__frame_central, orient="horizontal", length=300, mode="determinate")
        self.__barra_progresso.pack(pady=20)

        self.janela.protocol("WM_DELETE_WINDOW", self.__on_close)
    
        self.janela.mainloop()
    
    def __upload_file(self, upload_type):
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f'Arquivo selecionado para {upload_type}: {file_path}')
            
            destination_directory = './data'
            
            if upload_type == 'Dados':
                new_file_name = 'data.xlsx'
            else:
                new_file_name = file_path.split("/")[-1]

            destination_path = f"{destination_directory}/{new_file_name}"
            shutil.copy(file_path, destination_path)
            print(f'Arquivo copiado e renomeado para: {destination_path}')
    
    def __run_analyzer(self):
        from script.Gerador_xml import Gerador_xml
        try:
            gerador_xml = Gerador_xml()
            self.__start_task(gerador_xml.iniciar())
            messagebox.showinfo('Sucesso', 'Verifique sua pasta de Downloads')
            print('XML gerado com sucesso.')
        except subprocess.CalledProcessError:
            messagebox.showerror('Erro', 'Erro ao gerar XML.')
    
    def __start_task(self, func):
        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start()

        progress = 0
        while progress < 100:
            progress += 10
            self.__barra_progresso['value'] = progress
            self.janela.update_idletasks()
            time.sleep(1)
    
    def __on_close(self):
        self.janela.destroy()
        from visual.Home import Home
        Home()
