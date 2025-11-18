#Importa a biblioteca Pandas(pd).O Pandas é usado para criar a tabela (DataFrame)
import pandas as pd

#Definição de Dados(cria um discionário Python onde cada chave vira o nome de uma coluna no DataFrame)
dados = {
    'Matrícula': [101,102,103,104,105],
    'CPF': [11122233344,22233344455,33344455566,44455566677,55566677788],
    'Nome_Aluno': ['Ana Souza','Beto Lima','Ciro Neto','Rodrigo Parreira','Letícia Duarte'],
    'DT_Nascimento': ['2005-01-10','2004-05-15','2005-08-20','2004-04-04','2005-10-09'],
    'Nome_Responsável': ['Clara Souza','Paulo Lima','Eva Costa','Ana Parreira','Cristian Duarte']
}

#Criação do DataFrame(serve para converter o discionário na tabela estruturada do Pandas)
df = pd.DataFrame(dados)

#Configuração e Salvamento do Arquivo(define o nome do arquivo que será criado)
csv_file_path = 'Relatório Individual - Boletim Escolar.csv'

# Salva a tabela 'df' no arquivo CSV,sem incluir os números de índice 
df.to_csv(csv_file_path, index=False)

print("-" * 80)# Imprima no Terminal a string de um hífen repetida 80 vezes
# Visualização e Feedback no Terminal
print(f'Arquivo "{csv_file_path}" criado com sucesso')


#Imprime o conteúdo completo do DataFrame no Terminal para visualização
print("\n--- Dados do Aluno---")
print(df)