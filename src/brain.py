import sqlite3
import logging

def add_synapse(conn, content, parent_id):
    """Adiciona uma nova ramificacao a partir de um pai."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT depth FROM synapses WHERE id = ?", (parent_id,))
        parent_depth = cursor.fetchone()[0]
        
        new_depth = parent_depth + 1
        query = "INSERT INTO synapses (content, parent_id, depth) VALUES (?, ?, ?)"
        cursor.execute(query, (content, parent_id, new_depth))
        conn.commit()
        logging.info(f"Nova sinapse: {content} (Profundidade: {new_depth})")
    except Exception as e:
        logging.error(f"Erro ao ramificar: {e}")

def get_fractal_view(conn):
    """Recupera e exibe a estrutura hierarquica no terminal."""
    cursor = conn.cursor()
    
    cursor.execute("SELECT depth, content, id FROM synapses ORDER BY depth, parent_id")
    rows = cursor.fetchall()
    
    print("\n--- VISUALIZACAO DA REDE BIO-FRACTAL ---")
    for depth, content, node_id in rows:
        indent = "  " * depth  
        prefix = "|--" if depth > 0 else "ROOT:"
        print(f"{indent}{prefix} {content} (ID: {node_id})")
    print("----------------------------------------\n")

def expand_knowledge(conn, parent_id, concepts_list):
    """Expande a rede a partir de uma lista de conceitos para um pai especifico."""
    for concept in concepts_list:
      
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM synapses WHERE content = ? AND parent_id = ?", (concept, parent_id))
        if not cursor.fetchone():
            add_synapse(conn, concept, parent_id)

def get_network_stats(conn):
    """Gera metricas de agregacao sobre a rede (Visao BI)."""
    cursor = conn.cursor()
    
    
    query = """
    SELECT depth, COUNT(*) as total 
    FROM synapses 
    GROUP BY depth 
    ORDER BY depth
    """
    
    try:
        cursor.execute(query)
        stats = cursor.fetchall()
        
        print("\n=== DASHBOARD DA REDE (ESTATISTICAS) ===")
        print(f"{'CAMADA':<12} | {'QTD NEURONIOS':<15}")
        print("-" * 30)
        
        total_geral = 0
        for depth, count in stats:
            print(f"Nivel {depth:<8} | {count:<15}")
            total_geral += count
            
        print("-" * 30)
        print(f"TOTAL DE CONHECIMENTO: {total_geral} sinapses\n")
        
    except Exception as e:
        logging.error(f"Erro ao gerar stats: {e}")