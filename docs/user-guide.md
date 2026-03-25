# User Guide

## How DataZip Works

A DataZip file is a standard `.zip` archive with a specific internal layout:

- **Data files**: Large objects are stored as `.parquet` (DataFrames, Series), `.npy` (NumPy arrays), or `.pkl` (pickled objects like Plotly figures).
- **`__attributes__.json`**: References to all stored objects and their types.
- **`__metadata__.json`**: Version information, creation timestamp, and username.
- **`__state__.json`**: Serialized state for custom objects.

This makes DataZip archives human-inspectable: you can open them with any zip tool and read the JSON files directly.

## Supported Types

### Primitives

All standard Python primitives are supported:

```python
with DataZip(buffer, "w") as z:
    z["s"] = "hello"
    z["i"] = 42
    z["f"] = 3.14
    z["b"] = True
    z["n"] = None
    z["c"] = 1 + 2j         # complex numbers
```

### Collections

```python
with DataZip(buffer, "w") as z:
    z["d"] = {"key": "value", "nested": {"a": 1}}
    z["l"] = [1, 2, 3]
    z["t"] = (1, "two", 3.0)    # tuples are preserved (not converted to list)
    z["s"] = {1, 2, 3}          # sets
    z["fs"] = frozenset({1, 2}) # frozensets
```

### Date and Time

```python
from datetime import datetime
with DataZip(buffer, "w") as z:
    z["dt"] = datetime(2024, 1, 15, 12, 0, 0)
```

### Paths

```python
from pathlib import Path
with DataZip(buffer, "w") as z:
    z["path"] = Path("/usr/local/data")
```

### NumPy Arrays

Arrays are stored in `.npy` format, preserving dtype and shape:

```python
import numpy as np
with DataZip(buffer, "w") as z:
    z["arr"] = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
```

### Pandas DataFrames

DataFrames are stored as Parquet. DataZip preserves:

- Column dtypes
- **MultiIndex columns** (even though Parquet doesn't natively support them)
- Index structure

```python
import pandas as pd
with DataZip(buffer, "w") as z:
    # Regular DataFrame
    z["df"] = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0]})

    # MultiIndex columns
    z["multi"] = pd.DataFrame(
        {(0, "x"): [1, 2], (0, "y"): [3, 4], (1, "x"): [5, 6]}
    )
```

#### PyArrow Dtypes

If you use PyArrow-backed dtypes globally, you can tell DataZip to ignore stored dtype information:

```python
DataZip("file.zip", "r", ignore_pd_dtypes=True)
```

### Pandas Series

Series are stored as Parquet and the Series name is preserved:

```python
with DataZip(buffer, "w") as z:
    z["series"] = pd.Series([1, 2, 3], name="my_series")
```

### Polars

Polars DataFrames, LazyFrames, and Series are stored as Parquet:

```python
import polars as pl
with DataZip(buffer, "w") as z:
    z["pl_df"] = pl.DataFrame({"a": [1, 2, 3]})
    z["pl_lazy"] = pl.LazyFrame({"b": [4, 5, 6]})
    z["pl_series"] = pl.Series("c", [7, 8, 9])
```

### NamedTuples

NamedTuples are reconstructed if the class is importable. If not, they fall back to regular tuples:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

with DataZip(buffer, "w") as z:
    z["pt"] = Point(1.0, 2.0)
```

## Custom Classes

### Automatic Serialization

Any class with `__dict__` (i.e., not using `__slots__`) will be serialized automatically — no configuration needed:

```python
class Config:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

cfg = Config(0.01, 100)
with DataZip(buffer, "w") as z:
    z["cfg"] = cfg
```

### Classes with `__slots__`

Classes using `__slots__` are also handled automatically:

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Custom State Methods

For finer control, implement the standard pickle protocol:

```python
class MyClass:
    def __getstate__(self) -> dict:
        return {"data": self.data, "name": self.name}

    def __setstate__(self, state: dict) -> None:
        self.data = state["data"]
        self.name = state["name"]
```

### DataZip-specific State Methods

Use `_dzgetstate_` and `_dzsetstate_` when you need different behavior for DataZip vs. pickle. These take priority over `__getstate__`/`__setstate__` when DataZip is serializing:

```python
class MyClass:
    def _dzgetstate_(self) -> dict:
        # Exclude 'cache' attribute only for DataZip
        return {k: v for k, v in self.__dict__.items() if k != "cache"}

    def _dzsetstate_(self, state: dict) -> None:
        self.__dict__ = state
        self.cache = {}  # Reinitialize cache on load
```

### Priority Order

When serializing, DataZip checks for state methods in this order:

1. `_dzgetstate_` / `_dzsetstate_` (DataZip-specific)
2. `__getstate__` / `__setstate__` (standard pickle protocol)
3. Automatic `__dict__` / `__slots__` inspection

## Object Deduplication

By default, DataZip tracks object identities to avoid storing the same object multiple times. This means multiple references to the same object are deduplicated:

```python
shared = [1, 2, 3]
with DataZip(buffer, "w") as z:
    z["a"] = shared
    z["b"] = shared   # stored only once; on read, a and b will be the same list
```

!!! warning "Deduplication and object lifetime"
    Python reuses memory addresses for objects with non-overlapping lifetimes. If you create an object, store it, delete it, then create a new object that happens to get the same memory address, DataZip may incorrectly skip storing the new object.

    Use `z.reset_ids()` to clear the deduplication cache between such operations, or disable deduplication entirely with `ids_for_dedup=False`:

    ```python
    DataZip(buffer, "w", ids_for_dedup=False)
    ```

## Updating Archives

DataZip is write-once by design (a zip file constraint). To update an existing archive, use `DataZip.replace()`:

```python
# Replace values for specific keys; all other keys are copied unchanged
with DataZip.replace("data.zip", threshold=0.8) as z:
    z["new_feature"] = [1, 2, 3]
```

To keep the original file as a backup:

```python
with DataZip.replace("data.zip", save_old=True, threshold=0.8) as z:
    pass  # "data_old.zip" will be kept alongside the new "data.zip"
```

## Ignoring Unserializable Objects

DataZip will warn (not raise) when it encounters an object it cannot serialize (e.g., `functools.partial`, lambdas), and skip it. This means objects with unserializable attributes may be stored incompletely. Always define `__getstate__` to control exactly what gets stored.

## Deep Key Access

For nested DataZip structures (DataZips containing DataZips), use tuple keys for nested access:

```python
with DataZip(buffer, "r") as z:
    value = z[("outer_key", "inner_key")]
```
