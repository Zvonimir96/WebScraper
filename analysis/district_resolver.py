"""
Resolve Graz district from GPS coordinates using nearest-centroid matching.

Centroids were computed from the average GPS coordinates of apartments with
known districts in the willhaben database (2026-04-03, n=711 apartments with
both known district and coordinates).

Accuracy: 92.1% (655/711) tested against apartments with known districts.
All misclassifications occur between neighboring districts (e.g. Jakomini <->
Sankt Leonhard, Eggenberg <-> Wetzelsdorf). No cross-city errors.

For higher accuracy, use GeoJSON district boundaries with point-in-polygon.

Usage:
    from analysis.district_resolver import resolve_district

    resolve_district(47.051, 15.399)
    # => "Wetzelsdorf"

    resolve_district(47.051, 15.399, return_distance=True)
    # => ("Wetzelsdorf", 0.21)
"""

import math

# Average GPS coordinates (lat, lon) per Graz district.
# Source: willhaben.at apartment listings with known districts.
DISTRICT_CENTROIDS = {
    "Andritz":        (47.108276, 15.427263),
    "Eggenberg":      (47.070470, 15.398563),
    "Geidorf":        (47.083343, 15.446251),
    "Gösting":        (47.097042, 15.398061),
    "Gries":          (47.060922, 15.431127),
    "Innere Stadt":   (47.069814, 15.439028),
    "Jakomini":       (47.052819, 15.447686),
    "Lend":           (47.079657, 15.425327),
    "Liebenau":       (47.037554, 15.461645),
    "Mariatrost":     (47.101024, 15.477372),
    "Puntigam":       (47.022905, 15.431327),
    "Ries":           (47.085417, 15.492535),
    "Sankt Leonhard": (47.068151, 15.454811),
    "Sankt Peter":    (47.056394, 15.478656),
    "Straßgang":      (47.032416, 15.390411),
    "Waltendorf":     (47.070464, 15.476695),
    "Weinitzen":      (47.144300, 15.501400),
    "Wetzelsdorf":    (47.052663, 15.397743),
}


def _haversine(lat1, lon1, lat2, lon2):
    """Distance in km between two GPS points (Haversine formula)."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))


def resolve_district(lat, lon, return_distance=False):
    """
    Return the nearest Graz district for the given GPS coordinates.

    Args:
        lat: GPS latitude (float)
        lon: GPS longitude (float)
        return_distance: if True, return (district, distance_km) tuple

    Returns:
        str: district name, or tuple(str, float) if return_distance=True
    """
    best_district = None
    best_dist = float('inf')
    for district, (clat, clon) in DISTRICT_CENTROIDS.items():
        d = _haversine(lat, lon, clat, clon)
        if d < best_dist:
            best_dist = d
            best_district = district
    if return_distance:
        return best_district, round(best_dist, 2)
    return best_district
