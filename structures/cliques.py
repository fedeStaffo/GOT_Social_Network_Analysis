import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

# Function to find and print the top 10 weighted cliques with individual contributions
def print_top_10_weighted_cliques_with_contributions(G):
    """
    Finds cliques in the graph, calculates their comprehensive weight,
    and prints the top 10 based on the total clique weight along with individual edge weights.
    
    Args:
        G (networkx.Graph): Input graph with edge weights.
    """
    cliques = []
    maximal_cliques = []
    max_clique_size = 0
    
    # Iterate through all cliques in the graph
    for clique in nx.enumerate_all_cliques(G):
        if len(clique) >= 3:  
            # Check for maximal cliques 
            if len(clique) > max_clique_size:
                max_clique_size = len(clique)
                maximal_cliques = [clique]
            elif len(clique) == max_clique_size:
                maximal_cliques.append(clique)
            
            # Calculate the total weight of the clique
            total_weight = 0
            edge_weights = []
            for i in range(len(clique)):
                for j in range(i + 1, len(clique)):
                    edge_weight = G[clique[i]][clique[j]]["weight"]
                    total_weight += edge_weight
                    edge_weights.append((clique[i], clique[j], edge_weight))

            cliques.append((clique, total_weight, edge_weights))

    # Print the number of cliques and maximal cliques
    print(f"\nThe number of cliques found is {len(cliques)} of which {len(maximal_cliques)} are maximal.")
    print(f"The maximal cliques in this network are composed of {max_clique_size} elements and are {len(maximal_cliques)}.")

    # Sort cliques first by number of nodes (descending) and then by total weight (descending)
    sorted_cliques = sorted(cliques, key=lambda x: (len(x[0]), x[1]), reverse=True)[:10]
    
    # Print the top 10 cliques with edge contributions
    print("\nTop 10 cliques ordered by number of nodes and comprehensive clique weight:")
    for i, (nodes, total_weight, edge_weights) in enumerate(sorted_cliques, 1):
        print(f"{i}. Nodes: {nodes}")
        print(f"   Number of nodes: {len(nodes)}")
        print(f"   Comprehensive clique weight: {total_weight}")
        print("   Edge contributions:")
        for edge in edge_weights:
            print(f"   {edge[0]}-{edge[1]}: {edge[2]}")
        print()

    return maximal_cliques  


# Function to plot the subgraph of each maximal clique
def plot_maximal_cliques(G, maximal_cliques):
    """
    Plots a subgraph for each maximal clique in the graph and displays edge weights.
    
    Args:
        G (networkx.Graph): Input graph with edge weights.
        maximal_cliques (list): List of maximal cliques to plot.
    """
    for i, clique in enumerate(maximal_cliques, 1):
        subgraph = G.subgraph(clique)
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(subgraph)  
        nx.draw(subgraph, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_weight='bold')
        
        # Draw edge weights
        edge_labels = {(u, v): G[u][v]["weight"] for u, v in subgraph.edges()}
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels, font_size=10, font_color='red')

        plt.title(f"Maximal Clique {i} (Size: {len(clique)})")
        plt.show()


if __name__ == "__main__":
    try:
        G = load_graph_from_dataset()

        maximal_cliques = print_top_10_weighted_cliques_with_contributions(G)

        plot_maximal_cliques(G, maximal_cliques)

    except Exception as e:
        print(f"Error: {e}")
