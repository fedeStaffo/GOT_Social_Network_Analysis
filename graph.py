import networkx as nx
import matplotlib.pyplot as plt
from utils import load_graph_from_dataset

def print_graph_metrics(G):
    """
    Prints general graph metrics like number of nodes, edges, density, etc.
    """
    # Calculate and print general metrics
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    radius = nx.radius(G) if nx.is_connected(G) else float('inf')
    diameter = nx.diameter(G) if nx.is_connected(G) else float('inf')
    periphery = nx.periphery(G) if nx.is_connected(G) else []
    avg_clustering_coef = nx.average_clustering(G)
    connectivity = nx.is_connected(G)

     # Calculate weighted density
    total_weight = sum(data['weight'] for _, _, data in G.edges(data=True) if 'weight' in data)
    max_possible_weight = num_nodes * (num_nodes - 1) if num_nodes > 1 else 1
    weighted_density = total_weight / max_possible_weight

    print("\nGeneral Metrics:")
    print(f"Number of Nodes: {num_nodes}")
    print(f"Number of Edges: {num_edges}")
    print(f"Density: {density}")
    print(f"Weighted Density: {weighted_density}")
    print(f"Radius: {radius}")
    print(f"Diameter: {diameter}")
    print(f"Periphery: {periphery}")
    print(f"Average Clustering Coefficient: {avg_clustering_coef}")
    print(f"Connectivity: {connectivity}")


def plot_graph(G):
    """
    Plots the graph using multiple layouts for visualization.
    """
    layouts = ['spring', 'circular', 'kamada_kawai']
    layout_functions = {
        'spring': nx.spring_layout,
        'circular': nx.circular_layout,
        'kamada_kawai': nx.kamada_kawai_layout
    }

    for layout in layouts:
        plt.figure(figsize=(14, 12))  # Increase the plot size for better spacing
        pos = layout_functions[layout](G, seed=42, iterations=50) if layout == 'spring' else layout_functions[layout](G)

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue', alpha=0.8)

        # Draw edges with transparency
        nx.draw_networkx_edges(G, pos, alpha=0.3)

        # Draw labels using node labels from the graph
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="black", font_weight='bold')

        plt.title(f"Game of Thrones Character Relationship Graph - {layout.capitalize()} Layout", fontsize=16)
        plt.axis('off')  # Remove axis for better clarity
        plt.show()

def plot_edge_weight_distribution(G):
    """
    Plots the distribution of edge weights in the graph and prints the top 10 weights.
    """
    edges_with_weights = [(u, v, data['weight']) for u, v, data in G.edges(data=True) if 'weight' in data]

    if not edges_with_weights:
        print("No edge weights found in the graph.")
        return

    # Sort edges by weight in descending order
    edges_with_weights.sort(key=lambda x: x[2], reverse=True)

    # Print the top 10 weights with source and target
    print("Top 10 Edge Weights (Source-Target-Weight):")
    for i, (u, v, weight) in enumerate(edges_with_weights[:10], 1):
        print(f"{i}: {u}-{v}-{weight}")

    # Extract just the weights for plotting
    edge_weights = [weight for _, _, weight in edges_with_weights]

    # Plot the edge weight distribution
    plt.figure(figsize=(10, 6))
    plt.hist(edge_weights, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title("Edge Weight Distribution", fontsize=16)
    plt.xlabel("Weight", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(axis='y', alpha=0.75)
    plt.show()

if __name__ == "__main__":
    # Load the graph using the refactored function
    G = load_graph_from_dataset()

    if G:
        # Print the general graph metrics
        print_graph_metrics(G)

        # Plot the graph using different layouts
        plot_graph(G)

        # Plot the edge weight distribution
        plot_edge_weight_distribution(G)
