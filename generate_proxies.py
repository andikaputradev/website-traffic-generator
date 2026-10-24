#!/usr/bin/env python3
"""
High-Precision Proxy Generator & Validator
Fetches fresh public proxies from multiple reliable repositories,
validates them by making actual HTTPS requests to the target website,
and saves verified high-performance proxies to proxies.txt.
"""

import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
import logging
from typing import List, Set
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("proxy_validator")

SOURCES = [
    # ProxyScrape
    ("http", "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=3000&country=all&ssl=all&anonymity=all"),
    ("socks5", "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=3000&country=all"),
    # GitHub Lists
    ("socks5", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"),
    ("http", "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"),
    ("socks5", "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt"),
    ("http", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"),
    ("socks5", "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"),
    ("all", "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt"),
]

TARGET_URL = "https://andikadev.com/"

async def fetch_source(session: aiohttp.ClientSession, proto: str, url: str) -> Set[str]:
    proxies = set()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                text = await resp.text()
                for line in text.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "://" in line:
                        proxies.add(line)
                    else:
                        proxies.add(f"{proto}://{line}")
    except Exception as e:
        logger.debug(f"Failed to fetch {url}: {e}")
    return proxies

async def verify_proxy(proxy_url: str, sem: asyncio.Semaphore) -> bool:
    async with sem:
        try:
            connector = ProxyConnector.from_url(proxy_url, ssl=False)
            async with aiohttp.ClientSession(connector=connector) as session:
                timeout = aiohttp.ClientTimeout(total=7.0, connect=3.5)
                async with session.get(TARGET_URL, timeout=timeout) as resp:
                    if resp.status == 200:
                        return True
        except Exception:
            pass
        return False

async def main():
    logger.info("Fetching proxy candidates from upstream sources...")
    all_proxies: Set[str] = set()

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        fetch_tasks = [fetch_source(session, proto, url) for proto, url in SOURCES]
        results = await asyncio.gather(*fetch_tasks)
        for r in results:
            all_proxies.update(r)

    logger.info(f"Total raw proxies fetched: {len(all_proxies)}")
    if not all_proxies:
        return

    candidates = list(all_proxies)
    random.shuffle(candidates)

    # Test candidates in batches until we find at least 25-50 verified working proxies
    logger.info(f"Validating proxies directly against {TARGET_URL}...")
    verified: List[str] = []
    batch_size = 600
    sem = asyncio.Semaphore(120)

    for i in range(0, min(len(candidates), 2400), batch_size):
        batch = candidates[i : i + batch_size]
        logger.info(f"Testing batch {i // batch_size + 1} ({len(batch)} proxies)...")

        async def check_and_record(p: str):
            ok = await verify_proxy(p, sem)
            if ok:
                verified.append(p)
                logger.info(f"[VERIFIED] {p} -> HTTP 200 OK! (Total: {len(verified)})")

        tasks = [check_and_record(p) for p in batch]
        await asyncio.gather(*tasks, return_exceptions=True)

        if len(verified) >= 30:
            logger.info("Found enough verified working proxies!")
            break

    logger.info(f"Validation complete: {len(verified)} proxies confirmed working on target.")

    if verified:
        with open("proxies.txt", "w", encoding="utf-8") as f:
            f.write("# Verified proxies tested directly against target website\n")
            for p in verified:
                f.write(f"{p}\n")
        logger.info(f"Saved {len(verified)} working proxies to proxies.txt")

if __name__ == "__main__":
    asyncio.run(main())
