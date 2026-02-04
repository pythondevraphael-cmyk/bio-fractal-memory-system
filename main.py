from src.database import connect_db, create_structure
from src.brain import (
    add_synapse, 
    get_fractal_view, 
    get_network_stats, 
    get_density_report,
    delete_synapse,
    search_synapse,
    seed_from_file,
    export_for_bi
)

def menu():
    print("\n" + "="*30)
    print(" BIO-FRACTAL SYSTEM : MENU ")
    print("="*30)
    print("1. Adicionar Conhecimento (Manual)")
    print("2. Ver Arvore Fractal (Visualizacao)")
    print("3. Dashboard de BI (Estatisticas)")
    print("4. Podar Neuronio (Remover)")
    print("5. Buscar na Mente (Pesquisar)")
    print("6. Alimentacao em Massa (Arquivo .txt)")
    print("7. Exportar para Power BI (CSV)")
    print("0. Sair")
    return input("\nEscolha uma acao: ")

def run():
    conn = connect_db()
    if not conn:
        print("Erro: Nao foi possivel conectar ao banco de dados.")
        return
    
    create_structure(conn)
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            content = input("O que voce aprendeu? ")
            parent_id = input("ID do pai (deixe vazio para ROOT): ")
            parent_id = int(parent_id) if parent_id.isdigit() else None
            add_synapse(conn, content, parent_id)
            print(f"-> '{content}' semeado com sucesso!")
            
        elif opcao == "2":
            print("\n--- MAPA MENTAL FRACTAL ---")
            get_fractal_view(conn)
            
        elif opcao == "3":
            print("\n--- BI: DENSIDADE POR TEMA ---")
            report = get_density_report(conn)
            if report:
                for tema, qtd in report:
                    print(f"Tema: {tema:<20} | Conexoes: {qtd}")
            get_network_stats(conn)
            
        elif opcao == "4":
            node_id = input("ID do neuronio para remover: ")
            if node_id.isdigit():
                delete_synapse(conn, int(node_id))
            else:
                print("Por favor, digite um ID numerico valido.")

        elif opcao == "5":
            termo = input("O que deseja buscar na mente? ")
            search_synapse(conn, termo)

        elif opcao == "6":
            path = input("Digite o caminho do arquivo (ex: estudos.txt): ")
            seed_from_file(conn, path)

        elif opcao == "7":
            export_for_bi(conn)

        elif opcao == "0":
            print("Sincronizando pensamentos... Ate logo!")
            break
            
        else:
            print("Opcao invalida. Tente novamente.")

if __name__ == "__main__":
    run()