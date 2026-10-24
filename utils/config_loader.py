"""
Configuration Loader
Loads, validates, and merges YAML configuration with defaults.
Supports CLI argument overrides.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger("traffic_generator.config")

DEFAULT_CONFIG = {
    "target": {
        "url": "https://example.com",
        "pages": [],
    },
    "sessions": {
        "total": 10,
        "concurrent": 5,
        "delay_min": 15,
        "delay_max": 60,
        "pages_per_session_min": 1,
        "pages_per_session_max": 5,
    },
    "browser": {
        "headless": True,
        "engine": "chromium",
        "timeout": 30000,
    },
    "behavior": {
        "scroll": True,
        "scroll_speed": "random",
        "click_links": True,
        "mouse_movement": True,
        "random_pauses": True,
    },
    "referrers": {
        "organic_search_percent": 50,
        "social_percent": 20,
        "referral_percent": 20,
        "direct_percent": 10,
        "keywords": [
            "website traffic generator",
            "generate website traffic",
            "web traffic tool",
        ],
    },
    "devices": {
        "desktop_percent": 55,
        "mobile_percent": 40,
        "tablet_percent": 5,
    },
    "proxy": {
        "enabled": False,
        "file": "proxies.txt",
        "rotation": "random",
    },
    "output": {
        "logging": True,
        "log_file": "traffic_generator.log",
        "log_level": "INFO",
        "report_file": "report.json",
    },
}


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load configuration from YAML file with fallback to defaults.
    
    Args:
        config_path: Path to YAML config file.
        
    Returns:
        Merged configuration dictionary.
    """
    config = _deep_copy(DEFAULT_CONFIG)

    if config_path:
        path = Path(config_path)
        if path.exists():
            try:
                with open(path, "r") as f:
                    user_config = yaml.safe_load(f)
                if user_config:
                    config = _deep_merge(config, user_config)
                    logger.info(f"Config loaded: {config_path}")
            except yaml.YAMLError as e:
                logger.error(f"YAML parse error: {e}")
            except Exception as e:
                logger.error(f"Config load error: {e}")
        else:
            logger.debug(f"Config file not found: {config_path}")

    _validate(config)
    return config


def apply_overrides(config: Dict, **kwargs) -> Dict:
    """Apply CLI argument overrides to configuration."""
    if kwargs.get("url"):
        config["target"]["url"] = kwargs["url"]
    if kwargs.get("sessions"):
        config["sessions"]["total"] = kwargs["sessions"]
    if kwargs.get("concurrent"):
        config["sessions"]["concurrent"] = kwargs["concurrent"]
    if kwargs.get("proxy_file"):
        config["proxy"]["enabled"] = True
        config["proxy"]["file"] = kwargs["proxy_file"]
    if kwargs.get("headless") is not None:
        config["browser"]["headless"] = kwargs["headless"]
    if kwargs.get("browser_engine"):
        config["browser"]["engine"] = kwargs["browser_engine"]
    if kwargs.get("log_level"):
        config["output"]["log_level"] = kwargs["log_level"]
    if kwargs.get("report_file"):
        config["output"]["report_file"] = kwargs["report_file"]
    return config


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """Deep merge override into base dictionary."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _deep_copy(d: Dict) -> Dict:
    """Simple deep copy for nested dicts/lists."""
    import copy
    return copy.deepcopy(d)


def _validate(config: Dict):
    """Validate configuration values."""
    target = config.get("target", {}).get("url", "")
    if not target or target == "https://example.com":
        logger.warning("Target URL not configured. Update target.url in config.yaml")

    sessions = config.get("sessions", {})
    if sessions.get("concurrent", 5) > sessions.get("total", 10):
        config["sessions"]["concurrent"] = sessions["total"]

    # Validate percentages
    refs = config.get("referrers", {})
    ref_total = (
        refs.get("organic_search_percent", 0) +
        refs.get("social_percent", 0) +
        refs.get("referral_percent", 0) +
        refs.get("direct_percent", 0)
    )
    if ref_total != 100:
        logger.warning(f"Referrer percentages sum to {ref_total}%, not 100%")
