# An ersatz Linear algebra

[ToC]

## Ersatz LA just about matrices.

If we embrace the idea of categories of data then we interpret all values through their morphisms.  This is not a healthy perspective for every problem but by imposing this limit we can at times begin with a simpler data type and forgo concerns about over engineering before we actually have a working prototype.

To stick with an ersatz (i.e. a inferior copy) of linear algebra we first reduce all linear transformations to simply being matrices.  To exercise some coding discipline we can make this in a new data type called `Matrix` and we will even insert the smallest bit of safety.
```python
class Matrix:
    def __init__(self, rows, cols, values):
        self.rows = rows
        self.cols = cols
        assert len(values) == rows * cols
        self.values = values
```

You can test this by making a file with the above code and saving it as `ErsatzLA.py`.  If you don't want to follow along you can jump ahead and use `ErsatzLAFinal.py`. To run it, first have python installed, be in the same directory as the file and type
```python
user$ python3
exec( open( "ErsatzLA.py" ).read() )
m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
print(m.rows)
print(m.values)
print(m.values[0]) # 2.0 since python counts from 0.
```
A loose amount of checking happens, try making the list too short.
```
m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0])
```
But notice we are not inspecting thuroughly.
```
m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, "missing", 6.0])
```

## Composition
We need the product of matrices which we can do by hand so we understand the mechanics a bit.  This not recommend for production as matrix multiplication is vastly studied and optimized algorithm you wont improve on by writing on your own.

```python
def multiply(left: Matrix, right: Matrix) -> Matrix:
    """Matrix multiplication using Matrix class"""
    assert left.cols == right.rows, "Matrix dimensions incompatible"
    
    m, s, n = left.rows, left.cols, right.cols
    result = [0.0] * (m * n)
    
    for i in range(m):
        for j in range(n):
            for k in range(s):
                l = left.values[i * s + k]
                r = right.values[k * n + j]
                result[i * n + j] += l*r
    
    return Matrix(m, n, result)
```

Run a test
```python

m = Matrix(2, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
n = Matrix(3, 2, [7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
p = multiply(m, n)
print(p.rows)  # 2
print(p.cols)  # 2
print(p.values)  # [58.0, 64.0, 139.0, 154.0]

# rejected due to incompatible sizes.
n2 = Matrix(4, 2, [7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0])
p = multiply(m, n2)
```

We also need the identity matrix.

```python
def identity(n : int) -> Matrix:
    res = [0.0] * (n*n)
    for i in range(n):
        res[i][i] = 1
    return Matrix( n, n, res )
```
Here's a quick look
```python
print(identity(5))
```

### Helper program: Printing
It will get tedious to look at matrices as lists so let us tell python to print these row-by-row.  Add the following to `class Matrix` 
```python
    def __str__(self):
        lines = []
        for i in range(self.rows):
            row_start = i * self.cols
            row_end = row_start + self.cols
            row_values = self.values[row_start:row_end]
            lines.append(str(row_values))
        return '\n'.join(lines)
```
Reload `ErsatzLA.py` and try
```python
print(identity(5))
```

### Further operators.
In a single sorted category we need to ignore objects and deal instead with operators that get us identities.
```python
def left(m: Matrix) -> Matrix:
    """Create left matrix for m."""
    return identity(m.rows)

def right(m: Matrix) -> Matrix:
    """Create right matrix for m."""
    return identity(m.cols)

print(m)
print(left(m))
print(right(m))
```

Still missing is the failure to compose.  We can leave this as an error but that means we exit the algebra and stop following the theory.  So now let us revisit our plan with the option to return a token that reveals the error without halting our progress.  We add a type `None`.

```python

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

def none() -> Matrix | None:
    """Return None."""
    return None

p = compose(m, n)
print(p)
p2 = compose (m, n2)
print(p2)
```

Now if we commit to managing compisition errors as algebra then we should update all our commands.
```python
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
```

> Notice we have not biased ourselves to thinking of an orientation of our matrices.  We could think of row vectors coming on the left or column vectors comming in on the right.  This reflects the self-dual reality of categories and is the reason there even is an "op"-category.

### Testing axioms
In a category we know that composition, when defined, is associative, and identities behave, well, as identities.

> **Definition.** An [algebraic sturcture](Algebra.md) $A$ with signature $\langle \bot, \lhd(-), (-)\lhd, (-)\circ(-)\rangle$ and satisfying the following equational laws.
```math
\begin{aligned}
    \lhd(\bot) & = \bot & (\bot)\lhd & = \bot\\
    f\circ \bot & = \bot & \bot \circ g & = \bot\\
    \lhd(f\lhd) & = f\lhd & (\lhd f)\lhd & = \lhd f\\
    (\lhd f)f & = f & f(f\lhd) & = f\\
    \lhd(fg) & = \lhd (f(\lhd g)) & (fg)\lhd & ((f\lhd)g)\lhd\\
    f\circ (g\circ h) & = (f\circ g)\circ h
\end{aligned}
```

While the types in python are not robust enough to prove the necessary associativity and identity rules of these two operators we can at least use those to write some unit tests.

#### Test left/right identity of nothing.
```python
leftId(none()) == none()
rightId(none()) == none()
```

#### Test composing with nothing is nothing
```python
for _ in range(10):
    rows = random.randint(1, 5)
    cols = random.randint(1, 5)
    values = [random.uniform(-10, 10) for _ in range(rows * cols)]
    test_matrix = Matrix(rows, cols, values)
    
    # Compose with none() on the left
    assert compose(none(), test_matrix) == None
    
    # Compose with none() on the right
    assert compose(test_matrix, none()) == None
```

#### Test composing with left/right identity is constant.

Here we plan to test $(\lhd f)f=f$ but it will require us to now think of the hidden operator in categories, the equal sign!  Run this test
```python
rows = random.randint(1, 5)
cols = random.randint(1, 5)
values = [random.uniform(-10, 10) for _ in range(rows * cols)]
test_matrix = Matrix(rows, cols, values)
print(test_matrix)
print(leftId(test_matrix))
print(compose(leftId(test_matrix), test_matrix))
# Compose with none() on the left
assert compose(leftId(test_matrix), test_matrix) == test_matrix
```
The problem is one that goes underappreciated in math circles which is that often whatever we mean by equals is implicit from context but is not in any direct way understood by something as "follow-the-rules" as a program.  We can override this by resetting equals by adding this to our `class Matrix`
```python
    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return (self.rows == other.rows and 
                self.cols == other.cols and 
                self.values == other.values)
```
Now rerun our test and it will work.

```python
for _ in range(10):
    rows = random.randint(1, 5)
    cols = random.randint(1, 5)
    values = [random.uniform(-10, 10) for _ in range(rows * cols)]
    test_matrix = Matrix(rows, cols, values)
    
    # Compose with none() on the left
    assert compose(leftId(test_matrix), test_matrix) == test_matrix
    
    # Compose with none() on the right
    assert compose(test_matrix, rightId(test_matrix)) == test_matrix
```
[TBD: write some unit tests matching the axioms]