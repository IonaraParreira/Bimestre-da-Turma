import pandas as pd
import numpy as np

# --- 1 Leitura dos Arquivos CSV ---

# O DataFrame df_notas contém as notas b1, b2, b3, b4, média, situação
df_notas = pd.read_csv('Detalhes-da-Turma/notas.csv')

# df_alunos contém os dados cadastrais (Nome, CPF, etc)
df_alunos = pd.read_csv('Detalhes-da-Turma/alunos.csv')

# Unir as tabelas para a exibição inicial
df_geral = pd.merge(df_notas, df_alunos[['Matrícula', 'Nome_Aluno']], on='Matrícula', how='left')

print("--- Dados Carregados ---")
print(df_geral[['Matrícula', 'Nome_Aluno', 'Bimestre_1', 'Bimestre_2', 'Bimestre_3']].head())
print("-" * 80)

def calcular_media_e_situação(df):
    """
    Calcula a Média e a Situação Final de todos os alunos no DataFrame.
    """
    # 1 Calcular a Média
    colunas_notas = ['Bimestre_1', 'Bimestre_2', 'Bimestre_3', 'Bimestre_4']
    
    # Certifica-se de que a coluna Bimestre_4 existe antes de calcular
    if 'Bimestre_4' not in df.columns:
        df['Bimestre_4'] = np.nan
        
    df['Média'] = df[colunas_notas].mean(axis=1).round(2)

    # 2 Defini a Situação
    condicoes = [
        (df['Média'] >= 7.0),
        (df['Média'] >= 5.0) & (df['Média'] < 7.0),
        (df['Média'] < 5.0)
    ]
    
    resultados = ['APROVADO', 'RECUPERAÇÃO', 'REPROVADO']

    df['Situação'] = np.select(condicoes, resultados, default='N/A')
    return df

def inserir_nota_4bimestre_aluno(df_notas):
    """ Pede a matrícula e a nota do 4° Bimestre para um aluno específico."""
    
    # 1. Pede a matrícula do aluno
    while True:
        try:
            # Captura a matrícula do aluno para ser usada no filtro e retorno
            mat_input = input("\nPor favor, insira a Matrícula do aluno para lançar a nota do 4° Bimestre (ou 'sair'): ")
            
            # Condição de SAÍDA do loop principal (if 'sair': break)
            if mat_input.lower() == 'sair':
                return df_notas, None # Retorna None para sinalizar a saída do loop

            mat_input = int(mat_input) # Tenta converter para inteiro
            
            # Tenta encontrar o índice da Linha correspondente à matrícula
            indice_aluno = df_notas[df_notas['Matrícula'] == mat_input].index
            
            if not indice_aluno.empty:
                break
            else:
                print(f"Erro: Matrícula {mat_input} não encontrada.")
        except ValueError:
            print("Entrada inválida. Digite apenas números ou 'sair'.")

    # 2. Pede a nota do 4° Bimestre
    while True:
        try:
            nota_input = float(input(f"Insira a nota do 4° Bimestre para o aluno {mat_input}: "))
            if 0.0 <= nota_input <= 10.0: # Validação básica da nota
                break
            else:
                print("Erro: A nota deve estar entre 0.0 e 10.0.")
        except ValueError:
            print("Entrada inválida. Digite um número válido para a nota.")
    
    # 3. Atualiza o DataFrame com a nova nota
    df_notas.loc[indice_aluno[0], 'Bimestre_4'] = nota_input

    print("-" * 30)
    print(f"Nota {nota_input} lançada para o aluno Matrícula {mat_input}.")
    print("-" * 30)
    
    # Retorna o DataFrame atualizado e a matrícula do aluno editado
    return df_notas, mat_input

def exibir_relatorio_individual(df_relatorio_completo, matricula):
    """ Exibe o 'POP-UP' formatado para o aluno recém-atualizado, ou um aluno específico. """
    
    # Tenta encontrar o índice da Linha correspondente à matrícula
    aluno_df_series = df_relatorio_completo[df_relatorio_completo['Matrícula'] == matricula]
    
    if aluno_df_series.empty:
        print(f"\nErro: Matrícula {matricula} não encontrada no relatório.")
        return
        
    aluno_df = aluno_df_series.iloc[0]
    
    print("\n" + "=" * 40)
    print("RELATÓRIO INDIVIDUAL - BOLETIM ESCOLAR")
    print("=" * 40)
    print("DADOS DO ALUNO:")
    print(f"  Matrícula: {aluno_df['Matrícula']}")
    print(f"  Nome: {aluno_df['Nome_Aluno']}")
    print(f"  Responsável: {aluno_df['Nome_Responsável']}")
    print("-" * 40)
    print("NOTAS POR BIMESTRE")
    print("-" * 40)
    print(f"  1° Bimestre: {aluno_df['Bimestre_1']:.2f}\n"
      f"  2° Bimestre: {aluno_df['Bimestre_2']:.2f}\n"
      f"  3° Bimestre: {aluno_df['Bimestre_3']:.2f}\n"
      f"  4° Bimestre: {aluno_df['Bimestre_4']:.2f}")
    print("-" * 40)
    print("RESULTADO FINAL")
    print("-" * 40)

    print(f"  MÉDIA FINAL: {aluno_df['Média']:.2f}")
    print(f"  SITUAÇÃO: {aluno_df['Situação']}")
    print("=" * 40 + "\n")

# ---- 3 Fluxo Principal do Programa ----

df_trabalho = df_notas.copy() # Cria uma cópia para trabalhar dentro do loop

# LOOP INFINITO: Repete o processo de inserção e recálculo
while True:
    # 1. Tenta inserir a nota. Retorna o DataFrame e a matrícula do aluno editado
    df_notas_atualizado, mat_aluno_editado = inserir_nota_4bimestre_aluno(df_trabalho)
    
    # Condição de SAÍDA: Se a matrícula for None (usuário digitou 'sair'), quebra o loop
    if mat_aluno_editado is None:
        print("\nProcesso de inserção de notas finalizado.")
        break
        
    # Atualiza o DataFrame de trabalho
    df_trabalho = df_notas_atualizado
    
    # 2. Recalcular a Média e a Situação de TODOS os alunos (incluindo o que acabou de ser editado)
    df_final = calcular_media_e_situação(df_trabalho)

    # 3. Geração do Relatório Completo (Para exibição)
    df_relatorio_completo = pd.merge(
        df_final, 
        df_alunos[['Matrícula','Nome_Aluno','Nome_Responsável']],
        on='Matrícula',
        how='left'
    )
    
    # 4. EXIBIÇÃO DO RELATÓRIO COMPLETO DA TURMA (PRIORIDADE DENTRO DO LOOP)
    colunas_relatorio_completo = [
        'Matrícula', 'Nome_Aluno', 'Bimestre_1', 'Bimestre_2', 'Bimestre_3', 'Bimestre_4', 'Média', 'Situação', 'Nome_Responsável'
    ]
    
    print("\n" + "=" * 80)
    print(f"RELATÓRIO ATUALIZADO (APÓS EDIÇÃO DA MATRÍCULA {mat_aluno_editado})")
    print("=" * 80)
    print(df_relatorio_completo[colunas_relatorio_completo])
    
    # 5. PERGUNTA PARA EXIBIÇÃO DO POP-UP INDIVIDUAL
    opcao_pop = input(f"\nDeseja gerar o POP-UP individual para o aluno {mat_aluno_editado}? (s/n): ").lower()
    
    if opcao_pop == 's' or opcao_pop == 'sim':
        exibir_relatorio_individual(df_relatorio_completo, mat_aluno_editado)

    # 6. Opcional: Salvar o resultado final no CSV
    df_final.to_csv('notas.csv', index=False)
    
# --- EXIBIÇÃO FINAL DE TODOS OS RELATÓRIOS APÓS O FIM DO LOOP ---

# O df_relatorio_completo da última iteração já contém os dados finais
df_relatorio_completo_final = df_relatorio_completo # Renomeado para clareza

# 7. EXIBIÇÃO FINAL DO RELATÓRIO DA TURMA (Mensagem de Fim)
print("\n" + "=" * 80)
print("VISUALIZAÇÃO DO BOLETIM APÓS A ÚLTIMA ATUALIZAÇÃO")
print("=" * 80)
print(df_relatorio_completo_final[colunas_relatorio_completo])

# 8. EXIBIÇÃO OPCIONAL DO RELATÓRIO INDIVIDUAL (OPÇÃO FINAL)
while True:
    opcao_relatorio = input("\nDeseja gerar um Relatório Individual final? (Digite a Matrícula ou 'não'): ").lower()
    
    if opcao_relatorio == 'não' or opcao_relatorio == 'nao':
        break
        
    try:
        mat_final = int(opcao_relatorio)
        # Usa o DataFrame final que acabou de ser gerado
        exibir_relatorio_individual(df_relatorio_completo_final, mat_final)
    except ValueError:
        print("Entrada inválida. Por favor, digite a Matrícula ou 'não'.")

print("\n" + "~" * 80)
print("PROGRAMA FINALIZADO. O arquivo 'notas.csv' foi atualizado.")
print("~" * 80)
