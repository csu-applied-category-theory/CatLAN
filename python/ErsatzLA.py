from typing import Optional
import random


# Ersatz Linear Algebra.

# Begin with matrices as lists of length rows * cols.
class Matrix:
    def __init__(self, rows, cols, values):
        self.rows = rows
        self.cols = cols
        assert len(values) == rows * cols
        self.values = values
    def __str__(self):
        lines = []
        for i in range(self.rows):
            row_start = i * self.cols
            row_end = row_start + self.cols
            row_values = self.values[row_start:row_end]
            lines.append(str(row_values))
        return '\n'.join(lines)
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return (self.rows == other.rows and 
                self.cols == other.cols and 
                self.values == other.values)


# accepted
m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
print(m.rows)
print(m.values)
print(m.values[1]) # 4.0 since python counts from 0.

# rejected by size issues.
# m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0])

# accepted.
m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, "missing", 6.0])


def multiply(left: Matrix, right: Matrix) -> Matrix:
    """Matrix multiplication using Matrix class"""
    assert left.cols == right.rows, "Matrix dimensions incompatible"
    
    m, s, n = left.rows, left.cols, right.cols
    result = [0.0] * (m * n) # python trick to make list of zeros.
    
    for i in range(m):
        for j in range(n):
            for k in range(s):
                l = left.values[i * s + k]
                r = right.values[k * n + j]
                result[i * n + j] += l*r
    
    return Matrix(m, n, result)

m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
n = Matrix(3, 2, [7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
p = multiply(m, n)
print(p.rows)  # 2
print(p.cols)  # 2
print(p.values)  # [58.0, 64.0, 139.0, 154.0]

# rejected due to incompatible sizes.
n2 = Matrix(4, 2, [7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0])
# p = multiply(m, n2)

def identity(n : int) -> Matrix:
    res = [0.0] * (n*n)
    for i in range(n):
        res[i * n + i] = 1
    return Matrix( n, n, res )

i3 = identity(3)
print(i3.rows)  # 3
print(i3.cols)  # 3
print(i3.values)  # [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

def left(m: Matrix) -> Matrix:
    """Create left matrix for m."""
    return identity(m.rows)

def right(m: Matrix) -> Matrix:
    """Create right matrix for m."""
    return identity(m.cols)

print(m)
print(left(m))
print(right(m))


##################################

def compose(left: Optional[Matrix], right: Optional[Matrix]) -> Optional[Matrix]:
    """Matrix multiplication using Matrix class"""
    match (left, right):
        case (None, _) | (_, None):
            return None
    if left.cols != right.rows:
        return None
    # assert left.cols == right.rows, "Matrix dimensions incompatible"
    
    m, s, n = left.rows, left.cols, right.cols
    result = [0.0] * (m * n) # python trick to make list of zeros.
    
    for i in range(m):
        for j in range(n):
            for k in range(s):
                l = left.values[i * s + k]
                r = right.values[k * n + j]
                result[i * n + j] += l*r
    
    return Matrix(m, n, result)

def none() -> Optional[Matrix]:
    """Return None as a Maybe Matrix (using Optional/union type)."""
    return None

p = compose(m, n)
print(p)
p2 = compose (m, n2)
print(p2)

## Now update left, right, identity to return Optional[Matrix]
def leftId(m: Optional[Matrix]) -> Optional[Matrix]:
    """Create left matrix for m."""
    match m:
        case None:
            return None
        case Matrix():
            return identity(m.rows)

def rightId(m: Optional[Matrix]) -> Optional[Matrix]:
    """Create right matrix for m."""
    match m:
        case None:
            return None
        case Matrix():
            return identity(m.cols)


#####################################################################
# Make test of the abstract category axioms.

leftId(none()) == none()
rightId(none()) == none()

# Test composing random matrices with none()

for _ in range(10):
    rows = random.randint(1, 5)
    cols = random.randint(1, 5)
    values = [random.uniform(-10, 10) for _ in range(rows * cols)]
    test_matrix = Matrix(rows, cols, values)
    
    # Compose with none() on the left
    assert compose(none(), test_matrix) == None
    
    # Compose with none() on the right
    assert compose(test_matrix, none()) == None


# Identity laws 
m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])