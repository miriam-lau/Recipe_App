EPSILON = 0.000000001


# Behaves like Java's compareTo. Returns 1 if a>b, 0 if a==b, and -1 if a<b.
def compare(a: float, b: float):
    if abs(a - b) < EPSILON:
        return 0
    return 1 if (a > b) else -1
