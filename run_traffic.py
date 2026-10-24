#!/usr/bin/env python3
"""
Website Traffic Generator - Main Entry Point
An open-source, automated website traffic generator with realistic human behavior.

Usage:
    python run_traffic.py --url "https://yourwebsite.com" --sessions 100
    python run_traffic.py --config config.yaml
    python run_traffic.py --url "https://yourwebsite.com" --proxy-file proxies.txt --sessions 500 --concurrent 20
"""

import argparse
import asyncio
import sys
import logging
from pathlib import Path

# Ensure UTF-8 console output on Windows
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.config_loader import load_config, apply_overrides
from core.generator import WebsiteTrafficGenerator
from reports.reporter import TrafficReporter


def setup_logging(config: dict) -> logging.Logger:
    """Configure logging based on configuration settings."""
    output_config = config.get("output", {})
    log_level = getattr(logging, output_config.get("log_level", "INFO").upper())
    log_file = output_config.get("log_file", "traffic_generator.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger("traffic_generator")
    root_logger.setLevel(log_level)

    # Ensure UTF-8 output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    if output_config.get("logging", True):
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return root_logger


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="website-traffic-generator",
        description=(
            "Website Traffic Generator - Generate realistic, high-quality "
            "website visitors with human behavior simulation, proxy rotation, "
            "and comprehensive traffic source spoofing."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url "https://example.com" --sessions 50
  %(prog)s --config config.yaml
  %(prog)s --url "https://example.com" --proxy-file proxies.txt --sessions 200 --concurrent 20
  %(prog)s --url "https://example.com" --sessions 10 --visible
        """,
    )

    # Target
    parser.add_argument(
        "--url", type=str,
        help="Target website URL to generate traffic for",
    )
    parser.add_argument(
        "--config", type=str, default="config.yaml",
        help="Path to YAML configuration file (default: config.yaml)",
    )

    # Session settings
    parser.add_argument(
        "--sessions", type=int,
        help="Total number of visitor sessions to generate",
    )
    parser.add_argument(
        "--concurrent", type=int,
        help="Maximum number of concurrent browser sessions",
    )

    # Proxy settings
    parser.add_argument(
        "--proxy-file", type=str,
        help="Path to proxy list file (one proxy per line)",
    )

    # Browser settings
    parser.add_argument(
        "--visible", action="store_true",
        help="Run browsers in visible mode (not headless) for debugging",
    )
    parser.add_argument(
        "--browser", type=str, choices=["chromium", "firefox", "webkit"],
        default="chromium",
        help="Browser engine to use (default: chromium)",
    )

    # Output settings
    parser.add_argument(
        "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging verbosity level",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress terminal output (only log to file)",
    )
    parser.add_argument(
        "--report", type=str,
        help="Path to save the JSON traffic report",
    )

    return parser.parse_args()


def print_banner(config: dict):
    """Display the startup banner with configuration summary."""
    target = config.get("target", {}).get("url", "N/A")
    sessions = config.get("sessions", {}).get("total", 0)
    concurrent = config.get("sessions", {}).get("concurrent", 0)
    proxy_enabled = config.get("proxy", {}).get("enabled", False)
    browser = config.get("browser", {}).get("engine", "chromium")

    banner = f"""
=====================================================================
               WEBSITE TRAFFIC GENERATOR v1.0.0
         Realistic Automated Website Visitor Simulation
=====================================================================
  Target URL:    {target}
  Sessions:      {sessions}
  Concurrent:    {concurrent}
  Browser:       {browser}
  Proxies:       {"Enabled (" + config.get("proxy", {}).get("rotation", "random") + ")" if proxy_enabled else "Disabled"}
=====================================================================
"""
    try:
        print(banner)
    except Exception:
        pass


async def main():
    """Main execution function."""
    args = parse_arguments()

    # Load configuration
    config = load_config(args.config)

    # Apply CLI overrides
    overrides = {}
    if args.url:
        overrides["url"] = args.url
    if args.sessions:
        overrides["sessions"] = args.sessions
    if args.concurrent:
        overrides["concurrent"] = args.concurrent
    if args.proxy_file:
        overrides["proxy_file"] = args.proxy_file
    if args.visible:
        overrides["headless"] = False
    if args.browser:
        overrides["browser_engine"] = args.browser
    if args.log_level:
        overrides["log_level"] = args.log_level
    if args.report:
        overrides["report_file"] = args.report

    config = apply_overrides(config, **overrides)

    # Setup logging
    logger = setup_logging(config)

    # Validate target URL
    target_url = config.get("target", {}).get("url", "")
    if not target_url or target_url == "https://example.com":
        logger.error(
            "No target URL specified. Use --url or set target.url in config.yaml"
        )
        sys.exit(1)

    # Print banner
    if not args.quiet:
        print_banner(config)

    # Initialize and run the generator
    generator = WebsiteTrafficGenerator(config)

    logger.info("Starting website traffic generation...")
    results = await generator.run()

    # Generate report
    reporter = TrafficReporter(config)
    summary = generator.get_summary()
    reporter.save_report(results, summary)

    if not args.quiet:
        reporter.print_summary(summary)

    logger.info("Website traffic generation complete.")
    return results


if __name__ == "__main__":
    asyncio.run(main())
