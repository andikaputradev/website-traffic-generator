"""
Traffic Reporter
Generates detailed JSON reports and formatted terminal summaries
of website traffic generation results.
"""

import json
import time
import logging
from typing import Dict, List
from collections import Counter

from rich.console import Console
from rich.table import Table

logger = logging.getLogger("traffic_generator.reporter")


class TrafficReporter:
    """
    Generates comprehensive reports from traffic generation sessions.
    Outputs JSON files and formatted Rich terminal tables.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.console = Console()
        self.output_cfg = config.get("output", {})

    def save_report(self, results: List[Dict], summary: Dict):
        """Save a detailed JSON report."""
        report_file = self.output_cfg.get("report_file", "report.json")

        report = {
            "metadata": {
                "tool": "Website Traffic Generator v1.0.0",
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "target_url": self.config.get("target", {}).get("url", ""),
                "total_sessions": self.config.get("sessions", {}).get("total", 0),
                "concurrent": self.config.get("sessions", {}).get("concurrent", 0),
                "proxy_enabled": self.config.get("proxy", {}).get("enabled", False),
                "browser_engine": self.config.get("browser", {}).get("engine", "chromium"),
            },
            "summary": summary,
            "sessions": [
                {
                    "id": r.get("session_id"),
                    "status": r.get("status"),
                    "device": r.get("device_type"),
                    "pages": r.get("pages_visited"),
                    "duration_sec": r.get("total_time"),
                    "referrer_type": r.get("referrer_type"),
                    "referrer_url": r.get("referrer"),
                    "proxy": r.get("proxy"),
                    "viewport": r.get("viewport"),
                    "pages_visited": r.get("pages_list", [])[:5],
                    "errors": r.get("errors", []),
                }
                for r in results
            ],
        }

        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Report saved: {report_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")

    def print_summary(self, summary: Dict):
        """Print a formatted summary to the terminal."""
        self.console.print()

        # Main metrics table
        table = Table(
            title="Website Traffic Generator - Results Summary",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Metric", style="bold white")
        table.add_column("Value", justify="right", style="green")

        table.add_row("Total Sessions", str(summary.get("total_sessions", 0)))
        table.add_row(
            "Completed",
            f"[green]{summary.get('completed', 0)}[/green]"
        )
        table.add_row(
            "Failed",
            f"[red]{summary.get('failed', 0)}[/red]"
        )
        table.add_row(
            "Success Rate",
            f"{summary.get('success_rate', 0)}%"
        )
        table.add_row(
            "Total Pages Visited",
            str(summary.get("total_pages_visited", 0))
        )
        table.add_row(
            "Avg Session Duration",
            f"{summary.get('average_session_duration', 0):.1f}s"
        )
        table.add_row(
            "Avg Pages/Session",
            f"{summary.get('average_pages_per_session', 0):.1f}"
        )
        table.add_row(
            "Total Run Time",
            f"{summary.get('total_run_time', 0):.1f}s"
        )

        self.console.print(table)

        # Device breakdown
        device_data = summary.get("device_breakdown", {})
        if device_data:
            self.console.print()
            dev_table = Table(title="Device Distribution", header_style="bold blue")
            dev_table.add_column("Device", style="bold")
            dev_table.add_column("Count", justify="right")
            dev_table.add_column("Percent", justify="right")
            for device, info in device_data.items():
                dev_table.add_row(
                    device.capitalize(),
                    str(info["count"]),
                    f"{info['percent']}%",
                )
            self.console.print(dev_table)

        # Referrer breakdown
        ref_data = summary.get("referrer_breakdown", {})
        if ref_data:
            self.console.print()
            ref_table = Table(title="Traffic Source Distribution", header_style="bold magenta")
            ref_table.add_column("Source", style="bold")
            ref_table.add_column("Count", justify="right")
            ref_table.add_column("Percent", justify="right")
            for source, info in ref_data.items():
                ref_table.add_row(
                    source.replace("_", " ").title(),
                    str(info["count"]),
                    f"{info['percent']}%",
                )
            self.console.print(ref_table)

        self.console.print()
