import os
import pandas as pd
import networkx as nx

def load_graph_from_dataset():
    """
    Loads a graph from the 'got-nodes.csv' and 'got-edges.csv' files in the dataset folder.
    Returns:
        G (networkx.Graph): A NetworkX graph with nodes and weighted edges.
    """
    # Automatically find the 'dataset' folder in the root of the current directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(root_dir, 'dataset')

    # Define the paths to the CSV files in the 'dataset' folder
    nodes_path = os.path.join(dataset_dir, 'got-nodes.csv')
    edges_path = os.path.join(dataset_dir, 'got-edges.csv')

    # Check if the paths exist
    if not os.path.exists(nodes_path) or not os.path.exists(edges_path):
        print(f"Error: One or both of the files {nodes_path} and {edges_path} do not exist.")
        return None  # If files are missing, return None

    # Load the datasets
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

    return G
