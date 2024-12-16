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

    print("\nGeneral Metrics:")
    print(f"Number of Nodes: {num_nodes}")
    print(f"Number of Edges: {num_edges}")
    print(f"Density: {density}")
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


if __name__ == "__main__":
    # Load the graph using the refactored function
    G = load_graph_from_dataset()

    if G:
        # Print the general graph metrics
        print_graph_metrics(G)

        # Plot the graph using different layouts
        plot_graph(G)
