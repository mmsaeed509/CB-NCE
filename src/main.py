import COLORS
import warnings
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances

#
# Generate a random graph adjacency matrix (replace with your data)
# Adjacency matrix represents the connections between nodes (10000 nodes)
#
adjacency_matrix = np.random.rand(100, 100)

# Define parameters (step 2) #
Kmin = 2  # Minimum number of clusters #
Kmax = 25  # Maximum number of clusters #

# Initialize variables #
best_k = None
best_ace_upper_bound = np.inf

# Suppress FutureWarning for n_init #
warnings.simplefilter(action='ignore', category=FutureWarning)


#
# use Degree Centrality to calc
# Degree centrality is a simple measure that calculates the number of edges connected to a node.
# Nodes with higher degrees are considered more central.
# (step 3)
def calculate_centrality(adjacencyMatrix, node_idx):
    # print(COLORS.BOLD_GREEN + "\nAdjacency Matrix : \n" + COLORS.BOLD_BLUE)
    # print(adjacencyMatrix)

    # return Centrality #
    return np.sum(adjacencyMatrix[node_idx])


# Loop through possible numbers of clusters #
for K in range(Kmin, Kmax + 1):

    # Cluster the graph using KMeans clustering method #
    kmeans = KMeans(n_clusters=K)
    cluster_labels = kmeans.fit_predict(adjacency_matrix)  # Type for each cluster #

    # average center error #
    ace_upper_bound = 0

    #
    # Calculate centrality-based ACE(average center error) for each cluster
    # to choice the optimal number of cluster (the smallest No. errors)
    #
    for cluster_idx in range(K):
        cluster_nodes = np.where(cluster_labels == cluster_idx)[0]

        # Calculate the estimated center of the cluster (step 3) #
        estimated_center = cluster_nodes[
            np.argmax([calculate_centrality(adjacency_matrix, node_idx) for node_idx in cluster_nodes])]

        # Calculate ACE for the cluster (step 4,7) #
        # sum difference (ture and estimated)
        ace_cluster = 0
        for node_idx in cluster_nodes:
            ace_cluster += np.sum(
                np.square(
                    pairwise_distances(
                        adjacency_matrix[node_idx].reshape(1, -1), adjacency_matrix[estimated_center].reshape(1, -1))
                )
                                  )
        ace_upper_bound += ace_cluster

    # Update the best upper bound of ACE and the corresponding K value #
    if ace_upper_bound < best_ace_upper_bound:
        best_ace_upper_bound = ace_upper_bound
        best_k = K

print(COLORS.BOLD_PURPLE + "\nEstimated optimal number of clusters: " + COLORS.BOLD_CYAN, best_k)
