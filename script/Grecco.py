import PyPDF2
import re
import pandas as pd
import os
from datetime import datetime

class Grecco():
    def __init__(self,caminho_pdf):

        self.__caminho_pdf = caminho_pdf
        # 1. Expressões regulares atualizadas
        self.__regex_cnpj = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}' # Delimitador de cada registro
        self.__regex_rubrica = r'\b\d{5}\b'                    # Ex: 34116
        
        # ATUALIZADO: Aceita letras e números em qualquer posição (Banco/Agência/Conta)
        self.__regex_banco = r'[A-Za-z0-9]+/[A-Za-z0-9]+/[A-Za-z0-9]+' 
        
        self.__regex_valor = r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b'  # Ex: 1.034.782,91

        self.__dados_extraidos = []

        self.__timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.__nome_arquivo = f"Resultado_conferencia_GRECCO_{self.__timestamp}.xlsx"
        self.__EXIT_PATH = os.path.join(os.path.expanduser('~'), 'Downloads', self.__nome_arquivo)

    def __extrair_dados(self):
        with open(self.__caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            texto_completo = ""
            for pagina in leitor.pages:
                texto_completo += pagina.extract_text() + "\n"

        # 3. Quebrar o texto em blocos (cada bloco é uma consignatária, separada pelo CNPJ)
        blocos = re.split(f'(?={self.__regex_cnpj})', texto_completo)

        # 4. Processar cada bloco individualmente
        for bloco in blocos:
            if not re.search(self.__regex_cnpj, bloco):
                continue # Pula blocos vazios ou cabeçalhos

            rubricas = re.findall(self.__regex_rubrica, bloco)
            bancos = re.findall(self.__regex_banco, bloco)
            valores = re.findall(self.__regex_valor, bloco)

            # Se encontrou o código da rubrica e algum valor, podemos extrair
            if rubricas and valores:
                codigo_rubrica = rubricas[0]
                
                # Pega o primeiro banco encontrado ou define como 'Não informado'
                banco_ag_cc = bancos[0] if bancos else "Não informado"
                
                # O Valor Líquido costuma ser o último valor monetário do bloco
                valor_liquido = valores[-1] 

                self.__dados_extraidos.append({
                    'Código Rubrica': codigo_rubrica,
                    'Banco/Agência/C.Corrente': banco_ag_cc,
                    'Valor Líquido': valor_liquido
                })

        # 5. Salvar os resultados no Excel usando Pandas
        if self.__dados_extraidos:
            df = pd.DataFrame(self.__dados_extraidos)
            df.to_excel(self.__EXIT_PATH, index=False)
            print(f"Sucesso! {len(self.__dados_extraidos)} registros extraídos e salvos em '{self.__EXIT_PATH}'.")
        else:
            print("Nenhum dado correspondente aos padrões foi encontrado.")

    def iniciar(self):
        self.__extrair_dados()