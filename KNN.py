import random
import pandas as pd
import matplotlib.pyplot as plt
import math

# Function to calculate Euclidean distance between two nodes based on node indices
def calculate_distance(node1, node2, node_positions):
    x1, y1 = node_positions[node1]
    x2, y2 = node_positions[node2]

    # Euclidean distance formula
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return distance

# Function to generate initial solution using the nearest rule
def generate_initial_solution(nodes, node_positions):
    remaining_nodes = set(nodes)
    routes = []
    paths = []

    while remaining_nodes:
        current_node = random.choice(list(remaining_nodes))
        route = [current_node]
        path = [current_node]
        remaining_nodes.remove(current_node)

        while remaining_nodes:
            nearest_node = min(remaining_nodes, key=lambda x: calculate_distance(route[-1], x, node_positions))
            route.append(nearest_node)
            path.append(nearest_node)
            remaining_nodes.remove(nearest_node)

        routes.append(route)
        paths.append(path)

    return routes, paths

# Function to plot routes
def plot_routes(routes, node_positions, best_route=None):
    for route in routes:
        route_positions = [node_positions[node] for node in route]
        route_positions.append(route_positions[0])  # Close the loop
        x, y = zip(*route_positions)
        plt.plot(x, y, marker='o')

    if best_route:
        best_route_positions = [node_positions[node] for node in best_route]
        best_route_positions.append(best_route_positions[0])  # Close the loop
        x_best, y_best = zip(*best_route_positions)
        plt.plot(x_best, y_best, marker='o', linestyle='dashed', color='red', linewidth=2, label='Best Route')

    plt.title('Vehicle Routing Problem - Possible Routes')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

# Algorithm 1: The VRP model
def vrp_algorithm(nodes, node_demand, node_positions):
    # Step 2: Generate Initial Solution
    initial_routes, initial_paths = generate_initial_solution(nodes, node_positions)

    # Step 3: Calculate Fitness of Initial Solution
    initial_distance = sum(calculate_distance(route[0], route[-1], node_positions) for route in initial_routes)
    initial_demand = sum(sum(node_demand[node] for node in route) for route in initial_routes)
    initial_fitness = initial_distance + initial_demand

    # Step 4: Set Best Solution
    best_routes = initial_routes
    best_fitness = initial_fitness

    # Step 6: Loop for 10,000 iterations
    for _ in range(10000):
        # Step 6.1: Generate New Solution
        new_routes, new_paths = generate_initial_solution(nodes, node_positions)

        # Step 6.2: Calculate Fitness of New Solution
        new_distance = sum(calculate_distance(route[0], route[-1], node_positions) for route in new_routes)
        new_demand = sum(sum(node_demand[node] for node in route) for route in new_routes)
        new_fitness = new_distance + new_demand

        # Step 6.3: Update Best Solution if New Solution is better
        if new_fitness < best_fitness:
            best_routes = new_routes
            best_fitness = new_fitness

    # Step 9: Output results
    print("Best solution:")
    for i, route in enumerate(best_routes):
        print(f"Route {i + 1}: {route}")
    print(f"Best Fitness: {best_fitness}")

    # Step 10: Plot the Best Solution
    plot_routes(best_routes, node_positions, best_route=best_routes[0])  # Assuming there is only one best route

# Import data from Excel file
def import_data(file_path):
    data = pd.read_excel(file_path)
    nodes = data['CUSTOMER_CODE'].tolist()
    node_demand = dict(zip(data['CUSTOMER_CODE'], data['DEMAND']))
    node_positions = dict(zip(data['CUSTOMER_CODE'], zip(data['CUSTOMER_LONGITUDE'], data['CUSTOMER_LATITUDE'])))
    return nodes, node_demand, node_positions

# Example usage with the full path of the file
file_path = r"C:\Users\pauli\OneDrive - wvsu.edu.ph\Desktop\pau\Submissions\2023-2024\AI\New folder\DATASET.xlsx"  # Update with the correct full path
nodes, node_demand, node_positions = import_data(file_path)

# Run the VRP algorithm and plot the routes
vrp_algorithm(nodes, node_demand, node_positions)
