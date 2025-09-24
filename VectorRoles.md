# Vectors in practice

Following Wolfgang Bangerth's discussion here is the nature of a division of roles for vectors

```C++
class Vector {
  /* Set the i-th index to val. */
  void set(int index, double val);

  /* Get the i-th index */
  double get(int index);

  /* The norm of the vector. */
  double norm() const;

  /* Rescale the vector by scalar. */
  Vector scale(double scalar) const;

  /* Add with vector u */ 
  Vector operator+(Vector u) const;
  
}
```

When inspecting software however the roles of these methods are not uniformly distributed.  There are parts of a program at the start that spend their time mostly setting or getting values which seem to prefer an interpretation of the data as an array for quick random access for arbitrary coordinates.  

Later in a program the roles shift to become about frequent use of norms, scaling, and vector addition.

Because of these different roles optimizations are handled differently. For example the getters and setters need to be low cost since all they do is change or retrieve a value and we cannot wait around for such programming language nuance as looking up the correct command from a heap.  They should instead be inlined essentially doing the operations as instantely as possible.  Meanwhile teh cost of norms, dot-products, scaling and adding are so costly that the few cycles that might be spent fetching the correct command from a heap using a virtual function call could be worthwhile in targeting the correct nuanced implementaiton which can take advantage of subtle structure.

The result is although any vector could in principle be considered as having all these operations, in reality the separate roles suggests a split abstraction where we make two vector interfaces and then implement vectors from both if we need both or separately if we need only some properties.

Switching to Java syntax
```Java
public interface IOVector {
  /* Set the i-th index to val. */
  void set(int index, double val);

  /* Get the i-th index */
  double get(int index);
  
}
```
and 
```Java
public interface BlackBoxVector {

  /* The norm of the vector. */
  double norm() const;

  /* Rescale the vector by scalar. */
  Vector scale(double scalar) const;

  /* Add with vector u */ 
  Vector operator+(Vector u) const;
 
}
```
