import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

# Function to generate and display the ego network of a specific node
def display_ego_network(G, node):
    """
    Creates and visualizes the ego network of a specific node.
    
    Args:
        G (networkx.Graph): Input graph.
        node (str): The central node for the ego network.
    """
    # Create the ego network centered around the specified node
    ego_net = nx.ego_graph(G, node)
    
    # Print information about the ego network
    print(f"Ego Network of {node}:")
    print(f"Number of nodes: {len(ego_net.nodes())}")
    print(f"Number of edges: {len(ego_net.edges())}")
    print(f"Nodes in the ego network: {list(ego_net.nodes())}")
    print(f"Edges in the ego network: {list(ego_net.edges())}")
    print()

    # Plot the ego network
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(ego_net, seed=42)  
    node_colors = ['lightcoral' if n == node else 'lightblue' for n in ego_net.nodes()]
    nx.draw(ego_net, pos, with_labels=True, node_size=1000, node_color=node_colors, font_size=12, font_weight='bold', edge_color='gray', width=2)
    plt.title(f"Ego network of {node}", fontsize=16, fontweight='bold')
    plt.axis('off')  
    plt.tight_layout()  
    plt.show()

if __name__ == "__main__":
    try:
        G = load_graph_from_dataset()

        nodes_of_interest = ['Jon','Daenerys']

        for node in nodes_of_interest:
            display_ego_network(G, node)

    except Exception as e:
        print(f"Error: {e}")
