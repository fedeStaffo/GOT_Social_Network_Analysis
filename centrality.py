import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes with attributes (Id and Label)
    for _, row in nodes_df.iterrows():
        G.add_node(row['Id'], label=row['Label'])

    # Add edges with weights
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

    # Function to print the top 10 elements in a centrality measure
    def print_top_10(centrality, title):
        sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\n{title}:")
        for i, (node, centrality_value) in enumerate(sorted_centrality, 1):
            print(f"{i} {G.nodes[node]['label']}: {centrality_value}")

    # Function to plot distribution for a centrality measure
    def plot_centrality_distribution(centrality, title):
        values = list(centrality.values())
        plt.figure(figsize=(10, 6))
        sns.histplot(values, kde=True, bins=30)
        plt.title(f"{title} Distribution")
        plt.xlabel("Centrality Value")
        plt.ylabel("Frequency")
        plt.show()

    # Function to plot a heatmap-like graph visualization for a centrality measure
    def plot_heatmap_centrality(G, centrality, title, cmap='plasma'):
        plt.figure(figsize=(12, 8))
        node_colors = list(centrality.values())
        pos = nx.spring_layout(G, seed=42)  # Layout for consistent positioning

        # Draw the graph without labels
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=cmap, node_size=100, edgecolors="black")
        nx.draw_networkx_edges(G, pos, edge_color="gray")

        # Add colorbar explicitly to the current Axes
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
        sm.set_array([])
        plt.colorbar(sm, ax=plt.gca(), label="Centrality Value")  # Explicitly link to current Axes

        plt.title(title)
        plt.show()

    # Calculate and print centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)

    print_top_10(degree_centrality, "Degree Centrality")
    plot_centrality_distribution(degree_centrality, "Degree Centrality")
    plot_heatmap_centrality(G, degree_centrality, "Degree Centrality")

    print_top_10(closeness_centrality, "Closeness Centrality")
    plot_centrality_distribution(closeness_centrality, "Closeness Centrality")
    plot_heatmap_centrality(G, closeness_centrality, "Closeness Centrality")

    print_top_10(betweenness_centrality, "Betweenness Centrality")
    plot_centrality_distribution(betweenness_centrality, "Betweenness Centrality")
    plot_heatmap_centrality(G, betweenness_centrality, "Betweenness Centrality")

    print_top_10(eigenvector_centrality, "Eigenvector Centrality")
    plot_centrality_distribution(eigenvector_centrality, "Eigenvector Centrality")
    plot_heatmap_centrality(G, eigenvector_centrality, "Eigenvector Centrality")
