"""Dummy modules and classes when optional packages are not installed.

Could do something more like this:
https://github.com/pola-rs/polars/blob/master/py-polars/polars/dependencies.py
"""

try:
    import sqlalchemy
except (ModuleNotFoundError, ImportError):

    class sqlalchemy:  # noqa: N801
        """Dummy for :mod:`sqlalchemy` when not installed."""

        class engine:  # noqa: N801
            """Dummy for :mod:`sqlalchemy.engine` when not installed."""

            class Engine:
                """Dummy for :mod:`sqlalchemy.engine.Engine` when not installed."""

                pass

        @staticmethod
        def create_engine(*args, **kwargs):
            """Dummy for :func:`sqlalchemy.create_engine` when not installed."""
            pass


try:
    import plotly
except (ModuleNotFoundError, ImportError):

    class plotly:  # noqa: N801
        """Dummy for :mod:`plotly` when not installed."""

        class graph_objects:  # noqa: N801
            """Dummy for :mod:`plotly.graph_objects` when not installed."""

            class Figure:
                """Dummy for :mod:`plotly.graph_objects.Figure` when not installed."""

                pass


try:
    import numpy

except (ModuleNotFoundError, ImportError):

    class numpy:  # noqa: N801
        """Dummy for :mod:`numpy` when not installed."""

        class ndarray:  # noqa: N801
            """Dummy for :mod:`numpy.ndarray` when not installed."""

            pass

        class int64:  # noqa: N801
            """Dummy for :mod:`numpy.int64` when not installed."""

            pass

        class float64:  # noqa: N801
            """Dummy for :mod:`numpy.float64` when not installed."""

            pass

        def load(*args, **kwargs):
            """Dummy for :func:`numpy.load` when not installed."""
            pass

        def save(*args, **kwargs):
            """Dummy for :func:`numpy.save` when not installed."""
            pass


try:
    import pandas

    if pandas.__version__ < "2.0.0":
        raise ImportError("pandas < 2.0.0")

except (ModuleNotFoundError, ImportError):

    class pandas:  # noqa: N801
        """Dummy for when pandas is not installed."""

        class DataFrame:
            """Dummy for when pandas is not installed."""

            def to_parquet(*args, **kwargs):
                """Dummy for when pandas is not installed."""
                pass

        class Series:
            """Dummy for when pandas is not installed."""

            def to_frame(*args, **kwargs):
                """Dummy for when pandas is not installed."""
                pass

        class Timestamp:
            """Dummy for when pandas is not installed."""

            pass

        def read_parquet(*args, **kwargs):
            """Dummy for when pandas is not installed."""
            pass


try:
    import polars

except (ModuleNotFoundError, ImportError):

    class polars:  # noqa: N801
        """Dummy for when polars is not installed."""

        class DataFrame:
            """Dummy for when polars is not installed."""

            def write_parquet(*args, **kwargs):
                """Dummy for when polars is not installed."""
                pass

        class LazyFrame:
            """Dummy for when polars is not installed."""

            def collect(*args, **kwargs):
                """Dummy for when polars is not installed."""
                pass

        class Series:
            """Dummy for when polars is not installed."""

            def to_frame(*args, **kwargs):
                """Dummy for when polars is not installed."""
                pass

        def read_parquet(*args, **kwargs):
            """Dummy for when polars is not installed."""
            pass
