import logging

def add_synapse(conn, content, parent_id=None):
    cursor = conn.cursor()
    
    # Logica de Profundidade (Fractal)
    depth = 0
    if parent_id:
        cursor.execute("SELECT depth FROM synapses WHERE id = ?", (parent_id,))
        result = cursor.fetchone()
        if result:
            depth = result[0] + 1
        else:
            logging.warning(f"Pai ID {parent_id} nao encontrado. Criando como Raiz.")
            parent_id = None # Reseta para ser raiz se o ID nao existir

    query = "INSERT INTO synapses (content, parent_id, depth) VALUES (?, ?, ?)"
    try:
        cursor.execute(query, (content, parent_id, depth))
        conn.commit() # Garante que a semente foi plantada
    except Exception as e:
        logging.error(f"Erro ao ramificar: {e}")

def get_fractal_view(conn, parent_id=None, indent=0):
    """Busca recursiva para mostrar a arvore"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM synapses WHERE parent_id IS ? OR (parent_id IS NULL AND ? IS NULL)", (parent_id, parent_id))
    nodes = cursor.fetchall()
    
    for node_id, content in nodes:
        print("  " * indent + f"|-- {content} (ID: {node_id})")
        get_fractal_view(conn, node_id, indent + 1)

def get_network_stats(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT depth, COUNT(*) FROM synapses GROUP BY depth")
    stats = cursor.fetchall()
    
    print("\n=== DASHBOARD DA REDE (ESTATISTICAS) ===")
    print(f"{'CAMADA':<12} | {'QTD NEURONIOS':<15}")
    print("-" * 30)
    for depth, count in stats:
        print(f"Nivel {depth:<8} | {count:<15}")
    
    cursor.execute("SELECT COUNT(*) FROM synapses")
    total = cursor.fetchone()[0]
    print("-" * 30)
    print(f"TOTAL DE CONHECIMENTO: {total} sinapses\n")

def get_density_report(conn):
    """BI: Mostra quais temas sao mais densos (tem mais filhos)"""
    cursor = conn.cursor()
    query = """
    SELECT p.content, COUNT(c.id) as densidade
    FROM synapses p
    JOIN synapses c ON c.parent_id = p.id
    GROUP BY p.id
    ORDER BY densidade DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def delete_synapse(conn, node_id):
    """Remove um neuronio e tenta evitar orfaos (poda)"""
    cursor = conn.cursor()
    try:
        # Primeiro, avisamos que os filhos perderao o pai (opcional: deletar em cascata)
        cursor.execute("DELETE FROM synapses WHERE id = ?", (node_id,))
        conn.commit()
        print(f"Node {node_id} removido da rede.")
    except Exception as e:
        print(f"Erro na poda: {e}")

def search_synapse(conn, term):
    """Busca um neuronio pelo nome e mostra onde ele esta"""
    cursor = conn.cursor()
    query = "SELECT id, content, depth FROM synapses WHERE content LIKE ?"
    cursor.execute(query, (f'%{term}%',))
    results = cursor.fetchall()
    
    if results:
        print(f"\n--- Resultados para '{term}' ---")
        for res in results:
            print(f"ID: {res[0]} | Conteudo: {res[1]} | Camada: {res[2]}")
    else:
        print(f"\nNenhum padrao encontrado para '{term}'.")

def seed_from_file(conn, file_path):
    """
    Le um arquivo texto e insere cada linha como um neuronio raiz.
    Formato esperado: Cada linha um novo conceito.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                content = line.strip()
                if content:
                    add_synapse(conn, content, None) # Insere como raiz por padrao
            print(f"--- Sucesso: {len(lines)} novas sementes plantadas! ---")
    except FileNotFoundError:
        print("Erro: Arquivo nao encontrado.")
    except Exception as e:
        print(f"Erro no processamento: {e}")

import csv

def export_for_bi(conn, filename="data/brain_export.csv"):
    """Gera um CSV para ser lido no Power BI ou Excel"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, parent_id, depth FROM synapses")
    rows = cursor.fetchall()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Conteudo', 'ID_Pai', 'Camada']) # Cabecalho
        writer.writerows(rows)
    print(f"Dados exportados para {filename}. Pronto para o BI!")