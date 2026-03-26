"""Datazip."""

import logging

# Create a root logger for use anywhere within the package.
logger = logging.getLogger("datazip")

try:
    from datazip._version import version as __version__
except ImportError:
    logger.warning("Version unknown because package is not installed.")
    __version__ = "unknown"
