import sys
import os
import networkx as nx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

def print_top_10_weighted_triads_with_contributions(G):
    """
    Finds triangles (triads) in the graph, calculates their comprehensive weight,
    and prints the top 10 based on the total triad weight along with individual edge weights.
    
    Args:
        G (networkx.Graph): Input graph with edge weights.
    """
    triangles = []
    
    for triangle in nx.enumerate_all_cliques(G):
        if len(triangle) == 3:  
            weight1 = G[triangle[0]][triangle[1]]["weight"]
            weight2 = G[triangle[1]][triangle[2]]["weight"]
            weight3 = G[triangle[2]][triangle[0]]["weight"]
            weight_sum = weight1 + weight2 + weight3  
            triangles.append((triangle, weight_sum, weight1, weight2, weight3))

   
    print(f"\nTotal closed triads (triangles) found: {len(triangles)}")
    sorted_triangles = sorted(triangles, key=lambda x: x[1], reverse=True)[:10]
    

    print("\nTop 10 triads ordered by comprehensive triad Weight:")
    for i, (nodes, weight_sum, weight1, weight2, weight3) in enumerate(sorted_triangles, 1):
        print(f"{i}. Nodes: {nodes}")
        print(f"   Comprehensive triad weight: {weight_sum}")
        print(f"   Edge contributions: {nodes[0]}-{nodes[1]}: {weight1}, {nodes[1]}-{nodes[2]}: {weight2}, {nodes[2]}-{nodes[0]}: {weight3}")
        print()


if __name__ == "__main__":
    try:
        G = load_graph_from_dataset()
        print_top_10_weighted_triads_with_contributions(G)

    except Exception as e:
        print(f"Error: {e}")
