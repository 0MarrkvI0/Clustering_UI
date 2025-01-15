from classes.cluster import Point, Cluster

import random
import numpy as np
from scipy.spatial import distance
import copy
import matplotlib.pyplot as plt


def binary_search(clusters, target_id):
    left, right = 0, len(clusters) - 1
    while left <= right:
        mid = (left + right) // 2
        if clusters[mid].id == target_id:
            return mid
        elif clusters[mid].id < target_id:
            left = mid + 1
        else:
            right = mid - 1
    return -1

class ClusteringEndException(Exception):
    def __init__(self, message="End of clustering. Conditions satisfied"):
        super().__init__(message)

class MatrixOfDistances:
    def __init__(self, user_method):
        self.method = user_method
        self.clusters = []
        self.min_coordinates = -5000
        self.max_coordinates = 5000
        self.merge_index = 500
        self.matrix = None

    def add_initial_clusters(self, number_of_clusters):
        # Create and add clusters with random coordinates within specified bounds
        for _ in range(number_of_clusters):
            x, y = random.randint(self.min_coordinates, self.max_coordinates), random.randint(self.min_coordinates, self.max_coordinates)
            cluster = Cluster(len(self.clusters), Point(x, y), self.method)
            self.clusters.append(cluster)
            print(f"Added cluster: {cluster.id} with point: ({x}, {y})")

    def add_clusters(self, number_of_clusters):
        # Add clusters near randomly selected existing clusters, ensuring coordinates stay within bounds
        for _ in range(number_of_clusters):
            parent_cluster = random.choice(self.clusters)
            x = np.clip(parent_cluster.points[0].x + random.randint(-100, 100), self.min_coordinates, self.max_coordinates)
            y = np.clip(parent_cluster.points[0].y + random.randint(-100, 100), self.min_coordinates, self.max_coordinates)
            cluster = Cluster(len(self.clusters), Point(x, y), self.method)
            self.clusters.append(cluster)

    def create_distance_matrix(self):
        # Calculate the distance matrix for cluster centers or medoids, setting diagonals to infinity
        if not self.clusters:
            return

        centers = [cluster.medoid.to_2d() if self.method else cluster.centroid for cluster in self.clusters]
        self.matrix = distance.cdist(centers, centers, metric='euclidean')
    
        np.fill_diagonal(self.matrix, np.inf)
        mask = np.tril_indices(len(self.clusters), k=-1)
        self.matrix[mask] = np.inf


    def update_matrix(self, cluster1_index,cluster2_index):
            # Merge two clusters and update the matrix if merging conditions are met
            cluster_a = self.clusters_backup[cluster1_index]
            cluster_b = self.clusters_backup[cluster2_index]
        
            if not cluster_a.cluster_to_merge and not cluster_b.cluster_to_merge:
                # Extend points from cluster B to cluster A and calculate new centroid or medoid
                cluster_a.points.extend(cluster_b.points)
            
                cluster_a.calculate_centroid()
                if self.method:
                    cluster_a.calculate_medoid()

                # Check if the average points exceed the merge threshold; if so, stop clustering
                if cluster_a.calculate_average(self.method) >= self.merge_index:
                    print(f"Average points exceeded {self.merge_index}")
                    raise ClusteringEndException(f"Average points exceeded {self.merge_index}")

                # Update clusters in place by removing the merged cluster and replacing the existing one
                else:
                   index_add = binary_search(self.clusters, cluster_a.id)
                   if index_add != -1:
                        self.clusters[index_add] = cluster_a 

                   index_delete = binary_search(self.clusters, cluster_b.id)
                   if index_delete != -1: 
                        self.clusters.pop(index_delete) 

                   # Mark clusters as merged in the backup list
                   self.clusters_backup[cluster1_index].cluster_to_merge = True
                   self.clusters_backup[cluster2_index].cluster_to_merge = True


    def merge_closest_clusters(self):
        # Merge the closest clusters based on the current distance matrix
        if len(self.clusters) == 1:
            raise ClusteringEndException("Finite state reached")

        # Sort pairs of clusters by distance and identify those within a threshold for merging
        sorted_pairs = sorted(
                [(min(i, j), max(i, j), self.matrix[i, j]) for i, j in zip(*np.where(self.matrix <= 800))],
                key=lambda x: x[2]
            )

        # If no pairs meet the merge criteria, stop the clustering process
        if not sorted_pairs:
            raise ClusteringEndException("Too long distance")

        # Backup clusters state for potential rollback if merging is unsuccessful
        self.clusters_backup = copy.deepcopy(self.clusters)
        
        # Reset merge flags and recompute distance matrix
        for pair in sorted_pairs:
            i, j, distance_value = pair
            try:
                self.update_matrix(i, j)
            except ClusteringEndException as e:
                raise ClusteringEndException("Finite state reached")

        for cluster in self.clusters:
            cluster.cluster_to_merge = False
        self.create_distance_matrix()
        print(self.matrix)


    def plot_clusters(self):
        # Plot clusters using matplotlib to visualize their distribution and medoids/centroids
        plt.figure(figsize=(8, 6))
        for cluster in self.clusters:
            if cluster.points:
                x = [point.x for point in cluster.points]
                y = [point.y for point in cluster.points]
                normalized_color = [c / 255 for c in cluster.color]
                plt.scatter(x, y, color=normalized_color, label=f'Cluster {cluster.id}')

                if(self.method):
                    plt.scatter(cluster.medoid.x,cluster.medoid.y,marker='x', s=200, color='black')
                else:
                    x,y = cluster.centroid
                    plt.scatter(x,y,marker='x', s=200, color='black')

        plt.title('Clusters Visualization')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.xlim(self.min_coordinates, self.max_coordinates)
        plt.ylim(self.min_coordinates, self.max_coordinates)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.grid()
        plt.show()

    @staticmethod
    def rgb_to_hex(rgb):
        return '#' + ''.join(f'{c:02x}' for c in rgb)