from classes.matrix import MatrixOfDistances, ClusteringEndException

import time
from concurrent.futures import ThreadPoolExecutor

# Prompt the user to choose the clustering method: 0 for centroid, 1 for medoid
user_input = input("Choose clustering method (0 - centroid, 1 - medoid): ")
number_clusters = int(input("Number of clusters: "))

method = user_input == '1'
start_time = time.time()
# Initialize the MatrixOfDistances object with the chosen clustering method
matrix = MatrixOfDistances(method)

# Initialize the clustering process by creating an initial set of 20 clusters
matrix.add_initial_clusters(20)
# Add clusters up to the user-defined number
matrix.add_clusters(number_clusters)

matrix.create_distance_matrix()
print("\nInitial distance matrix")
print(matrix.matrix)

solution_found = False

# Use ThreadPoolExecutor for potential parallel execution of the clustering process
with ThreadPoolExecutor() as executor:
    while not solution_found:
        try:
            # Merge the closest clusters iteratively until the final clustering is reached
            matrix.merge_closest_clusters()
        except ClusteringEndException as e:
            print(matrix.matrix)
            end_time = time.time()
            execution_time = end_time - start_time
            print("Clustering completed. Displaying the final plot.")
            print(f"Execution time: {execution_time:.6f} seconds")
            matrix.plot_clusters()
            solution_found = True