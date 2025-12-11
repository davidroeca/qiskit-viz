"""Qiskit Viz API - Main application entry point."""

import logging
import logging.config
import typing as t
from fastapi import FastAPI
from starlette.routing import BaseRoute, Route

from src.schemas import RootResponse
from src.routes import router

app = FastAPI(
    title="Qiskit Viz API",
    version="0.1.0",
    root_path="/api",
)


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "qiskit_viz_backend": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(log_config)


def _is_route(base_route: BaseRoute) -> t.TypeGuard[Route]:
    """Silences type checker; consider more robust alternatives if relied upon more heavily."""
    return hasattr(base_route, "path") and hasattr(base_route, "methods")


@app.get("/", response_model=RootResponse)
def read_root():
    """Get API information and available endpoints."""
    # Dynamically generate endpoint list from registered routes
    endpoints: list[str] = []
    for route in app.routes:
        if _is_route(route) and route.methods:
            for method in route.methods:
                if method != "HEAD":  # Skip HEAD methods
                    endpoints.append(f"{method} {route.path}")

    return RootResponse(
        message="Qiskit Viz API v1",
        api_prefix="/api",
        endpoints=sorted(endpoints),
    )


# Include API router
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
