```
import hailc.v01.tpoterba as tpot
```

This is code contributed by **Tim Poterba**. I'm a software engineer 
working on the Hail development team at the Broad Institute, and I care 
about making Hail as useful as possible for as many people as possible.

## Table of Contents:

1. Utility Functions

## 1. Utility Functions

-----

#### `mutate_va_schema(vds, f)`: Rename variant annotations in a dataset according to a function. 
  
  Lower-case each annotation name in variant schema:
  
  ```python
  >>> vds = tpot.mutate_va_schema(vds, lambda x: x.lower())
  ```

  Replace all instances of '.' with '__':

  ```python
  >>> vds = tpot.mutate_va_schema(vds, lambda x: x.replace('.', '__'))
  ```
  
-----

#### `mutate_sa_schema(vds, f)`: Rename sample annotations in a dataset according to a function.
 
 The usage is identical to `mutate_va_schema` above.
 
-----
