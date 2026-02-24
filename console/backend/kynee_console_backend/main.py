"""Main entry point for console backend."""

import uvicorn

from kynee_console_backend.app import create_app


def main() -> None:
    """Run the console backend."""
    app = create_app()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
