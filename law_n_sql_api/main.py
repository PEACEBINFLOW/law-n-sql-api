from __future__ import annotations
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .config import settings
from .store import network_routes_store
from .engine import nsql_engine


class NetworkRoutesLoadPayload(BaseModel):
    rows: List[Dict[str, Any]]


class NsqlQueryPayload(BaseModel):
    query: str


app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tables/network-routes")
def get_network_routes(
    g_layer: Optional[str] = Query(default=None),
    tower_id: Optional[str] = Query(default=None),
    limit: Optional[int] = Query(default=100, ge=1, le=10000),
) -> Dict[str, Any]:
    rows = network_routes_store.filtered(
        g_layer=g_layer,
        tower_id=tower_id,
        limit=limit,
    )
    return {
        "count": len(rows),
        "rows": rows,
    }


@app.post("/tables/network-routes/load")
def load_network_routes(payload: NetworkRoutesLoadPayload) -> Dict[str, Any]:
    network_routes_store.replace(payload.rows)
    return {
        "status": "ok",
        "row_count": len(payload.rows),
    }


@app.post("/query/nsql")
def query_nsql(payload: NsqlQueryPayload) -> Dict[str, Any]:
    if not nsql_engine.available():
        return {
            "engine_available": False,
            "error": "N-SQL engine not available. Install `law-n-sql-core` and ensure it is importable.",
        }

    rows = network_routes_store.all()
    if not rows:
        raise HTTPException(status_code=400, detail="No rows in `network.routes` table.")

    # hardcode the table name for now; can expand later
    tables = {"network.routes": rows}

    try:
        result = nsql_engine.query(payload.query, tables=tables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"N-SQL execution error: {e}")

    return {
        "engine_available": True,
        "row_count": len(result),
        "rows": result,
    }


def run() -> None:
    """
    Convenience entrypoint for `python -m` or `law-n-sql-api` script.
    """
    import uvicorn

    uvicorn.run("law_n_sql_api.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
