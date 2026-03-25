# Quick Start

## Basic Read and Write

`DataZip` works like a dictionary. Use it as a context manager for clean resource handling:

```python
from pathlib import Path
import pandas as pd
import numpy as np
from datazip import DataZip

# Write data to a .zip file
with DataZip(Path("my_data.zip"), "w") as z:
    z["dataframe"] = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
    z["array"] = np.array([1, 2, 3, 4])
    z["config"] = {"alpha": 0.01, "tags": ["x", "y"]}
    z["values"] = {1, 2, 3}

# Read data back
with DataZip(Path("my_data.zip"), "r") as z:
    df = z["dataframe"]
    arr = z["array"]
    config = z["config"]
```

!!! note
    DataZip automatically appends `.zip` to `Path` arguments if the suffix is missing.

## Serializing a Single Object

Use `DataZip.dump()` and `DataZip.load()` to serialize and deserialize a single object directly:

```python
from datazip import DataZip

class MyModel:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

model = MyModel(weights=[0.1, 0.5, 0.9], bias=0.01)

# Save
DataZip.dump(model, "model.zip")

# Load
restored = DataZip.load("model.zip")
print(restored.weights)  # [0.1, 0.5, 0.9]
```

## Using IOMixin

For custom classes, inherit from `IOMixin` to get `to_file()` and `from_file()` methods automatically:

```python
import numpy as np
import pandas as pd
from datazip import IOMixin

class MyAnalysis(IOMixin):
    def __init__(self, name: str, data: pd.DataFrame):
        self.name = name
        self.data = data
        self.results = None

analysis = MyAnalysis("experiment_1", pd.DataFrame({"x": range(10)}))
analysis.results = np.array([0.1, 0.2, 0.3])

# Save
analysis.to_file("analysis.zip")

# Load
loaded = MyAnalysis.from_file("analysis.zip")
print(loaded.name)     # experiment_1
print(loaded.results)  # [0.1, 0.2, 0.3]
```

## Checking Contents

```python
with DataZip("my_data.zip", "r") as z:
    # List all keys
    print(list(z.keys()))

    # Check if a key exists
    print("dataframe" in z)

    # Number of items
    print(len(z))

    # Iterate over items
    for key, value in z.items():
        print(key, type(value))
```

## Updating a DataZip

Because zip files are write-once, use `DataZip.replace()` to update an existing archive:

```python
# Add or update keys; existing keys not in kwargs are copied over unchanged
with DataZip.replace("my_data.zip", config={"alpha": 0.05}) as z:
    z["new_key"] = "new value"
```

!!! warning
    Keys copied from the old archive cannot be reliably mutated inside the `replace` block.
    Use `kwargs` to replace values for existing keys.

## Working with Buffers

DataZip works with in-memory buffers (`BytesIO`) as well as files — useful for testing or passing data without touching disk:

```python
from io import BytesIO
from datazip import DataZip

buffer = BytesIO()
with DataZip(buffer, "w") as z:
    z["x"] = [1, 2, 3]

with DataZip(buffer, "r") as z:
    print(z["x"])  # [1, 2, 3]
```

## Handling Custom Classes with Unserializable Attributes

If your class has attributes that cannot be serialized (e.g., lambdas, open file handles), define `__getstate__` and `__setstate__`:

```python
from collections import defaultdict
from datazip import IOMixin

class MyClass(IOMixin):
    def __init__(self):
        self.data = defaultdict(lambda: 0)

    def __getstate__(self):
        # Convert defaultdict to a plain dict for serialization
        return {"data": dict(self.data)}

    def __setstate__(self, state):
        # Restore defaultdict from the plain dict
        self.data = defaultdict(lambda: 0, state["data"])
```

For DataZip-specific exclusions (e.g., skip certain attributes only when saving to DataZip, not when pickling), use `_dzgetstate_` and `_dzsetstate_` instead.
