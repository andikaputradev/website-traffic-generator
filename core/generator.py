"""
Website Traffic Generator - Core Engine
Orchestrates browser sessions with human behavior simulation,
proxy rotation, traffic source management, and ultra-lightweight execution.
"""

import asyncio
import random
import time
import logging
from typing import Optional, Dict, List
from urllib.parse import urlparse
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from core.behavior import HumanBehaviorEngine
from utils.user_agents import UserAgentManager
from utils.referrers import ReferrerManager
from utils.proxy_pool import ProxyPool

logger = logging.getLogger("traffic_generator.core")


class VisitorSession:
    """
    Represents a single simulated visitor session.
    Manages navigation, human behavior simulation, and multi-page browsing.
    """

    def __init__(
        self,
        session_id: int,
        config: Dict,
        proxy_pool: Optional[ProxyPool] = None,
        ua_manager: Optional[UserAgentManager] = None,
        ref_manager: Optional[ReferrerManager] = None,
    ):
        self.session_id = session_id
        self.config = config
        self.proxy_pool = proxy_pool
        self.ua_manager = ua_manager or UserAgentManager(config)
        self.ref_manager = ref_manager or ReferrerManager(config)
        self.behavior = HumanBehaviorEngine(config)

        self.stats = {
            "session_id": session_id,
            "pages_visited": 0,
            "total_time": 0,
            "start_time": None,
            "end_time": None,
            "referrer": None,
            "referrer_type": None,
            "user_agent": None,
            "device_type": None,
            "proxy": None,
            "viewport": None,
            "status": "pending",
            "pages_list": [],
            "errors": [],
        }

    def _select_viewport(self, device_type: str) -> Dict[str, int]:
        """Select a realistic viewport size based on device type."""
        viewports = {
            "desktop": [
                {"width": 1920, "height": 1080},
                {"width": 1366, "height": 768},
                {"width": 1536, "height": 864},
                {"width": 1440, "height": 900},
                {"width": 1280, "height": 720},
            ],
            "mobile": [
                {"width": 390, "height": 844},
                {"width": 393, "height": 852},
                {"width": 412, "height": 915},
                {"width": 360, "height": 800},
                {"width": 414, "height": 896},
            ],
            "tablet": [
                {"width": 768, "height": 1024},
                {"width": 820, "height": 1180},
                {"width": 834, "height": 1194},
            ],
        }
        return random.choice(viewports.get(device_type, viewports["desktop"]))

    async def execute(self, shared_browser: Optional[Browser] = None) -> Dict:
        """Execute the full visitor session lifecycle using lightweight browser context."""
        self.stats["start_time"] = time.time()
        self.stats["status"] = "running"

        # Select session parameters
        user_agent, device_type = self.ua_manager.get_random()
        referrer, referrer_type = self.ref_manager.get_random()
        viewport = self._select_viewport(device_type)

        self.stats["user_agent"] = user_agent
        self.stats["device_type"] = device_type
        self.stats["referrer"] = referrer
        self.stats["referrer_type"] = referrer_type
        self.stats["viewport"] = viewport

        # Target and session configuration
        base_url = self.config.get("target", {}).get("url", "").rstrip("/")
        configured_pages = self.config.get("target", {}).get("pages", [])
        session_cfg = self.config.get("sessions", {})
        pages_min = session_cfg.get("pages_per_session_min", 2)
        pages_max = session_cfg.get("pages_per_session_max", 4)
        target_pages = random.randint(pages_min, pages_max)

        # Determine landing page
        landing_url = base_url
        if configured_pages and random.random() < 0.75:
            chosen = random.choice(configured_pages)
            if chosen.startswith("http://") or chosen.startswith("https://"):
                landing_url = chosen
            else:
                landing_url = base_url + ("" if chosen.startswith("/") else "/") + chosen

        timeout = self.config.get("browser", {}).get("timeout", 30000)
        max_attempts = 4 if self.proxy_pool else 1

        owns_browser = False
        browser = shared_browser

        for attempt in range(max_attempts):
            # Try rotating proxy, or fallback to direct on last attempt
            proxy = None
            if self.proxy_pool and attempt < max_attempts - 1:
                proxy = self.proxy_pool.get_next()
            
            self.stats["proxy"] = proxy.get("server", "direct") if proxy else "direct"
            context = None

            try:
                # If no shared browser, launch an isolated one
                if not browser:
                    owns_browser = True
                    playwright_cm = async_playwright()
                    p = await playwright_cm.start()
                    engine = self.config.get("browser", {}).get("engine", "chromium")
                    browser_type = getattr(p, engine, p.chromium)
                    browser = await browser_type.launch(
                        headless=self.config.get("browser", {}).get("headless", True),
                        args=["--no-sandbox", "--disable-dev-shm-usage", "--mute-audio"]
                    )

                # Context options
                ctx_opts = {
                    "viewport": viewport,
                    "user_agent": user_agent,
                    "ignore_https_errors": True,
                    "locale": random.choice(["id-ID", "en-US", "id", "en"]),
                    "timezone_id": random.choice([
                        "Asia/Jakarta", "Asia/Makassar", "Asia/Jayapura", "Asia/Singapore"
                    ]),
                    "color_scheme": random.choice(["light", "dark", "no-preference"]),
                }

                if proxy:
                    ctx_opts["proxy"] = proxy

                if referrer:
                    ctx_opts["extra_http_headers"] = {"Referer": referrer}

                context = await browser.new_context(**ctx_opts)
                page = await context.new_page()

                # Resource blocker for maximum speed and minimal memory/CPU usage
                async def block_heavy_assets(route, request):
                    if request.resource_type in ["image", "media", "font"]:
                        await route.abort()
                    else:
                        await route.continue_()

                await page.route("**/*", block_heavy_assets)

                # Navigate to landing target
                logger.info(
                    f"Session {self.session_id}: Visiting {landing_url} "
                    f"[{device_type}] (ref: {referrer_type or 'direct'}) via {self.stats['proxy']}"
                )

                nav_timeout = 15000 if proxy else timeout
                goto_attempts = 3 if not proxy else 1
                for g_att in range(goto_attempts):
                    try:
                        await page.goto(landing_url, wait_until="domcontentloaded", timeout=nav_timeout)
                        break
                    except Exception as goto_err:
                        if g_att < goto_attempts - 1:
                            await asyncio.sleep(2.0)
                        else:
                            raise goto_err

                self.stats["pages_visited"] += 1
                self.stats["pages_list"].append(landing_url)

                # Human behavior + interactive content clicking on landing page
                await self.behavior.simulate_landing_page(page)

                # Multi-page browsing
                for _ in range(target_pages - 1):
                    next_url = await self._navigate_to_next_page(page, base_url)
                    if not next_url:
                        break

                    try:
                        # Try natural link click first
                        clicked = False
                        if self.config.get("behavior", {}).get("click_links", True):
                            clicked = await self._try_click_link(page, next_url, timeout)

                        if not clicked:
                            await page.goto(
                                next_url, wait_until="domcontentloaded", timeout=timeout
                            )

                        self.stats["pages_visited"] += 1
                        self.stats["pages_list"].append(next_url)

                        # Simulate behavior on subsequent page
                        await self.behavior.simulate_page_visit(page)

                    except Exception as e:
                        logger.debug(
                            f"Session {self.session_id}: Navigation step failed on {next_url}: {e}"
                        )
                        break

                # Completed successfully
                await context.close()
                self.stats["status"] = "completed"
                break

            except Exception as e:
                if context:
                    try:
                        await context.close()
                    except Exception:
                        pass

                if self.proxy_pool and proxy:
                    self.proxy_pool.mark_failed(proxy.get("server", ""))

                err_msg = str(e)
                if any(k in err_msg for k in ["ERR_NETWORK_CHANGED", "ERR_INTERNET_DISCONNECTED", "ERR_NAME_NOT_RESOLVED"]):
                    logger.info(f"Session {self.session_id}: Local network recovery in progress, waiting 3s...")
                    await asyncio.sleep(3.0)

                if attempt < max_attempts - 1:
                    logger.warning(
                        f"Session {self.session_id}: Attempt {attempt + 1} with {self.stats['proxy']} failed ({e}), rotating proxy..."
                    )
                    await asyncio.sleep(1.2)
                    continue
                else:
                    if self.stats["pages_visited"] >= 1:
                        self.stats["status"] = "completed"
                    else:
                        self.stats["status"] = "failed"
                        self.stats["errors"].append(str(e))
                        logger.error(f"Session {self.session_id} failed: {e}")

            finally:
                if owns_browser and browser:
                    await browser.close()
                    browser = None

        self.stats["end_time"] = time.time()
        self.stats["total_time"] = round(
            self.stats["end_time"] - self.stats["start_time"], 2
        )

        logger.info(
            f"Session {self.session_id}: {self.stats['status']} | "
            f"{self.stats['pages_visited']} pages | "
            f"{self.stats['total_time']}s"
        )

        return self.stats

    async def _try_click_link(self, page: Page, next_url: str, timeout: int) -> bool:
        """Attempt to click an internal link element naturally instead of page.goto."""
        try:
            parsed = urlparse(next_url)
            target_path = parsed.path
            query = f"?{parsed.query}" if parsed.query else ""
            full_rel = target_path + query

            # Try selectors matching the target URL
            selectors = [
                f'a[href="{next_url}"]',
                f'a[href="{full_rel}"]',
                f'a[href="{target_path}"]',
                f'a[href="{target_path.rstrip("/")}"]',
            ]

            for sel in selectors:
                loc = page.locator(sel).first
                if await loc.count() > 0 and await loc.is_visible():
                    box = await loc.bounding_box()
                    if box and box["width"] > 0:
                        await loc.scroll_into_view_if_needed(timeout=2000)
                        # Smooth mouse movement
                        target_x = box["x"] + box["width"] / 2
                        target_y = box["y"] + box["height"] / 2
                        await self.behavior.move_mouse_to(page, target_x, target_y)
                        await asyncio.sleep(random.uniform(0.15, 0.4))
                        
                        logger.info(f"Session {self.session_id}: Clicking internal link element -> {full_rel}")
                        try:
                            async with page.expect_navigation(timeout=timeout, wait_until="domcontentloaded"):
                                await loc.click(timeout=3000, delay=random.randint(50, 100))
                            return True
                        except Exception:
                            # Fallback if navigation was client-side or instant
                            return True
        except Exception as e:
            logger.debug(f"Direct link click attempt failed: {e}")

        return False

    async def _navigate_to_next_page(self, page: Page, base_url: str) -> Optional[str]:
        """Determine the next page to visit."""
        configured_pages = self.config.get("target", {}).get("pages", [])

        # Mix between finding internal links and configured pages
        if random.random() < 0.4 and self.config.get("behavior", {}).get("click_links", True):
            internal_link = await self._find_internal_link(page)
            if internal_link and internal_link not in self.stats["pages_list"]:
                return internal_link

        if configured_pages:
            unvisited = [
                p for p in configured_pages
                if p not in self.stats["pages_list"] and
                (base_url + ("" if p.startswith("/") else "/") + p) not in self.stats["pages_list"]
            ]
            path = random.choice(unvisited if unvisited else configured_pages)
            if path.startswith("http://") or path.startswith("https://"):
                return path
            if not path.startswith("/"):
                path = "/" + path
            return base_url.rstrip("/") + path

        return None

    async def _find_internal_link(self, page: Page) -> Optional[str]:
        """Find a clickable internal link on the current page."""
        try:
            links = await page.evaluate("""
                () => {
                    const anchors = document.querySelectorAll('a[href]');
                    const host = window.location.hostname;
                    const results = [];
                    for (const a of anchors) {
                        try {
                            const url = new URL(a.href);
                            if (url.hostname === host &&
                                !a.href.includes('#') &&
                                !a.href.includes('javascript:') &&
                                !a.href.includes('mailto:') &&
                                !a.href.includes('tel:') &&
                                a.offsetParent !== null) {
                                results.push(a.href);
                            }
                        } catch(e) {}
                    }
                    return [...new Set(results)].slice(0, 20);
                }
            """)
            if links:
                return random.choice(links)
        except Exception:
            pass
        return None


class WebsiteTrafficGenerator:
    """
    Main orchestrator for the Website Traffic Generator.
    Manages lightweight shared Chromium instance, concurrent contexts, and proxy pool.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.results: List[Dict] = []
        self.start_time = None
        self.end_time = None

        # Initialize managers
        self.ua_manager = UserAgentManager(config)
        self.ref_manager = ReferrerManager(config)

        # Initialize proxy pool if enabled
        self.proxy_pool = None
        proxy_cfg = config.get("proxy", {})
        if proxy_cfg.get("enabled", False):
            self.proxy_pool = ProxyPool(proxy_cfg)

    async def run(self) -> List[Dict]:
        """Execute all visitor sessions with ultra-lightweight shared browser architecture."""
        session_cfg = self.config.get("sessions", {})
        total = session_cfg.get("total", 30)
        concurrent = session_cfg.get("concurrent", 4)

        logger.info(
            f"Website Traffic Generator: {total} total sessions, "
            f"{concurrent} concurrent contexts"
        )
        self.start_time = time.time()

        # Ultra-lightweight Chromium flags
        launch_args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-accelerated-2d-canvas",
            "--no-first-run",
            "--no-zygote",
            "--disable-gpu",
            "--hide-scrollbars",
            "--mute-audio",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-component-extensions-with-background-pages",
            "--disable-extensions",
            "--disable-renderer-backgrounding",
        ]

        semaphore = asyncio.Semaphore(concurrent)

        async with async_playwright() as p:
            engine = self.config.get("browser", {}).get("engine", "chromium")
            browser_type = getattr(p, engine, p.chromium)
            logger.info("Initializing ultra-lightweight browser instance...")
            browser = await browser_type.launch(
                headless=self.config.get("browser", {}).get("headless", True),
                args=launch_args
            )

            async def run_session(session_id: int):
                async with semaphore:
                    # Random small stagger
                    stagger = random.uniform(0.5, 2.5)
                    await asyncio.sleep(stagger)

                    session = VisitorSession(
                        session_id=session_id,
                        config=self.config,
                        proxy_pool=self.proxy_pool,
                        ua_manager=self.ua_manager,
                        ref_manager=self.ref_manager,
                    )
                    result = await session.execute(shared_browser=browser)
                    self.results.append(result)
                    return result

            # Run all sessions concurrently with semaphore
            tasks = [run_session(i + 1) for i in range(total)]
            await asyncio.gather(*tasks, return_exceptions=True)

            logger.info("Closing browser engine...")
            await browser.close()

        self.end_time = time.time()
        logger.info(
            f"Traffic generation complete: {len(self.results)} sessions "
            f"in {self.end_time - self.start_time:.1f}s"
        )

        return self.results

    def get_summary(self) -> Dict:
        """Aggregate results into a summary report."""
        if not self.results:
            return {"status": "no results"}

        completed = [r for r in self.results if r.get("status") == "completed"]
        failed = [r for r in self.results if r.get("status") == "failed"]
        total_pages = sum(r.get("pages_visited", 0) for r in self.results)
        total_time = sum(r.get("total_time", 0) for r in self.results)

        return {
            "total_sessions": len(self.results),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": round(
                len(completed) / len(self.results) * 100, 1
            ) if self.results else 0,
            "total_pages_visited": total_pages,
            "average_session_duration": round(
                total_time / len(self.results), 2
            ) if self.results else 0,
            "average_pages_per_session": round(
                total_pages / len(self.results), 2
            ) if self.results else 0,
            "total_run_time": round(
                (self.end_time - self.start_time) if self.end_time else 0, 2
            ),
            "device_breakdown": self._device_breakdown(),
            "referrer_breakdown": self._referrer_breakdown(),
        }

    def _device_breakdown(self) -> Dict:
        """Calculate device type distribution."""
        from collections import Counter
        devices = Counter(r.get("device_type", "unknown") for r in self.results)
        total = len(self.results) or 1
        return {
            k: {"count": v, "percent": round(v / total * 100, 1)}
            for k, v in devices.most_common()
        }

    def _referrer_breakdown(self) -> Dict:
        """Calculate referrer type distribution."""
        from collections import Counter
        refs = Counter(
            r.get("referrer_type", "direct") or "direct"
            for r in self.results
        )
        total = len(self.results) or 1
        return {
            k: {"count": v, "percent": round(v / total * 100, 1)}
            for k, v in refs.most_common()
        }
