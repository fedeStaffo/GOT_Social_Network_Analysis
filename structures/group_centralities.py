import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

# Function to calculate group degree centrality
def group_degree_centrality(G, group):
    """
    Calculate group degree centrality.
    
    Args:
        G (networkx.Graph): The input graph.
        group (list): List of nodes representing the group.
    
    Returns:
        float: The group degree centrality.
    """
    # Get all nodes not in the group
    non_group_nodes = set(G.nodes()) - set(group)
    
    # Calculate the sum of connections from non-group nodes to group members
    connected_nodes = set()
    for node in non_group_nodes:
        neighbors = set(G.neighbors(node))
        connected_nodes.update(neighbors.intersection(group))
    
    # Degree centrality is the ratio of connected nodes to total non-group nodes
    return len(connected_nodes) / len(non_group_nodes) if len(non_group_nodes) > 0 else 0

# Function to calculate group closeness centrality
def group_closeness_centrality(G, group):
    """
    Calculate group closeness centrality.
    
    Args:
        G (networkx.Graph): The input graph.
        group (list): List of nodes representing the group.
    
    Returns:
        float: The group closeness centrality.
    """
    # Get all nodes not in the group
    non_group_nodes = set(G.nodes()) - set(group)
    
    # Calculate the sum of the shortest path lengths from group to non-group nodes
    total_distance = 0
    for node in non_group_nodes:
        shortest_paths = nx.single_source_shortest_path_length(G, node)
        distances = [shortest_paths.get(member, float('inf')) for member in group]
        total_distance += min(distances)  # Minimum distance to any member of the group
    
    # Closeness centrality is the inverse of the average distance
    return len(non_group_nodes) / total_distance if total_distance > 0 else 0

# Function to calculate group betweenness centrality
def group_betweenness_centrality(G, group):
    """
    Calculate group betweenness centrality.
    
    Args:
        G (networkx.Graph): The input graph.
        group (list): List of nodes representing the group.
    
    Returns:
        float: The group betweenness centrality.
    """
    # Calculate the total number of shortest paths in the graph
    all_pairs_shortest_paths = nx.all_pairs_shortest_path_length(G)
    
    # Count the number of paths that pass through any of the group nodes
    passing_through_group = 0
    total_paths = 0
    for source, target_paths in all_pairs_shortest_paths:
        for target, path_len in target_paths.items():
            if source != target:
                total_paths += 1
                # Check if any group node is part of the shortest path
                for group_member in group:
                    if group_member in nx.shortest_path(G, source, target):
                        passing_through_group += 1
                        break
    
    # Betweenness centrality is the ratio of paths passing through the group
    return passing_through_group / total_paths if total_paths > 0 else 0

# Function to display group centrality metrics for multiple groups
def display_group_centralities(G, groups):
    """
    Displays the centrality metrics for multiple groups in the graph.
    
    Args:
        G (networkx.Graph): The input graph.
        groups (dict): A dictionary where keys are group names and values are lists of group nodes.
    """
    for group_name, group in groups.items():
        print(f"\nCentralities for group '{group_name}':")
        degree_centrality = group_degree_centrality(G, group)
        closeness_centrality = group_closeness_centrality(G, group)
        betweenness_centrality = group_betweenness_centrality(G, group)
        
        print(f"Degree Centrality: {degree_centrality:.4f}")
        print(f"Closeness Centrality: {closeness_centrality:.4f}")
        print(f"Betweenness Centrality: {betweenness_centrality:.4f}")

if __name__ == "__main__":
    try:
        # Load the graph
        G = load_graph_from_dataset()

        # Define the groups of interest: TODO
        groups = {
            'Family1': ['Tyrion', 'Jaime', 'Cersei'],
            'Family2': ['Jon', 'Arya', 'Sansa'],
            'Family3': ['Daenerys', 'Tyrion', 'Varys']
        }

        # Display group centralities
        display_group_centralities(G, groups)

    except Exception as e:
        print(f"Error: {e}")
