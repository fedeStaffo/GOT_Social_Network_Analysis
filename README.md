# Game of Thrones Social Network Analysis

📌 The dataset used in this analysis was sourced from [here](https://github.com/melaniewalsh/sample-social-network-datasets).

## Project Overview

This project analyzes the social network of characters from the Game of Thrones series. The analysis includes various centrality measures, clique detection, k-core analysis, ego networks, and group centralities. The project is structured as follows:

### Files and Directories

- `centrality.py`: Calculates and visualizes various centrality measures (degree, closeness, betweenness, eigenvector) for the graph.
- `graph.py`: Prints general graph metrics, plots the graph using different layouts, and plots the edge weight distribution.
- `structures/`
  - `cliques.py`: Finds and prints the top 10 weighted cliques with individual contributions and plots the subgraph of each maximal clique.
  - `ego_net.py`: Generates and displays the ego network of specific nodes.
  - `group_centralities.py`: Calculates and displays group centrality metrics (degree, closeness, betweenness) for predefined groups.
  - `k_core.py`: Finds and prints the k-core details with automatic selection of k and plots the k-core subgraph.
  - `triades.py`: Finds and prints the top 10 weighted triads with individual contributions.
- `utils.py`: Contains `load_graph_from_dataset` to load the graph from the dataset.
- `dataset/`
  - `got-nodes.csv`: Contains the nodes (characters) of the graph with their labels.
  - `got-edges.csv`: Contains the edges (relationships) of the graph with their weights.