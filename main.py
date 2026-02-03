from src.database import connect_db, create_structure, seed_root
from src.brain import add_synapse, get_fractal_view, expand_knowledge, get_network_stats

def run():
    
    conn = connect_db()
    if not conn:
        return
        
    create_structure(conn)
    seed_root(conn)
    
   
    eixos_principais = ["Data Engineering", "Business Intelligence", "Machine Learning"]
    expand_knowledge(conn, 1, eixos_principais)
    
   
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM synapses WHERE content = 'Data Engineering' LIMIT 1")
    result = cursor.fetchone()
    
    if result:
        de_id = result[0]
        ferramentas_de = ["SQL Server", "Python ETL", "Airflow", "Spark"]
        expand_knowledge(conn, de_id, ferramentas_de)

    
    get_fractal_view(conn)
    get_network_stats(conn)
    
    
    conn.close()
    print("--- Processamento Bio-Fractal Concluido ---")

if __name__ == "__main__":
    run()