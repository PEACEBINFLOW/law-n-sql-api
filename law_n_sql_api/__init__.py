"""
law_n_sql_api

Minimal HTTP API exposing Law-N N-SQL over an in-memory `network.routes` table.
"""

from .main import app  # FastAPI app

__all__ = ["app"]
