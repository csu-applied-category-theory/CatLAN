
# Algebraic operators and structures.


`CC-BY-2025 James B. Wilson`  
[TBD: add your name as you edit.]

[ToC]

## Homogeneous Operators

A (homogeneous) algebraic operator is a function $\omega:A^{\ell} \to A$.  The number $\ell$ is called the **valence** or **arity** of the operator.  Some exmaples include addition of natural numbers:
```math
\begin{aligned}
\mathbb{N} & := 0 \text{ or } {+}{+}k \text{ for some existing }k:\mathbb{N}\\
+ & :\mathbb{N}^2\to \mathbb{N} & m+n & :=\begin{cases} m, & n=0; \\ {+}{+}(m+k), & n={+}{+}k.\end{cases}
\end{aligned}
```
Multiplication of polynomails $\mathbb{R}[x]$
```math
\sum_{i=0}^m a_i x^i \sum_{j=0}^n b_j x^j := \sum_{s=0}^{m+n} \left(\sum_{i+j=s} a_i b_j\right)x^s
```
maps $\cdot :\mathbb{R}[x]\times \mathbb{R}[x]\to \mathbb{R}[x]$ so it is an operator.  
Negatives count as operators, $-:\mathbb{Z}\to \mathbb{Z}$.

## Heterogeneous Operators

What our definition does **not** include is things like scalar-vector product
```math
\cdot : \mathbb{R}\times V\to V
```
nor dot-products, because those output different value than allowed as inputs.  We call these **heterogeneous** operators.  

There is a hack to be able to study these as operators.  For example, when it comes to vector spaces say over $\mathbb{R}$, then we can treat every single scalar $\lambda$ as a constant and use 
```math
L_{\lambda}:V\to V \qquad L_{\lambda}(v) := \lambda v
```
As its own univalent operator.

## Jargon

 * **nullary** valence 0
 * **univalent** valence 1
 * **bivalent** valence 2

## Constants as operators

A loop-hole is to recall that $A^{\ell}$ is the same as function $\{1,\ldots,\ell\}\to A$ and so in particular $A^0=\{\emptyset \to A\}$.  Now there is a unique function $\emptyset \to A$ so $A^0$ has cardinality 1.  Hence, an operator $A^0\to A$ is akin to choosing one symbol out of $A$, i.e. a constant.  So in this telling things like $0$ and $1$ can be included as operators using 
```math
0:\mathbb{R}^0\to \mathbb{R} \qquad 1:\mathbb{R}^0\to \mathbb{R}
```
Technically you should write something else like $\mathbf{0}:\mathbb{R}^0\to \mathbb{R}$ where $\mathbf{0}(\emptyset\to \mathbb{R}):=0$ but you get the idea.  It is easier to just count constants as 0-valent operators.

## Grammar
Usually operators come with a grammar, e.g. $u+v$ is preferred in math to `+ u v` or $+(u,v)$.  But this can change, for example, when we program we might prefer `add(u,v)`.   So you should typically include a grammar with your operator, and this will help eventually with describing things like formulas.  We can do this with Backus-Naur Form since most operators can be expressed with context-free grammars.  Here is an infix add grammar
```bnf
<Add> ::= <Add> + <Add>
```
In fact most operator grammars are so obvious form experience that we need only put in blanks for where values go, like this `(_+_)`.

> **Definition.** The **signature** of an operator is its valence and grammar.

> **Caution.** A lot of grammar is intuitive because we use ingredients of implicit rules like "order of operations" to avoid excessive parenthesis.  These are somewhat hard to model in BNF grammar but can be stated often by some degree of precedence.  For example if we want exponents to come before multiplication we could say it has order higher than multiplication.  Many programming languages will let you use such grammar, for example
```agda
infix 1 + : Nat -> Nat -> Nat
...
infix 2 * : Nat -> Nat -> Nat
```
Says to allow $u+v$ and $u*v$ and to read the $*$ before $+$ in formulas like $v+2*u$.

## An algebraic structure


> **Definition.** An algebraic structure is set $A$ with a collection of operators.
