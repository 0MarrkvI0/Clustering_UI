import random
import numpy as np
from scipy.spatial import distance

# Define a Point class to represent a point in 2D space
class Point:
    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate
       
    def to_2d(self):
        return (self.x, self.y)

# Define a Cluster class to represent a group of points
class Cluster:
    def __init__(self, identificational_number, initial_point,user_method):
        self.id = identificational_number
        self.points = []
        self.average_points_distance = 0
        self.cluster_to_merge = False
        self.centroid = None
        self.medoid = None
        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.add_point(initial_point,user_method)
    
    def add_point(self, point,user_method):
        if isinstance(point, Point):
            self.points.append(point)
            # Recalculate centroid when a new point is added
            self.calculate_centroid()
            # If the user has chosen the medoid method, also calculate the medoid
            if (user_method):
                self.calculate_medoid()

    def calculate_centroid(self):
        # Calculate the centroid (mean position) of the cluster if it contains points
        if self.points:
            coords = np.array([(point.x, point.y) for point in self.points])
            self.centroid = tuple(coords.mean(axis=0))
    
    def calculate_medoid(self):
        # Calculate the medoid, defined as the point closest to the centroid
        if self.centroid:
            min_distance = float('inf')
            closest_point = None

            # Find the point with the smallest distance to the centroid
            for point in self.points:
                # Calculate squared Euclidean distance to centroid (avoids computing square root)
                dist_to_centroid = (point.x - self.centroid[0]) ** 2 + (point.y - self.centroid[1]) ** 2
                if dist_to_centroid < min_distance:
                    min_distance = dist_to_centroid
                    closest_point = point

            self.medoid = closest_point

    def calculate_average(self, user_method):
        # Calculate the average distance of points in the cluster from the medoid or centroid
        if user_method:
            distances = [distance.euclidean((point.x, point.y), (self.medoid.x, self.medoid.y)) for point in self.points]
        else:
            distances = [distance.euclidean((point.x, point.y), self.centroid) for point in self.points]

        average_distance = np.mean(distances)
        self.average_points_distance = average_distance
        return average_distance