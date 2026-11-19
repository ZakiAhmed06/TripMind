"""
Sightseeing Route Optimization Service
Implements Haversine distance matrix calculation, Greedy Nearest-Neighbor heuristic,
and 2-Opt local search improvement to minimize transit time between attractions.
"""
import math
from typing import List, Dict, Any


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on the earth in kilometers.
    """
    r = 6371.0  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(r * c, 3)


def calculate_route_distance(route: List[Dict[str, Any]]) -> float:
    total_km = 0.0
    for i in range(len(route) - 1):
        d = haversine_km(
            route[i]["latitude"], route[i]["longitude"],
            route[i+1]["latitude"], route[i+1]["longitude"]
        )
        total_km += d
    return round(total_km, 2)


def optimize_attraction_sequence(attractions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Given a list of attractions with latitude & longitude, orders them
    using Greedy Nearest Neighbor followed by 2-Opt refinement.
    """
    valid_points = [a for a in attractions if a.get("latitude") and a.get("longitude")]
    if len(valid_points) <= 2:
        dist = calculate_route_distance(valid_points) if len(valid_points) == 2 else 0.0
        return {
            "ordered_attractions": attractions,
            "total_distance_km": dist,
            "estimated_transit_minutes": int(dist * 3.5),
            "algorithm": "Direct Order"
        }

    # Step 1: Nearest Neighbor Greedy Tour
    unvisited = valid_points[1:]
    current = valid_points[0]
    tour = [current]

    while unvisited:
        nearest = min(
            unvisited,
            key=lambda pt: haversine_km(current["latitude"], current["longitude"], pt["latitude"], pt["longitude"])
        )
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    # Step 2: 2-Opt Improvement Heuristic
    improved = True
    best_dist = calculate_route_distance(tour)
    iterations = 0

    while improved and iterations < 50:
        improved = False
        iterations += 1
        for i in range(1, len(tour) - 1):
            for k in range(i + 1, len(tour)):
                # 2-opt swap
                new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
                new_dist = calculate_route_distance(new_tour)
                if new_dist < best_dist - 0.01:
                    tour = new_tour
                    best_dist = new_dist
                    improved = True
                    break
            if improved:
                break

    # Reassign sequence order numbers
    for idx, item in enumerate(tour, start=1):
        item["sequence_order"] = idx

    estimated_time = int(best_dist * 3.2) + len(tour) * 15  # transit time + buffer

    return {
        "ordered_attractions": tour,
        "total_distance_km": round(best_dist, 2),
        "estimated_transit_minutes": estimated_time,
        "algorithm": "Greedy Nearest-Neighbor + 2-Opt Improvement"
    }
