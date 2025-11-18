#Importa a biblioteca Pandas(pd).O Pandas é usado para criar a tabela (DataFrame)
import pandas as pd

#Definição de Dados(cria um discionário Python onde cada chave vira o nome de uma coluna no DataFrame)
dados = {
    'Matrícula': [101,102,103,104,105],
    'Bimestre_1': [8.0,4.0,9.5,10,7],
    'Bimestre_2': [9.0,5.0,8.0,9,7],
    'Bimestre_3': [7.0,6.0,8.5,8.0,7],
    'Bimestre_4': [0.0,0.0,0.0,0.0,0.0],
    'Média':[0.0,0.0,0.0,0.0,0.0],
    'Situação':[0.0,0.0,0.0,0.0,0.0],
}

#Criação do DataFrame(serve para converter o discionário na tabela estruturada do Pandas)
df = pd.DataFrame(dados)

#Configuração e Salvamento do Arquivo(define o nome do arquivo que será criado)
csv_file_path = 'notas.csv'

# Salva a tabela 'df' no arquivo CSV,sem incluir os números de índice 
df.to_csv(csv_file_path, index=False)

# Visualização e Feedback no Terminal
print(f'Arquivo "{csv_file_path}" criado com sucesso"')

#Imprime o conteúdo completo do DataFrame no Terminal para visualização
print("\n--- Tabela de Alunos (DataFrame)---")
print(df)