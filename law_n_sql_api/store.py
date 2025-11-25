from __future__ import annotations
from typing import Any, Dict, List, Optional


class NetworkRoutesStore:
    """
    Simple in-memory store for `network.routes`.
    """

    def __init__(self) -> None:
        self._rows: List[Dict[str, Any]] = []

    def replace(self, rows: List[Dict[str, Any]]) -> None:
        self._rows = list(rows)

    def all(self) -> List[Dict[str, Any]]:
        return list(self._rows)

    def filtered(
        self,
        g_layer: Optional[str] = None,
        tower_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        rows = self._rows

        if g_layer is not None:
            rows = [r for r in rows if r.get("g_layer") == g_layer]

        if tower_id is not None:
            rows = [r for r in rows if r.get("tower_id") == tower_id]

        if limit is not None:
            rows = rows[:limit]

        return list(rows)


# single global store instance for this process
network_routes_store = NetworkRoutesStore()
