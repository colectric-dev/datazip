# Installation

## Requirements

- Python ≥ 3.13

## Basic Installation

```bash
pip install datazip
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add datazip
```

## Core Dependencies

These are installed automatically:

| Package | Purpose |
|---|---|
| `pandas` | DataFrame and Series serialization |
| `polars` | Polars DataFrame/Series serialization |
| `pyarrow` | Parquet file format for tabular data |
| `numpy` | Array serialization |
| `orjson` | Fast JSON encoding/decoding |
| `pyyaml` | YAML support |
| `platformdirs` | Platform-specific directory paths |

## Optional Dependencies

Some types require additional packages:

```bash
# Plotly figure support
pip install plotly

# SQLAlchemy engine support
pip install sqlalchemy
```

## Development Installation

To install with all development dependencies (including test tools):

```bash
pip install datazip[dev]
```

Or clone the repository and install in editable mode:

```bash
git clone https://github.com/colectric-dev/datazip.git
cd datazip
pip install -e ".[dev]"
```
