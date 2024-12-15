import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Automatically find the 'dataset' folder in the root of the current directory
root_dir = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(root_dir, 'dataset')

# Define the paths to the CSV files in the 'dataset' folder
nodes_path = os.path.join(dataset_dir, 'got-nodes.csv')
edges_path = os.path.join(dataset_dir, 'got-edges.csv')

# Check if the paths exist
if not os.path.exists(nodes_path) or not os.path.exists(edges_path):
    print(f"Error: One or both of the files {nodes_path} and {edges_path} do not exist.")
else:
    
    nodes_df = pd.read_csv(nodes_path)
    edges_df = pd.read_csv(edges_path)

    print("Nodes Data Head:")
    print(nodes_df.head())

    print("\nEdges Data Head:")
    print(edges_df.head())

    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes with attributes (Id and Label)
    for _, row in nodes_df.iterrows():
        G.add_node(row['Id'], label=row['Label'])

    # Add edges with weights
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

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

    # Plot using Spring Layout
    plt.figure(figsize=(14, 12))  # Increase the plot size for better spacing
    pos = nx.spring_layout(G, seed=42, iterations=50)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue', alpha=0.8)

    # Draw edges with transparency
    nx.draw_networkx_edges(G, pos, alpha=0.3)

    # Draw labels using node labels from the graph
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="black", font_weight='bold')

    plt.title("Game of Thrones Character Relationship Graph - Spring Layout", fontsize=16)
    plt.axis('off')  # Remove axis for better clarity
    plt.show()

    # Plot using Circular Layout
    plt.figure(figsize=(14, 12))  # Increase the plot size for better spacing
    pos = nx.circular_layout(G)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue', alpha=0.8)

    # Draw edges with transparency
    nx.draw_networkx_edges(G, pos, alpha=0.3)

    # Draw labels using node labels from the graph
    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="black", font_weight='bold')

    plt.title("Game of Thrones Character Relationship Graph - Circular Layout", fontsize=16)
    plt.axis('off')  # Remove axis for better clarity
    plt.show()

    # Plot using Kamada-Kawai Layout
    plt.figure(figsize=(14, 12))  # Increase the plot size for better spacing
    pos = nx.kamada_kawai_layout(G)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='skyblue', alpha=0.8)

    # Draw edges with transparency
    nx.draw_networkx_edges(G, pos, alpha=0.3)

    # Draw labels using node labels from the graph
    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="black", font_weight='bold')

    plt.title("Game of Thrones Character Relationship Graph - Kamada-Kawai Layout", fontsize=16)
    plt.axis('off')  # Remove axis for better clarity
    plt.show()
