from __future__ import annotations
from typing import Any, Dict, List, Optional


class NsqlEngineWrapper:
    """
    Thin wrapper around `law-n-sql-core`'s execution entrypoint.

    We try to import the engine lazily. If unavailable, we signal that
    to the caller.
    """

    def __init__(self) -> None:
        self._engine = self._try_load_engine()

    def _try_load_engine(self):
        try:
            from law_n_sql_core.engine import execute_query  # type: ignore
            return execute_query
        except Exception:
            return None

    def available(self) -> bool:
        return self._engine is not None

    def query(
        self,
        query: str,
        tables: Dict[str, List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        if not self._engine:
            raise RuntimeError(
                "N-SQL engine not available. Install `law-n-sql-core` and ensure it is importable."
            )
        engine = self._engine
        # adjust if the core API is different
        result = engine(query, tables=tables)  # type: ignore[arg-type]
        return result


nsql_engine = NsqlEngineWrapper()
