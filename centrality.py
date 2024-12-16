import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_graph_from_dataset

# Load the graph using the load_graph_from_dataset function
G = load_graph_from_dataset()

# Check if the graph is loaded successfully
if G:
    # Function to print the top 10 elements in a centrality measure
    def print_top_10(centrality, title):
        """
        Prints the top 10 nodes based on their centrality measure.

        Args:
            centrality (dict): A dictionary where keys are node identifiers and values are their centrality values.
            title (str): The title describing the centrality measure (e.g., 'Degree Centrality').

        Prints:
            The top 10 nodes with their centrality values in descending order.
        """
        sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\n{title}:")
        for i, (node, centrality_value) in enumerate(sorted_centrality, 1):
            print(f"{i} {G.nodes[node]['label']}: {centrality_value}")

    # Function to plot distribution for a centrality measure
    def plot_centrality_distribution(centrality, title):
        """
        Plots a histogram with a kernel density estimate (KDE) for the distribution of centrality values.

        Args:
            centrality (dict): A dictionary where keys are node identifiers and values are their centrality values.
            title (str): The title of the plot.

        Displays:
            A histogram with KDE representing the distribution of centrality values.
        """
        values = list(centrality.values())
        plt.figure(figsize=(10, 6))
        sns.histplot(values, kde=True, bins=30)
        plt.title(f"{title} Distribution")
        plt.xlabel("Centrality Value")
        plt.ylabel("Frequency")
        plt.show()

    # Function to plot a heatmap-like graph visualization for a centrality measure
    def plot_heatmap_centrality(G, centrality, title, cmap='plasma'):
        """
        Plots a heatmap-like visualization of the graph nodes based on a centrality measure.

        Args:
            G (networkx.Graph): The graph object.
            centrality (dict): A dictionary where keys are node identifiers and values are their centrality values.
            title (str): The title of the plot.
            cmap (str, optional): The colormap to be used for node colors. Defaults to 'plasma'.

        Displays:
            A graph visualization with nodes colored based on centrality values, with a colorbar indicating the centrality values.
        """
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

        plt.title(f"{title} Heatmap")
        plt.show()

    # Calculate and print centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)

    # Print top 10 and plot distributions and heatmaps for each centrality measure
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

else:
    print("Error: Graph not loaded successfully.")
