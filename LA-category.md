# Categories as Algebraic structures.

`CC-BY-2025 James B. Wilson`  
[TBD: add your name as you edit.]

[ToC]

## An algebraic category.

In the beginning categories were invented as a form of algebra to study concepts of equality.  Its usefullness in topology and algebraic geometry became very important and much of what is written about it today is targeted at those questions.  However, defining categories with objects and morphisms and hom-sets and the rest is technical and prone to lots of gaps or mistakes.  So for some purposes it can be helpful to use a simpler account.  This is one such account.  This form was known to Saunders Maclane and popular amongst universal algebraist especially Peter Freyd.  However, the language of partial operators has often been employed to some confusion and occassional error.  So here we give a modified treatment based on [Brooksbank et. al.](#refs). 

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


## A Python Matrix category.

First we make a program to multiply matrices over the integers `ZZ` with errors returned as `None`.
```python
def compose( A : Optional[Matrix], B : Optional[Matrix] ) : Optional[Matrix]
    if A is None or B is None :
        return None
    if A.ncols() != B.nrows() :
        return None
    C = Matrix( ZZ, A.nrows(), B.ncols() )
    for i in range( A.nrows() ) :
        for j in range( B.ncols() ) :
            s = 0
            for k in range( A.ncols() ) :
                s += A[i,k]*B[k,j]
            C[i,j] = s
    return C
```

This is a binary operation on the data type `Optional[Matrix]` which is the union of the type `Matrix` and the type `NoneType`.   So we next add the target and source operators.

```python
def source( A : Optional[Matrix] ) : Optional[Matrix]
    if A is None :
        return None
    return IdentityMatrix( ZZ, A.ncols() )

def target( A : Optional[Matrix] ) : Optional[Matrix] :
    if A is None :
        return None
    return IdentityMatrix( ZZ, A.nrows() )
```

