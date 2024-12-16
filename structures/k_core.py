import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

# Function to find and print the k-core details with automatic selection of k
def print_k_core_details(G):
    """
    Automatically selects the k-core with the highest degree, calculates its comprehensive weight, 
    and prints details such as the number of nodes, total weight, and edge contributions.
    
    Args:
        G (networkx.Graph): Input graph with edge weights.
    """
    # Find the maximum degree of the graph
    degrees = dict(G.degree())
    max_degree = max(degrees.values())
    
    # Try progressively lower k values until a non-empty k-core is found
    for k in range(max_degree, 0, -1):
        k_core = nx.k_core(G, k)
        if len(k_core.nodes()) > 0:
            break

    # If no non-empty k-core is found (which should not happen unless the graph is disconnected with low degrees)
    if len(k_core.nodes()) == 0:
        print("No k-core subgraph found with the given degree threshold.")
        return None

    # Calculate the total weight of the k-core subgraph
    total_weight = 0
    edge_weights = []
    for u, v in k_core.edges():
        edge_weight = k_core[u][v]["weight"]
        total_weight += edge_weight
        edge_weights.append((u, v, edge_weight))

    # Print the details of the k-core subgraph
    print(f"\nThe k-core (with degree {k}) has {len(k_core.nodes())} nodes and {len(k_core.edges())} edges.")
    print(f"Total weight of the k-core subgraph: {total_weight}")
    print("Edge Contributions:")
    for edge in edge_weights:
        print(f"   {edge[0]}-{edge[1]}: {edge[2]}")
    print()

    return k_core, k  # Return the k-core and the value of k for plotting


# Function to plot the k-core subgraph
def plot_k_core(G, k_core, k):
    """
    Plots the k-core subgraph and displays edge weights.
    
    Args:
        G (networkx.Graph): Input graph with edge weights.
        k_core (networkx.Graph): The k-core subgraph to be plotted.
        k (int): The degree threshold for the k-core.
    """
    # Draw the k-core subgraph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(k_core)  # Layout for node positions
    nx.draw(k_core, pos, with_labels=True, node_size=3000, node_color='lightgreen', font_size=12, font_weight='bold')

    # Draw edge labels (edge weights)
    # edge_labels = {(u, v): G[u][v]["weight"] for u, v in k_core.edges()}
    # nx.draw_networkx_edge_labels(k_core, pos, edge_labels=edge_labels, font_size=10, font_color='red')

    plt.title(f"K-core Subgraph (Degree {k})")
    plt.show()


if __name__ == "__main__":
    try:
        # Load the graph
        G = load_graph_from_dataset()

        # Print the details of the k-core subgraph with automatic k selection
        k_core, k = print_k_core_details(G)

        if k_core:
            # Plot the k-core subgraph
            plot_k_core(G, k_core, k)

    except Exception as e:
        print(f"Error: {e}")
