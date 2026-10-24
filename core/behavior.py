"""
Human Behavior Simulation Engine
Provides realistic browsing behavior patterns including scrolling,
mouse movements, reading pauses, and interactive content clicking.
"""

import asyncio
import random
import math
import logging
from typing import Dict, Optional
from playwright.async_api import Page

logger = logging.getLogger("traffic_generator.behavior")


class HumanBehaviorEngine:
    """
    Simulates realistic human browsing behavior on web pages.
    Includes natural scrolling, mouse movements, reading pauses,
    and interactive content clicking that mimic real users.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.behavior_cfg = config.get("behavior", {})
        self.session_cfg = config.get("sessions", {})

    async def simulate_landing_page(self, page: Page):
        """
        Simulate behavior on a landing page (first page of session).
        Landing pages typically have longer dwell times and interactive clicks.
        """
        # Initial pause (user reading the hero section)
        await self._reading_pause(min_sec=1.5, max_sec=3.5)

        # Mouse movement (user moving cursor while orienting)
        if self.behavior_cfg.get("mouse_movement", True):
            await self._natural_mouse_movement(page, movements=random.randint(2, 4))

        # Scroll through the top content
        if self.behavior_cfg.get("scroll", True):
            await self._natural_scroll(page, depth_factor=random.uniform(0.4, 0.7))

        # Interactive content clicking (tabs, categories, tags, buttons)
        if self.behavior_cfg.get("click_content", True):
            await self.simulate_content_interaction(page)

        # Dwell time (reading/absorbing content to secure GA4 engaged session)
        delay_min = self.session_cfg.get("delay_min", 10)
        delay_max = self.session_cfg.get("delay_max", 25)
        await self._reading_pause(min_sec=delay_min * 0.4, max_sec=delay_max * 0.5)

        # Further scroll down
        if self.behavior_cfg.get("scroll", True) and random.random() < 0.6:
            await self._natural_scroll(page, depth_factor=random.uniform(0.6, 0.9))

    async def simulate_page_visit(self, page: Page):
        """
        Simulate behavior on subsequent pages (not the landing page).
        """
        # Brief pause on page load
        await self._reading_pause(min_sec=1.0, max_sec=2.5)

        # Mouse movement
        if self.behavior_cfg.get("mouse_movement", True):
            await self._natural_mouse_movement(page, movements=random.randint(2, 4))

        # Scroll
        if self.behavior_cfg.get("scroll", True):
            await self._natural_scroll(page, depth_factor=random.uniform(0.3, 0.7))

        # Interactive content interaction
        if self.behavior_cfg.get("click_content", True) and random.random() < 0.7:
            await self.simulate_content_interaction(page)

        # Dwell time
        delay_min = self.session_cfg.get("delay_min", 10)
        delay_max = self.session_cfg.get("delay_max", 25)
        await self._reading_pause(
            min_sec=max(4.0, delay_min * 0.4),
            max_sec=max(10.0, delay_max * 0.5),
        )

    async def simulate_content_interaction(self, page: Page):
        """
        Simulate authentic human clicks on interactive page elements
        such as category filters, article preview cards, tags, and buttons.
        """
        try:
            interactive_selectors = [
                'a[href*="category="]',
                'button:not([disabled])',
                'a[href*="/artikel"]',
                'a[href*="/work"]',
                'article a',
                '.tag',
                '[role="button"]',
                '[role="tab"]'
            ]
            
            for selector in interactive_selectors:
                elements = page.locator(selector)
                count = await elements.count()
                if count > 0:
                    candidates = list(range(min(count, 6)))
                    random.shuffle(candidates)
                    
                    for idx in candidates:
                        elem = elements.nth(idx)
                        if await elem.is_visible():
                            box = await elem.bounding_box()
                            if box and box["width"] > 0 and box["height"] > 0:
                                await elem.scroll_into_view_if_needed(timeout=1500)
                                target_x = box["x"] + random.uniform(box["width"] * 0.3, box["width"] * 0.7)
                                target_y = box["y"] + random.uniform(box["height"] * 0.3, box["height"] * 0.7)
                                
                                await self.move_mouse_to(page, target_x, target_y)
                                await asyncio.sleep(random.uniform(0.2, 0.5))
                                
                                # Click the element
                                await elem.click(timeout=2000, delay=random.randint(40, 100))
                                
                                # Natural pause to view the clicked result
                                await asyncio.sleep(random.uniform(1.2, 2.8))
                                return
        except Exception as e:
            logger.debug(f"Content interaction skipped or handled: {e}")

    async def move_mouse_to(self, page: Page, target_x: float, target_y: float):
        """Move mouse smoothly from current position to target coordinates."""
        try:
            viewport = page.viewport_size or {"width": 1280, "height": 800}
            target_x = max(10, min(target_x, viewport["width"] - 10))
            target_y = max(10, min(target_y, viewport["height"] - 10))

            steps = random.randint(6, 14)
            # Simple smooth trajectory
            for i in range(1, steps + 1):
                t = i / steps
                # Slight curve offset
                curve = math.sin(t * math.pi) * random.uniform(-15, 15)
                # Assuming starting from an approximate point if not set
                await page.mouse.move(target_x + curve * (1 - t), target_y)
                await asyncio.sleep(random.uniform(0.01, 0.03))
                
            await page.mouse.move(target_x, target_y)
        except Exception:
            pass

    async def _natural_scroll(self, page: Page, depth_factor: float = 0.6):
        """
        Simulate natural scrolling behavior.
        Humans scroll in bursts, pause to read, and occasionally scroll back up.
        """
        scroll_speed = self.behavior_cfg.get("scroll_speed", "random")

        profiles = {
            "slow": (80, 200, 0.5, 1.2),
            "medium": (150, 400, 0.3, 0.8),
            "fast": (250, 600, 0.15, 0.4),
            "random": (100, 500, 0.2, 0.8),
        }
        min_px, max_px, min_pause, max_pause = profiles.get(
            scroll_speed, profiles["random"]
        )

        try:
            page_height = await page.evaluate("document.body.scrollHeight")
            viewport_height = (
                page.viewport_size["height"] if page.viewport_size else 800
            )
            max_scroll = page_height - viewport_height

            if max_scroll <= 0:
                return

            scroll_target = max_scroll * depth_factor
            current_pos = 0

            while current_pos < scroll_target:
                scroll_amount = random.randint(min_px, max_px)

                # Micro-scroll
                if random.random() < 0.2:
                    scroll_amount = random.randint(30, 80)

                current_pos += scroll_amount
                await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
                await asyncio.sleep(random.uniform(min_pause, max_pause))

                # Reading pause
                if random.random() < 0.15:
                    await asyncio.sleep(random.uniform(1.0, 2.5))

                # Scroll back up slightly (re-reading)
                if random.random() < 0.08:
                    back_amount = random.randint(40, 120)
                    await page.evaluate(f"window.scrollBy(0, -{back_amount})")
                    current_pos -= back_amount
                    await asyncio.sleep(random.uniform(0.3, 0.8))

        except Exception as e:
            logger.debug(f"Scroll simulation error: {e}")

    async def _natural_mouse_movement(self, page: Page, movements: int = None):
        """Simulate natural mouse cursor movements."""
        if movements is None:
            movements = random.randint(2, 5)

        viewport = page.viewport_size
        if not viewport:
            return

        width = viewport["width"]
        height = viewport["height"]

        try:
            current_x = random.randint(100, max(150, width - 100))
            current_y = random.randint(100, max(150, height - 100))

            for _ in range(movements):
                target_x = random.randint(50, max(100, width - 50))
                target_y = random.randint(50, max(100, height - 50))

                steps = random.randint(6, 14)
                for step in range(steps):
                    t = step / steps
                    curve_offset = math.sin(t * math.pi) * random.uniform(-20, 20)

                    x = int(current_x + (target_x - current_x) * t + curve_offset)
                    y = int(current_y + (target_y - current_y) * t)

                    x = max(0, min(x, width))
                    y = max(0, min(y, height))

                    await page.mouse.move(x, y)
                    await asyncio.sleep(random.uniform(0.01, 0.03))

                current_x, current_y = target_x, target_y
                await asyncio.sleep(random.uniform(0.15, 0.5))

        except Exception as e:
            logger.debug(f"Mouse movement error: {e}")

    async def _reading_pause(self, min_sec: float = 2.0, max_sec: float = 6.0):
        """Simulate a reading pause with natural variation."""
        if not self.behavior_cfg.get("random_pauses", True):
            await asyncio.sleep(min_sec)
            return

        mean = (min_sec + max_sec) / 2
        std = (max_sec - min_sec) / 4
        pause = max(min_sec, min(max_sec, random.gauss(mean, std)))
        await asyncio.sleep(pause)
