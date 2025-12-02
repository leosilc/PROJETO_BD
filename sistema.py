import oracledb
import unicodedata

# Função auxiliar para remover acentos, espaços e deixar toda a string em caps lock
def limpar(texto):
    if not texto: 
        return ""
    # Separa o acento da letra
    nfkd = unicodedata.normalize('NFKD', texto) 
    # Descarta o acento, passa para maiúsculo e tira espaços
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).upper().strip()

# Função de conexão com o banco de dados
def conectar():
    try:
        user = "SEU_LOGIN"
        pwd = "SUA_SENHA" 
        dsn = "NOME_HOST/NOME_SERVICO" 
        connection = oracledb.connect(user=user, password=pwd, dsn=dsn)
        return connection
    except oracledb.Error as e:
        print(f"Erro ao conectar: {e}")
        return None

# Função de busca
def consultar_hospitais(conn):
    cursor = conn.cursor()
    try:   
        print("\n--- Consulta de Hospitais ---")
        cidade = limpar(input("Digite a cidade para consultar hospitais: "))

        consulta = """
        SELECT H.NOME, COUNT(T.ID_ORGAO) AS QTD, H.CIDADE
        FROM HOSPITAL H
        LEFT JOIN TRANSPLANTE T ON H.CNPJ = T.HOSPITAL
        WHERE H.CIDADE = :cidade
        GROUP BY H.NOME, H.CIDADE
        ORDER BY QTD DESC
        """
        cursor.execute(consulta, cidade=cidade)
        hospitais = cursor.fetchall()

        if hospitais:
            for hospital in hospitais:
                print(f"Nome: {hospital[0]} | Quantidade de transplantes: {hospital[1]} | Cidade: {hospital[2]}")
        else:
            print(f"Nenhum hospital encontrado na cidade de {cidade}.")
    except oracledb.Error as e:
        print(f"Erro ao consultar hospitais: {e}")
    finally:
        cursor.close()

# Função de inserção
def cadastrar_veiculo(conn):
    cursor = conn.cursor()
    try:
        print("\n--- Cadastro de Veículo ---")
        placa = limpar(input("Digite a placa do veículo: ")).replace("-", "") 
        # remove o hífen caso o usuário insira
        if not placa:
            print("Erro: A placa não pode ser vazia.")
            return
        modelo = limpar(input("Digite o modelo do veículo: "))
        if not modelo:
            print("Erro: O modelo não pode ser vazio.")
            return
        meio = limpar(input("Digite o meio de transporte (TERRESTRE/AEREO): "))
        if meio not in ['TERRESTRE', 'AEREO']:
            print("Erro: Meio de transporte inválido. Use 'TERRESTRE' ou 'AEREO'.")
            return
        
        insercao = """
        INSERT INTO VEICULO (PLACA, MODELO, MEIO_TRANSPORTE)
        VALUES (:1, :2, :3)
        """ # inserir dessa forma protege de SQL Injection

        cursor.execute(insercao, (placa, modelo, meio))

        # Confirma a transação 
        conn.commit()
        print(f"Sucesso! Veículo {placa} cadastrado.")

    except oracledb.IntegrityError as e:
        # Se der erro (ex: placa duplicada), faz ROLLBACK
        conn.rollback()
        error_obj, = e.args
        if error_obj.code == 1: # Código ORA-00001 (Violação de chave única)
            print(f"Erro: Já existe um veículo com a placa '{placa}'.")
        else:
            print(f"Erro de integridade: {error_obj.message}")
            
    finally:
        cursor.close()
    
def main():
    conn = conectar()
    if conn:
        print("Conexão bem-sucedida!")

        while True:
            print("\n=== SISTEMA DE TRANSPLANTES ===")
            print("1. Cadastrar Veículo")
            print("2. Relatório de Hospitais por Cidade")
            print("0. Sair")
            opcao = input("Escolha: ")

            if opcao == '1':
                cadastrar_veiculo(conn)
            elif opcao == '2':
                consultar_hospitais(conn)
            elif opcao == '0':
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

        conn.close()    
    else:
        print("Falha na conexão.")
    
if __name__ == "__main__":
    main()