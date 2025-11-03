# An ersatz Linear algebra

[ToC]

## Minimal model

Suppose that all data is a matrix.
```python
class Matrix:
    def __init__(self, rows, cols, values)
        self.rows = rows
        self.cols = cols
        self.values = values

matrix = Matrix(3, 3, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
```

We need the product of matrices.

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

We also need the identity matrix.

```python
def identity(n : int) -> Matrix:
    res = [0.0] * (n*n)
    for i in range(n):
        res[i][i] = 1
    return Matrix( n, n, res )
```

While the types in python are not robust enough to prove the necessary associativity and identity rules of these two operators we can at least use those to write some unit tests.

## Zero Space

> * An object $I$ is **initial** if for every object $A$ there is a unique morphism $i:I\to A$.  
> * An object $T$ is **terminal** if for every object $A$ there is a unique morphism $t:A\to T$.
> * A **zero** object is one that is both initial and terminal.

Vector spaces have a zero object, such as any 0-dimensional vector space.  To prove it however we need to provide the necessary unique morphisms in, and out, of the zero object.

```python
def fromZero( m : int) -> Matrix :
    return Matrix( m, 0, [])

def toZero( n : int) -> Matrix :
    return Matrix( 0, n, [])
```

Once more python is not equipped to make a proof of uniqueness but we can run an implicit test by observing that $\mathbb{R}^n\to 0 \to \mathbb{R}^m$ should be unique.  It should be the zero matrix.

```python
l0 = toZero(5)
r0 = fromZero(4)
multiply(l0, r0)
```

## Vectors as arrays

Let us take the view that the scalars are constant.  These could be floating point numbers but this will later be relaxed.  All our vector spaces are finite-dimensional as well so that means that subject to rounding errors we can imagine this is $\mathbb{R}^n$.  As such there is a clear data type to consider for vectors.

### In Python


### In OCaml

```OCaml
type matrix = {
  rows : int;
  cols : int;
  values : float array;
}

(* Populate it: *)
let matrix = {
  rows = 3;
  cols = 3;
  values = [| 1.0; 2.0; 3.0; 4.0; 5.0; 6.0; 7.0; 8.0; 9.0 |];
}
```

### In C.
```C
struct {
   int rows,
   int cols,
   float* values
}
```

### In Rust
```Rust
struct Matrix<T, const ROWS: usize, const COLS: usize> {
    values: [T; ROWS * COLS],
}
```

Which we could access by
```Rust
let matrix = Matrix::<f32, 3, 3> {
    values: [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
};
```

## Linear maps as matrices

## Identities

```Python
def identity(n) : Linear n n 
```

Many systems use the homonym `eye` for `identity`.

## Composition

```python
def compose(F, G) :
assert F.nCols() == G.nRows()
    res = []
    for i in range(F.nRows()) :
        for j in range( G.nCols() ) :
            for k in range( F.nCols() ) :
                res[i]
```

```java
public Linear<m,n> multiply(Matrix<m,s> left, Matrix<s,n> right) {
    Float[][] res = new Float[m][n];
    for (int i=0; i < m; ++i) {
        for (int j=0; j < n; ++j ){
            for (int k=0; k < s; ++k ){
                res[i][j] += left[i][k]*right[k][j]
            }
        }
    }
    return res;
}
```

```ocaml
let multiply (left : float array array) (right : float array array) : float array array =
    let m = Array.length left in
    let s = Array.length (left.(0)) in
    let n = Array.length (right.(0)) in
    let res = Array.make_matrix m n 0.0 in
    for i = 0 to m - 1 do
        for j = 0 to n - 1 do
            for k = 0 to s - 1 do
                res.(i).(j) <- res.(i).(j) +. left.(i).(k) *. right.(k).(j)
            done
        done
    done;
    res
```

```scala
def multiply[M, S, N](left: Array[Array[Float]], right: Array[Array[Float]]): Array[Array[Float]] = {
    val m = left.length
    val s = left(0).length
    val n = right(0).length
    val res = Array.ofDim[Float](m, n)
    
    for (i <- 0 until m) {
        for (j <- 0 until n) {
            for (k <- 0 until s) {
                res(i)(j) += left(i)(k) * right(k)(j)
            }
        }
    }
    res
}
```