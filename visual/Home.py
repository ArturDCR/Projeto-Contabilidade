import tkinter as tk
from PIL import Image, ImageTk

class Home:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Contabilidade")
        self.__largura = self.janela.winfo_screenwidth()
        self.__altura = self.janela.winfo_screenheight()
        self.janela.geometry(f'{self.__largura}x{self.__altura}')

        self.__canvas = tk.Canvas(self.janela, width=self.__largura, height=self.__altura)
        self.__canvas.pack(fill="both", expand=True)

        self.__frame_botoes = tk.Frame(self.janela, bg="gray")
        self.__frame_botoes.place(relx=0.5, rely=0.0, anchor="n")

        self.__imagem_original = Image.open("./data/bitcoin.jpg")
        self.__imagem_tk = None

        self.__bg_id = self.__canvas.create_image(0, 0, anchor="nw", image=None)

        self.__redimensionar_imagem()

        botoes = [
            ('Gerador XML')
        ]

        for texto in botoes:
            tk.Button(self.__frame_botoes, text=texto, command=lambda: self.__abrir_segunda_tela()).pack(side=tk.LEFT, padx=10, pady=5)

        self.janela.mainloop()

    def __abrir_segunda_tela(self):
        self.janela.destroy()  # Fecha a tela atual
        from visual.Screen_xml import Screen_xml # Importa o objeto tela xml
        Screen_xml()  # Abre a nova tela

    def __redimensionar_imagem(self):
        imagem_resized = self.__imagem_original.resize((self.__largura, self.__altura))
        self.__imagem_tk = ImageTk.PhotoImage(imagem_resized)
        self.__canvas.itemconfig(self.__bg_id, image=self.__imagem_tk)