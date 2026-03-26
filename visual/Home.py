import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Toplevel
import os

from gerenciador_caminhos.gerenciador_caminhos import GerenciadorCaminhos
from visual.Grecco_tela import Grecco_tela

class Home:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Contabilidade")
        self.__largura = self.__root.winfo_screenwidth()
        self.__altura = self.__root.winfo_screenheight()
        self.__root.geometry(f'{self.__largura}x{self.__altura}')

        self.__canvas = tk.Canvas(self.__root, width=self.__largura, height=self.__altura)
        self.__canvas.pack(fill="both", expand=True)

        self.__frame_botoes = tk.Frame(self.__root, bg="gray")
        self.__frame_botoes.place(relx=0.5, rely=0.0, anchor="n")

        caminho_relativo = os.path.join("data", "bitcoin.jpg")
        caminho_imagem = GerenciadorCaminhos.obter_caminho_recurso(caminho_relativo)

        self.__imagem_original = Image.open(caminho_imagem)
        self.__imagem_tk = None

        self.__bg_id = self.__canvas.create_image(0, 0, anchor="nw", image=None)

        self.__redimensionar_imagem()

        botoes = [
            ('Gerador GRECCO', 'Gerador GRECCO')
        ]

        for texto in botoes:
            tk.Button(self.__frame_botoes, text=texto[0], command=lambda t=texto[1]: self.__abrir_tela(titulo=t)).pack(side=tk.LEFT, padx=10, pady=5)

        self.__root.mainloop()

    def __redimensionar_imagem(self):
        imagem_resized = self.__imagem_original.resize((self.__largura, self.__altura))
        self.__imagem_tk = ImageTk.PhotoImage(imagem_resized)
        self.__canvas.itemconfig(self.__bg_id, image=self.__imagem_tk)

    def __abrir_tela(self, titulo):
        nova_tela = Toplevel(self.__root)
        nova_tela.geometry(f'{850}x{600}')

        nova_tela.title(titulo)

        if titulo == 'Gerador GRECCO':
            Grecco_tela(nova_tela)