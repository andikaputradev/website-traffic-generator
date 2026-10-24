"""
Proxy Pool Manager
Handles loading, parsing, rotation, and health tracking of HTTP/SOCKS5 proxies.
"""

import random
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger("traffic_generator.proxy_pool")


class ProxyPool:
    """
    Manages a pool of proxies with multiple rotation strategies.
    
    Supports:
    - HTTP, HTTPS, and SOCKS5 proxy protocols
    - Round-robin, random, and per-session rotation
    - Automatic health tracking and failed proxy removal
    - Loading from file or inline configuration
    """

    def __init__(self, proxy_config: Dict):
        self.config = proxy_config
        self.proxies: List[Dict] = []
        self.rotation = proxy_config.get("rotation", "random")
        self.current_index = 0
        self.failed: set = set()

        self._load_proxies()

    def _load_proxies(self):
        """Load proxies from configured source."""
        # Try file first
        proxy_file = self.config.get("file", "")
        if proxy_file and Path(proxy_file).exists():
            self._load_from_file(proxy_file)
        elif self.config.get("list"):
            self._load_from_list(self.config["list"])
        else:
            logger.warning("No proxy source configured. Running without proxies.")

    def _load_from_file(self, filepath: str):
        """
        Load proxies from a text file.
        
        Supported formats per line:
        - protocol://user:pass@host:port
        - protocol://host:port
        - host:port (assumes http)
        - user:pass@host:port (assumes http)
        """
        try:
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    proxy = self._parse(line)
                    if proxy:
                        self.proxies.append(proxy)

            logger.info(f"Loaded {len(self.proxies)} proxies from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load proxy file: {e}")

    def _load_from_list(self, proxy_list: List[str]):
        """Load proxies from inline configuration list."""
        for entry in proxy_list:
            proxy = self._parse(entry)
            if proxy:
                self.proxies.append(proxy)
        logger.info(f"Loaded {len(self.proxies)} proxies from config")

    def _parse(self, proxy_str: str) -> Optional[Dict]:
        """Parse a proxy string into Playwright-compatible format."""
        try:
            proxy_str = proxy_str.strip()

            # Determine protocol
            if "://" in proxy_str:
                protocol, remainder = proxy_str.split("://", 1)
            else:
                protocol = "http"
                remainder = proxy_str

            # Parse authentication
            username = None
            password = None

            if "@" in remainder:
                auth, host_part = remainder.rsplit("@", 1)
                if ":" in auth:
                    username, password = auth.split(":", 1)
                else:
                    username = auth
            else:
                host_part = remainder

            # Build proxy dict
            proxy = {"server": f"{protocol}://{host_part}"}
            if username:
                proxy["username"] = username
            if password:
                proxy["password"] = password

            return proxy

        except Exception as e:
            logger.warning(f"Failed to parse proxy '{proxy_str}': {e}")
            return None

    def get_next(self) -> Optional[Dict]:
        """
        Get the next proxy based on rotation strategy.
        
        Returns:
            Playwright-compatible proxy dict, or None if no proxies available.
        """
        if not self.proxies:
            return None

        # Filter out failed proxies
        available = [
            p for p in self.proxies if p["server"] not in self.failed
        ]

        if not available:
            logger.warning("All proxies failed. Resetting pool...")
            self.failed.clear()
            available = self.proxies

        if self.rotation == "round_robin":
            proxy = available[self.current_index % len(available)]
            self.current_index += 1
        elif self.rotation == "random":
            proxy = random.choice(available)
        elif self.rotation == "per_session":
            proxy = random.choice(available)
        else:
            proxy = random.choice(available)

        return proxy

    def mark_failed(self, server: str):
        """Mark a proxy server as failed."""
        self.failed.add(server)
        logger.debug(f"Proxy marked failed: {server}")

    @property
    def total_count(self) -> int:
        """Total number of proxies in the pool."""
        return len(self.proxies)

    @property
    def active_count(self) -> int:
        """Number of active (non-failed) proxies."""
        return len(self.proxies) - len(self.failed)

    def get_stats(self) -> Dict:
        """Get proxy pool statistics."""
        return {
            "total": self.total_count,
            "active": self.active_count,
            "failed": len(self.failed),
            "rotation": self.rotation,
        }
