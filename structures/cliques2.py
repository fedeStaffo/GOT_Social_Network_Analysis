import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

def print_clique_analysis(G):
    """
    Finds maximal cliques using Bron-Kerbosch, identifies the largest cliques, 
    and prints their properties.
    """
    massimal_cliques = list(nx.find_cliques(G))
    
    max_clique_size = max(len(clique) for clique in massimal_cliques)
    
    maximal_size_cliques = [clique for clique in massimal_cliques if len(clique) == max_clique_size]
    
    print(f"Total maximal cliques found: {len(massimal_cliques)}")
    print(f"Maximum clique size: {max_clique_size}")
    print(f"Number of cliques with maximal size: {len(maximal_size_cliques)}")
    
    return massimal_cliques, maximal_size_cliques

def plot_cliques(G, cliques, title):
    """
    Plots subgraphs for the given cliques.
    """
    for i, clique in enumerate(cliques, 1):
        subgraph = G.subgraph(clique)
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(subgraph)
        nx.draw(subgraph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_weight='bold')
        edge_labels = {(u, v): G[u][v]["weight"] for u, v in subgraph.edges()}
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=10, font_color='red')
        plt.title(f"{title} {i} (Size: {len(clique)} nodes)")
        plt.show()

def visualize_network_with_maximal_clique_improved(G, maximal_clique):
    """
    Visualizes the entire network with the maximal clique in red.
    
    Args:
        G (networkx.Graph): The full graph.
        maximal_clique (list): List of nodes in the maximal clique.
    """
    plt.figure(figsize=(14, 10))

    pos = nx.kamada_kawai_layout(G)

    nx.draw_networkx_nodes(
        G, pos, node_size=200, node_color="lightgray", alpha=0.6, label="Other nodes"
    )

    nx.draw_networkx_nodes(
        G, pos, nodelist=maximal_clique, node_size=200, node_color="red", label="Maximal clique"
    )

    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color="gray")


    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v) for u in maximal_clique for v in maximal_clique if G.has_edge(u, v)],
        width=2, edge_color="red", alpha=0.8
    )

    nx.draw_networkx_labels(
        G, pos,
        labels={node: node for node in maximal_clique},
        font_size=12, font_color="black", font_weight="bold"
    )

    plt.legend(scatterpoints=1, loc='best')
    plt.title("Network with maximal clique", fontsize=16)
    plt.axis('off')
    plt.show()




if __name__ == "__main__":
    try:
        G = load_graph_from_dataset()

        massimal_cliques, maximal_size_cliques = print_clique_analysis(G)
        
        maximal_clique = ["Tyrion", "Cersei", "Gregor", "Joffrey", "Sandor", "Ilyn", "Meryn"]

        visualize_network_with_maximal_clique_improved(G, maximal_clique)

        print("\nVisualizing maximal cliques:")
        plot_cliques(G, massimal_cliques[:5], "Massimal clique")
        
        print("\nVisualizing cliques of maximal size:")
        plot_cliques(G, maximal_size_cliques, "Maximal size xlique")

    except Exception as e:
        print(f"Error: {e}")
