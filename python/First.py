
import numpy as np
from typing import TypeVar, Generic, List
import random

# Type variables for dimensions
D = TypeVar('D')
M = TypeVar('M') 
N = TypeVar('N')
P = TypeVar('P')

# Vector Space class - represents a d-dimensional vector space
class VS:
    def __init__(self, dimension: int):
        self.dimension = dimension
    
    def __repr__(self):
        return f"VS({self.dimension})"

# Linear Transformation class - represents an m×n matrix
class LT:
    def __init__(self, rows: int, cols: int, data: np.ndarray = None):
        self.rows = rows
        self.cols = cols
        if data is None:
            self.data = np.zeros((rows, cols))
        else:
            self.data = data
    
    def __repr__(self):
        return f"LT({self.rows},{self.cols})"
    
    def __mul__(self, other):
        if isinstance(other, LT):
            return LT(self.rows, other.cols, np.dot(self.data, other.data))
        return NotImplemented

# given a vector space A, return the identity linear map A to A
def getIdentity(A: VS) -> LT:
    return LT(A.dimension, A.dimension, np.eye(A.dimension))

def random_vector_space(d: int) -> VS:
    return VS(d)

def random_matrix(rows: int, cols: int) -> LT:
    return LT(rows, cols, np.random.randn(rows, cols))

def test_getIdentity():
    for i in range(100):  # Reduced from 1000 for faster testing
        for d in range(1, 10):
            A = random_vector_space(d)
            I = getIdentity(A)
            m = random_matrix(d, d)
            # Test if m * I == m (approximately, due to floating point)
            result = m * I
            if np.allclose(result.data, m.data):
                print(f"Test passed for dimension {d}")
            else:
                print(f"Test failed for dimension {d}")

def composition(L1: LT, L2: LT) -> LT:
    if L1.cols != L2.rows:
        raise ValueError(f"Cannot compose matrices: {L1.cols} != {L2.rows}")
    return LT(L1.rows, L2.cols, np.dot(L2.data, L1.data))

def getZero() -> VS:
    return VS(0)

def fromZero(A: VS) -> LT:
    return LT(0, A.dimension, np.zeros((0, A.dimension)))

def toZero(A: VS) -> LT:
    return LT(A.dimension, 0, np.zeros((A.dimension, 0)))