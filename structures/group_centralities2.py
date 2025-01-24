import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_graph_from_dataset

def group_degree_centrality(G, group):
    non_group_nodes = set(G.nodes()) - set(group)
    connected_nodes = set()
    for node in non_group_nodes:
        neighbors = set(G.neighbors(node))
        if neighbors.intersection(group):
            connected_nodes.add(node)
    return len(connected_nodes) / len(non_group_nodes) if len(non_group_nodes) > 0 else 0

def group_closeness_centrality(G, group):
    non_group_nodes = set(G.nodes()) - set(group)
    total_distance = 0
    for node in non_group_nodes:
        shortest_paths = nx.single_source_shortest_path_length(G, node)
        distances = [shortest_paths.get(member, float('inf')) for member in group]
        min_distance = min(distances) if distances else float('inf')
        total_distance += min_distance
    return len(non_group_nodes) / total_distance if total_distance > 0 else 0

def group_betweenness_centrality(G, group):
    passing_through_group = 0
    total_paths = 0
    all_pairs = dict(nx.all_pairs_shortest_path_length(G))
    
    for source in all_pairs:
        for target, _ in all_pairs[source].items():
            if source == target:
                continue
            total_paths += 1
            path = nx.shortest_path(G, source, target)
            if any(node in group for node in path):
                passing_through_group += 1
    
    return passing_through_group / total_paths if total_paths > 0 else 0

if __name__ == "__main__":
    
    G = load_graph_from_dataset()

    # Houses
    groups = {
        'Stark': ['Eddard','Catelyn','Robb','Sansa','Arya','Bran','Rickon','Jon'],
        'Lannister': ['Tywin','Cersei','Jaime','Tyrion','Joffrey','Lancel','Kevan','Tommen','Myrcella','Gregor','Ilyn','Meryn'],
        'Targaryen': ['Aerys','Rhaegar','Viserys','Daenerys','Aegon','Drogo','Jorah','Missandei','Rakharo','Kraznys','Worm'],
        'Baratheon': ['Robert','Stannis','Renly','Shireen','Davos','Melisandre','Gendry','Salladhor','Cressen'],
        'Tyrell': ['Mace','Olenna','Margaery','Loras'],
        'Martell': ['Doran','Oberyn','Ellaria','Elia'],
        'Greyjoy': ['Balon','Theon'],
        'Tully': ['Catelyn','Edmure','Hoster','Lysa','Brynden','Roslin']
    }

    # It calculates and collects the centrality values (GDC, GCC, GBC) for each group
    group_centralities = {}
    for group_name, members in groups.items():
        # Filter the valid members (present in the graph)
        valid_members = [m for m in members if m in G.nodes()]
        if not valid_members:
            # If no member is in the graph skip
            continue
        
        gdc = group_degree_centrality(G, valid_members)
        gcc = group_closeness_centrality(G, valid_members)
        gbc = group_betweenness_centrality(G, valid_members)
        
        group_centralities[group_name] = (gdc, gcc, gbc)


    df = pd.DataFrame.from_dict(
        group_centralities,
        orient='index',
        columns=['GDC','GCC','GBC']
    )

    df = df.reindex(['Stark','Lannister','Targaryen','Baratheon','Tyrell','Martell','Greyjoy','Tully'])

    # Heatmap
    plt.figure(figsize=(6, 5))
    sns.heatmap(df, annot=True, cmap='Blues', vmin=0, vmax=1, fmt='.3f')
    plt.title("Group centralities heatmap")
    plt.yticks(rotation=0)  
    plt.show()
