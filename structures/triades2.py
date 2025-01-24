import networkx as nx
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset


if __name__ == "__main__":
    try:
        G = load_graph_from_dataset()

        average_clustering = nx.average_clustering(G)
        clustering_per_node = nx.clustering(G)
        print(f"Average clustering coefficient: {average_clustering:.4f}")
        print("\nClustering coefficient of node (ordered):")
        for node, coef in sorted(clustering_per_node.items(), key=lambda x: x[1], reverse=True):
            print(f"Node {node}: {coef:.4f}")

    
        transitivity = nx.transitivity(G)
        print(f"\nTransitivity: {transitivity:.4f}")


        triangles_per_node = nx.triangles(G)
        total_triangles = sum(triangles_per_node.values()) // 3
        print(f"\n N. of triads for node (ordered):")
        for node, count in sorted(triangles_per_node.items(), key=lambda x: x[1], reverse=True):
            print(f"Node {node}: {count}")
        print(f"\n Total triads: {total_triangles}")

      
        open_triads_estimated = 0
        for node in G.nodes():
            degree = G.degree(node)
            possible_triads = degree * (degree - 1) // 2  
            closed_triads = triangles_per_node[node]
            open_triads_estimated += possible_triads - closed_triads

        print(f"\n N. of open triads: {open_triads_estimated}")
        print(f"Number of closed triads: {total_triangles}")


        
        plt.figure(figsize=(10, 6))
        bins = np.linspace(0, 1, 10)  
        counts, edges, bars = plt.hist(
            clustering_per_node.values(),
            bins=bins,
            color="#4CAF50",  
            alpha=0.85,
            edgecolor="black",  
            rwidth=0.85,  
        )

    
        for count, edge in zip(counts, edges):
            if count > 0:
                plt.text(edge + (bins[1] - bins[0]) / 2, count + 0.5, int(count), ha="center", fontsize=10)

        plt.title("Distribution of the clustering coefficient", fontsize=16)
        plt.xlabel("Clustering coefficient", fontsize=14)
        plt.ylabel("Number of nodes", fontsize=14)
        plt.xticks(bins, [f"{b:.1f}" for b in bins], fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(axis="y", linestyle="--", alpha=0.7)  

    
        plt.tight_layout()
        plt.show()
        labels = ['Closed triads', 'Closed triads']
        sizes = [total_triangles, open_triads_estimated]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Closed triads vs open triads")
        plt.show()

    except Exception as e:
        print(f"Error: {e}")
