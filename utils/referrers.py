"""
Referrer Manager
Generates realistic HTTP Referer headers to simulate traffic from
organic search, social media, referral sites, and direct visits.
"""

import random
from typing import Dict, Tuple, Optional

# Organic search engine referrers with keyword templates
SEARCH_ENGINES = {
    "google": {
        "weight": 78,
        "templates": [
            "https://www.google.com/",
            "https://www.google.com/search?q={keyword}",
            "https://www.google.com/search?q={keyword}&sourceid=chrome",
            "https://www.google.co.uk/search?q={keyword}",
            "https://www.google.ca/search?q={keyword}",
            "https://www.google.com.au/search?q={keyword}",
            "https://www.google.de/search?q={keyword}",
            "https://www.google.fr/search?q={keyword}",
        ],
    },
    "bing": {
        "weight": 10,
        "templates": [
            "https://www.bing.com/",
            "https://www.bing.com/search?q={keyword}",
            "https://www.bing.com/search?q={keyword}&form=QBLH",
        ],
    },
    "duckduckgo": {
        "weight": 5,
        "templates": [
            "https://duckduckgo.com/",
            "https://duckduckgo.com/?q={keyword}",
        ],
    },
    "yahoo": {
        "weight": 4,
        "templates": [
            "https://search.yahoo.com/",
            "https://search.yahoo.com/search?p={keyword}",
        ],
    },
    "yandex": {
        "weight": 2,
        "templates": [
            "https://yandex.com/",
            "https://yandex.com/search/?text={keyword}",
        ],
    },
    "ecosia": {
        "weight": 1,
        "templates": [
            "https://www.ecosia.org/",
            "https://www.ecosia.org/search?q={keyword}",
        ],
    },
}

# Social media referrers
SOCIAL_PLATFORMS = {
    "facebook": {
        "weight": 28,
        "urls": [
            "https://www.facebook.com/",
            "https://l.facebook.com/",
            "https://lm.facebook.com/",
            "https://m.facebook.com/",
            "https://www.facebook.com/groups/",
        ],
    },
    "twitter": {
        "weight": 22,
        "urls": [
            "https://t.co/",
            "https://twitter.com/",
            "https://x.com/",
            "https://mobile.twitter.com/",
        ],
    },
    "linkedin": {
        "weight": 18,
        "urls": [
            "https://www.linkedin.com/",
            "https://www.linkedin.com/feed/",
            "https://www.linkedin.com/posts/",
            "https://lnkd.in/",
        ],
    },
    "reddit": {
        "weight": 12,
        "urls": [
            "https://www.reddit.com/",
            "https://old.reddit.com/",
            "https://www.reddit.com/r/",
        ],
    },
    "pinterest": {
        "weight": 7,
        "urls": [
            "https://www.pinterest.com/",
            "https://pin.it/",
        ],
    },
    "youtube": {
        "weight": 6,
        "urls": [
            "https://www.youtube.com/",
            "https://www.youtube.com/redirect",
            "https://youtu.be/",
        ],
    },
    "instagram": {
        "weight": 4,
        "urls": [
            "https://www.instagram.com/",
            "https://l.instagram.com/",
        ],
    },
    "tiktok": {
        "weight": 3,
        "urls": [
            "https://www.tiktok.com/",
        ],
    },
}

# Referral websites (blogs, news, publications)
REFERRAL_SITES = [
    "https://www.medium.com/",
    "https://www.quora.com/",
    "https://news.ycombinator.com/",
    "https://www.producthunt.com/",
    "https://www.techcrunch.com/",
    "https://www.forbes.com/",
    "https://www.entrepreneur.com/",
    "https://www.inc.com/",
    "https://www.wired.com/",
    "https://www.theverge.com/",
    "https://www.businessinsider.com/",
    "https://www.cnet.com/",
    "https://www.zdnet.com/",
    "https://arstechnica.com/",
    "https://www.engadget.com/",
    "https://lifehacker.com/",
    "https://www.makeuseof.com/",
    "https://www.mashable.com/",
    "https://www.huffpost.com/",
    "https://www.buzzfeed.com/",
    "https://dev.to/",
    "https://www.indiehackers.com/",
    "https://hackernoon.com/",
    "https://www.smashingmagazine.com/",
    "https://css-tricks.com/",
]

# Default keywords for search referrers
DEFAULT_KEYWORDS = [
    "website traffic generator",
    "generate website traffic",
    "increase website visitors",
    "web traffic tool",
    "free traffic generator",
    "website visitor generator",
    "automated web traffic",
    "traffic generation software",
    "boost website traffic",
    "organic traffic tool",
    "SEO traffic generator",
    "website traffic bot",
    "get more website visitors",
    "traffic automation",
    "web traffic software",
]


class ReferrerManager:
    """
    Manages referrer generation with configurable source distribution.
    Produces realistic referrer URLs for organic search, social media,
    referral sites, and direct traffic.
    """

    def __init__(self, config: Dict):
        self.config = config
        ref_cfg = config.get("referrers", {})
        self.organic_pct = ref_cfg.get("organic_search_percent", 50)
        self.social_pct = ref_cfg.get("social_percent", 20)
        self.referral_pct = ref_cfg.get("referral_percent", 20)
        # direct_pct is the remainder
        self.keywords = ref_cfg.get("keywords", DEFAULT_KEYWORDS)

    def get_random(self) -> Tuple[Optional[str], str]:
        """
        Generate a random referrer based on configured distribution.
        
        Returns:
            Tuple of (referrer_url_or_None, referrer_type_string)
        """
        roll = random.randint(1, 100)

        if roll <= self.organic_pct:
            return self._organic_referrer(), "organic_search"
        elif roll <= self.organic_pct + self.social_pct:
            return self._social_referrer(), "social"
        elif roll <= self.organic_pct + self.social_pct + self.referral_pct:
            return self._referral_referrer(), "referral"
        else:
            return None, "direct"

    def _organic_referrer(self) -> str:
        """Generate an organic search engine referrer."""
        engines = list(SEARCH_ENGINES.keys())
        weights = [SEARCH_ENGINES[e]["weight"] for e in engines]

        engine = random.choices(engines, weights=weights, k=1)[0]
        template = random.choice(SEARCH_ENGINES[engine]["templates"])

        if "{keyword}" in template:
            keyword = random.choice(self.keywords).replace(" ", "+")
            return template.format(keyword=keyword)
        return template

    def _social_referrer(self) -> str:
        """Generate a social media referrer."""
        platforms = list(SOCIAL_PLATFORMS.keys())
        weights = [SOCIAL_PLATFORMS[p]["weight"] for p in platforms]

        platform = random.choices(platforms, weights=weights, k=1)[0]
        return random.choice(SOCIAL_PLATFORMS[platform]["urls"])

    def _referral_referrer(self) -> str:
        """Generate a referral site URL."""
        return random.choice(REFERRAL_SITES)
