import numpy as np

def trilaterate(router_positions, distances):
    """
    router_positions: Lista de tuplas [(x1, y1), (x2, y2), (x3, y3)]
    distances: Lista de distancias calculadas [d1, d2, d3]
    """
    (x1, y1), (x2, y2), (x3, y3) = router_positions
    d1, d2, d3 = distances

    # Ecuaciones de círculos para encontrar la intersección
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    # Resolución del sistema lineal
    x = (C*E - F*B) / (A*E - D*B)
    y = (A*F - D*C) / (A*E - D*B)

    return x, y
