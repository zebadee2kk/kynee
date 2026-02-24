"""Main CLI entry point."""

import argparse
import asyncio
import sys
from pathlib import Path

import structlog

from kynee_agent import __version__
from kynee_agent.core import Agent

logger = structlog.get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="kynee-agent",
        description="KYNEĒ autonomous penetration testing agent",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start the agent daemon")
    start_parser.add_argument(
        "--config",
        "-c",
        type=str,
        help="Path to configuration file",
    )

    # Enroll command
    enroll_parser = subparsers.add_parser("enroll", help="Enroll agent with console")
    enroll_parser.add_argument(
        "--console",
        "-C",
        type=str,
        required=True,
        help="Console URL (e.g., https://console.example.com)",
    )
    enroll_parser.add_argument(
        "--token",
        "-t",
        type=str,
        required=True,
        help="One-time enrollment token",
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Show agent status")
    status_parser.add_argument(
        "--config",
        "-c",
        type=str,
        help="Path to configuration file",
    )

    return parser


async def cmd_start(args: argparse.Namespace) -> int:
    """Handle 'start' command."""
    agent = Agent(config_path=args.config)
    try:
        await agent.start()
        # Keep running until interrupted
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("shutdown_requested")
        await agent.stop()
        return 0
    except Exception as e:
        logger.error("startup_failed", error=str(e))
        return 1


async def cmd_enroll(args: argparse.Namespace) -> int:
    """Handle 'enroll' command."""
    logger.info(
        "enrollment_started",
        console=args.console,
    )
    # TODO: Implement enrollment handshake
    logger.info("enrollment_pending", message="Enrollment flow not yet implemented")
    return 0


async def cmd_status(args: argparse.Namespace) -> int:
    """Handle 'status' command."""
    agent = Agent(config_path=args.config)
    status = agent.get_status()
    logger.info("agent_status", **status)
    return 0


async def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Configure logging
    if args.verbose:
        level = "debug"
    else:
        level = "info"

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    if not args.command:
        parser.print_help()
        return 0

    try:
        if args.command == "start":
            return await cmd_start(args)
        elif args.command == "enroll":
            return await cmd_enroll(args)
        elif args.command == "status":
            return await cmd_status(args)
        else:
            logger.error("unknown_command", command=args.command)
            return 1
    except Exception as e:
        logger.error("unexpected_error", error=str(e), exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
