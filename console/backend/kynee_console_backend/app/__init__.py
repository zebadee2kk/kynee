"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from kynee_console_backend import __version__

logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="KYNEĒ Console API",
        description="Backend API for KYNEĒ penetration testing platform",
        version=__version__,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure from environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": __version__,
        }

    # API v1 routes (to be added)
    # from kynee_console_backend.routers import agents, engagements, findings
    # app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
    # app.include_router(engagements.router, prefix="/api/v1", tags=["engagements"])
    # app.include_router(findings.router, prefix="/api/v1", tags=["findings"])

    logger.info("app_created", version=__version__)

    return app
