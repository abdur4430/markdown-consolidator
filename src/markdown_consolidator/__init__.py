"""
Markdown Consolidator - Intelligent consolidation and synthesis of markdown files.

This package provides tools for consolidating multiple markdown files with
overlapping content and different update dates, commonly produced by AI-assisted
workflows.
"""

__version__ = "0.1.0"

from .consolidator import consolidate, ConsolidationResult
from .inventory import inventory_directory, analyze_file
from .relationships import analyze_relationships
from .clustering import cluster_files
from .synthesis import synthesize_cluster

__all__ = [
    "__version__",
    "consolidate",
    "ConsolidationResult",
    "inventory_directory",
    "analyze_file",
    "analyze_relationships",
    "cluster_files",
    "synthesize_cluster",
]
