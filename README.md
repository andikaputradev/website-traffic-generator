<div align="center">

# 🚀 Website Traffic Generator & Human Session Simulator

**Advanced Open-Source Traffic Simulation, Human Behavior Emulation, and Headless Browser Automation Engine**

Developed & Maintained with ❤️ by **[Wahyu Andika Putra](https://andikadev.com)**  
*(Founder & Fullstack / Security Engineer at **[AndikaDev](https://andikadev.com)**)*

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Chromium%20%7C%20Firefox-2EAD33.svg?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Author: Wahyu Andika Putra](https://img.shields.io/badge/Author-Wahyu%20Andika%20Putra-blueviolet.svg?style=for-the-badge&logo=github)](https://github.com/andikaputradev)
[![Official Website](https://img.shields.io/badge/Website-andikadev.com-00C7B7.svg?style=for-the-badge&logo=googlechrome&logoColor=white)](https://andikadev.com)

<br/>

[🌟 Overview](#-overview) • [✨ Key Features](#-key-features) • [🏗️ Architecture](#️-architecture) • [🚀 Quick Start](#-quick-start) • [⚙️ Configuration](#️-configuration-guide) • [🔄 Proxy Generation](#-proxy-generation--validation) • [⏱️ Scheduler & Automation](#️-scheduler--automation) • [🌐 VPS Deployment](#-vps-deployment) • [👨‍💻 Author & Contact](#-author--contact)

---

</div>

## 🌟 Overview

**Website Traffic Generator** is a production-grade, asynchronous website traffic generator and user-behavior simulator built in Python using **Playwright**. Unlike elementary curl/ping tools or simple HTTP request spammers that are immediately dropped by modern Web Application Firewalls (WAF) and ignored by analytics platforms, this engine drives **real, headless Chromium/Firefox browsers** to render complete DOM trees, load CSS/web fonts, execute JavaScript bundles, and trigger analytics SDKs such as **Google Analytics 4 (GA4)**, Meta Pixel, Adobe Analytics, and Plausible.

The project is designed, engineered, and maintained by **[Wahyu Andika Putra](https://andikadev.com)** from **[AndikaDev](https://andikadev.com)** to serve developers, SEO specialists, QA engineers, and system administrators for:
- Testing and verifying analytics events, UTM tracking, and conversion funnels.
- Realistic web application load and infrastructure stress testing under real browser conditions.
- Simulating organic search, social media, and multi-channel referral traffic flows.
- Validating CDN caching, edge routing, and Web Application Firewall responsiveness.

> 💡 **Looking for custom software development, mobile apps, or security audits?**  
> Explore official services by Wahyu Andika Putra at **[AndikaDev.com](https://andikadev.com)**:  
> • [Jasa Pembuatan Website Profesional](https://andikadev.com/layanan/pembuatan-website)  
> • [Jasa Pembuatan Aplikasi Mobile (Android & iOS)](https://andikadev.com/layanan/pembuatan-aplikasi)  
> • [Jasa Upload Aplikasi ke Google Play Store](https://andikadev.com/layanan/upload-play-store)  
> • [Audit Keamanan Siber & Defensive Security](https://andikadev.com/layanan/keamanan-siber)  
> • [Web3 & Blockchain Development](https://andikadev.com/layanan/web3-blockchain)

---

## ✨ Key Features

### 1. 🧠 Realistic Human Behavior Emulation
- **Bézier Curve Mouse Movements:** Generates mathematical cubic Bézier curve cursor paths with acceleration and deceleration curves that evade bot detection heuristics.
- **Natural Dynamic Scrolling:** Smooth, non-linear scrolling with randomized dwell depths, pauses, reading intervals, and occasional upward scrolls.
- **Interactive Element Clicking:** Identifies and interacts with internal page links, tabs, categories, accordion filters, and preview cards to simulate authentic user exploration.
- **GA4 Engaged Sessions:** Guarantees sessions satisfy Google Analytics 4 thresholds for *Engaged Sessions* (customizable dwell time $\ge 10$ seconds, multi-page paths, and active DOM engagement).

### 2. 🔀 Multi-Source Traffic Spoofing & Referrer Injection
- **Organic Search Engines:** Emulates organic visitors arriving from Google, Bing, Yahoo, DuckDuckGo, and Yandex, complete with customized search keywords and search engine query params.
- **Social Media Networks:** Spoofs referrers from Twitter/X, LinkedIn, Reddit, Facebook, Instagram, and Pinterest.
- **Direct & Referral Influx:** Configurable ratios for direct URL entries, web publications, Medium, Dev.to, and industry partner backlinks.

### 3. 🛡️ Rotating Proxy Pool & Geo-Targeting
- Full support for **HTTP**, **HTTPS**, and **SOCKS5** rotating proxies.
- Flexible rotation strategies: `random`, `round-robin`, and `per-session`.
- Built-in multi-threaded proxy generator & real-time validator (`generate_proxies.py`) that harvests and verifies live proxies against your target domain.

### 4. 📱 Dynamic Device Fingerprinting & Viewports
- Balanced device split: **Desktop** (55%), **Mobile** (40%), and **Tablet** (5%).
- Curated, up-to-date User-Agent database encompassing Chrome, Safari, Edge, Firefox, iOS Mobile Safari, and Android Chrome.
- Responsive viewports, screen pixel ratios, touch event support, and automated header locale / timezone synchronization.

### 5. ⚡ Asynchronous Concurrency & Resource Efficiency
- Powered by `asyncio` and Playwright browser contexts for ultra-low memory overhead.
- Supports concurrent browser contexts running in parallel without launching multiple heavy browser instances.

---

## 🏗️ Architecture

```
                                  ┌────────────────────────────────┐
                                  │   Target Website (e.g. GA4)    │
                                  └────────────────────────────────┘
                                                  ▲
                                                  │ (Realistic Sessions)
┌──────────────────────┐         ┌────────────────┴────────────────┐
│  config.yaml / CLI   │ ──────► │       run_traffic.py            │
└──────────────────────┘         │   Async Session Coordinator     │
                                 └────────────────┬────────────────┘
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 ▼                                ▼                                ▼
  ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐
  │   Human Behavior Engine     │  │     Proxy Pool Manager      │  │   User-Agent & Referrers    │
  │ • Cubic Bézier Mouse Moves  │  │ • HTTP / HTTPS / SOCKS5     │  │ • Organic Search Keywords   │
  │ • Dynamic Dwell & Scroll    │  │ • Health checks & rotation  │  │ • Social / Referral / Direct│
  │ • Internal Link Traversal   │  │ • proxies.txt validator     │  │ • Device & Viewport Emulation│
  └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or newer** installed.
- **Git** installed on your system.
- Recommended: Operating on Linux VPS (Ubuntu/Debian) or Windows 10/11.

### Step 1: Clone the Repository

```bash
git clone https://github.com/andikaputradev/website-traffic-generator.git
cd website-traffic-generator
```

### Step 2: Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies & Playwright Browsers

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

> *Tip: If installing on a headless Ubuntu/Debian VPS, also install the necessary system libraries:*  
> `python -m playwright install-deps chromium`

---

## 💻 Usage Guide

### 1. Simple Single Command

Launch 30 simulated visitor sessions to your website with 5 concurrent workers:

```bash
python run_traffic.py --url "https://andikadev.com" --sessions 30 --concurrent 5
```

### 2. Using Custom Proxy File

Run traffic routed through your verified proxy list:

```bash
python run_traffic.py --url "https://andikadev.com" --sessions 50 --concurrent 4 --proxy-file proxies.txt
```

### 3. Production Mode (YAML Configuration)

For fine-grained control over dwell time, internal link exploration, device distribution, and keyword spoofing, use `config.yaml`:

```bash
python run_traffic.py --config config.yaml
```

---

## ⚙️ Configuration Guide

The `config.yaml` file gives you full mastery over your traffic campaigns:

```yaml
# ============================================================
# Website Traffic Generator - Configuration
# ============================================================
# Target: https://andikadev.com
# Author: Wahyu Andika Putra (https://andikadev.com)
# ============================================================

# --- Target Website ---
target:
  url: "https://andikadev.com"          # Primary domain / URL
  pages:                                # Specific pages to visit
    - "/"
    - "/tentang"
    - "/layanan"
    - "/layanan/pembuatan-website"
    - "/layanan/pembuatan-aplikasi"
    - "/layanan/upload-play-store"
    - "/layanan/keamanan-siber"
    - "/layanan/web3-blockchain"
    - "/blog"
    - "/blog/core-web-vitals-inp-nextjs-optimasi-performa-seo"
    - "/blog/cara-membuat-website-pendaftaran-online"
    - "/blog/kepatuhan-uu-pdp-bagi-pengembang-kontrol-teknis"
    - "/kontak"

# --- Session & Duration Settings ---
sessions:
  total: 50                           # Total visitors to generate
  concurrent: 4                       # Simultaneous browser contexts
  delay_min: 10                       # Minimum dwell time per page in seconds (ensures GA4 engagement)
  delay_max: 22                       # Maximum dwell time per page in seconds
  pages_per_session_min: 2            # Minimum pageviews per visitor
  pages_per_session_max: 4            # Maximum pageviews per visitor

# --- Browser Engine ---
browser:
  headless: true                      # Run invisibly (true) or open window (false)
  engine: "chromium"                  # Options: chromium, firefox, webkit
  timeout: 30000                      # 30-second timeout per page load

# --- Realistic Human Behavior Simulation ---
behavior:
  scroll: true                        # Natural human scrolling
  scroll_speed: "random"              # Options: slow, medium, fast, random
  click_links: true                   # Autonomously click internal links
  click_content: true                 # Click interactive content (tabs, categories, buttons)
  mouse_movement: true                # Mathematical Bezier curve mouse movements
  random_pauses: true                 # Natural reading pauses

# --- Traffic Referrer Distribution ---
referrers:
  organic_search_percent: 50          # 50% from Search Engines
  social_percent: 25                  # 25% from Social Media
  referral_percent: 15                # 15% from External Websites
  direct_percent: 10                  # 10% Direct Navigation
  keywords:                           # Realistic SEO search queries
    - "wahyu andika putra"
    - "andikadev"
    - "jasa pembuatan website"
    - "jasa pembuatan website profesional"
    - "jasa bikin web semarang wonosobo"
    - "jasa pembuatan aplikasi mobile"
    - "jasa upload aplikasi ke play store"
    - "jasa audit keamanan siber"
    - "penetration testing indonesia"
    - "web3 blockchain developer indonesia"

# --- Device Distribution ---
devices:
  desktop_percent: 55                 # 55% Desktop (Chrome, Firefox, Safari)
  mobile_percent: 40                  # 40% Mobile (Android Chrome, iOS Safari)
  tablet_percent: 5                   # 5% Tablet (iPad, Galaxy Tab)

# --- Proxy Rotation ---
proxy:
  enabled: true                       # Set to true to route via proxies
  file: "proxies.txt"                 # File containing proxy list (protocol://ip:port)
  rotation: "random"                  # Strategy: random, round-robin

# --- Output & Logging ---
output:
  logging: true                       # Write detailed logs
  log_file: "traffic_generator.log"   # Log filepath
  log_level: "INFO"                   # Log level (DEBUG, INFO, WARNING, ERROR)
  report_file: "report.json"          # JSON summary report
```

---

## 🔄 Proxy Generation & Validation

Need fresh proxies? The included `generate_proxies.py` script automatically scrapes public repositories, tests connectivity against the target website via asynchronous HTTPS requests, and writes working proxies directly to `proxies.txt`:

```bash
python generate_proxies.py
```

Features:
- Scrapes across verified HTTP, HTTPS, and SOCKS5 proxy pools.
- Concurrent validation with semaphore throttling (tests hundreds of proxies per minute).
- Only saves proxies that return an authentic `HTTP 200 OK` status from the target domain.

---

## ⏱️ Scheduler & Automation

To simulate natural human traffic distribution throughout the day rather than sending spikes that trigger anomaly detectors, use `run_scheduler.py`:

```bash
python run_scheduler.py
```

- **Peak Hour Detection:** Schedules batches during high-traffic hours (08:00 - 23:00 local time).
- **Batch Processing:** Runs controlled batches (e.g., 20 sessions per run) to maintain steady, natural traffic pacing.
- **Crash Recovery:** Safely recovers and logs errors without interrupting the scheduling cycle.

---

## 🌐 VPS Deployment

Deploying the generator to run 24/7 on a Linux VPS (Ubuntu/Debian):

### Method 1: Using `nohup` (Simplest)
```bash
nohup python3 run_scheduler.py > scheduler.log 2>&1 &
echo "Scheduler running in background with PID $!"
```

To stop:
```bash
pkill -f run_scheduler.py
```

### Method 2: Systemd Service (Recommended for Production)

Create a systemd service file `/etc/systemd/system/traffic-generator.service`:

```ini
[Unit]
Description=Website Traffic Generator Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/website-traffic-generator
ExecStart=/var/www/website-traffic-generator/venv/bin/python run_scheduler.py
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable traffic-generator
sudo systemctl start traffic-generator
sudo systemctl status traffic-generator
```

---

## ⚖️ Website Traffic Generator vs. Traditional Bot Scripts

| Capability | This Project (Playwright Browser) | Traditional cURL / Python `requests` |
| :--- | :--- | :--- |
| **Full DOM & JS Execution** | ✅ Complete (Renders React, Next.js, Vue, etc.) | ❌ No (Raw HTML only) |
| **GA4 & Analytics Tracking** | ✅ Triggers real events & engaged sessions | ❌ Ignored or blocked by analytics |
| **Mouse Movements & Scroll** | ✅ Mathematical Bézier curves & dynamic scroll | ❌ None |
| **Internal Link Traversal** | ✅ Clicks real DOM elements naturally | ❌ Only follows HTTP redirects |
| **Fingerprint Integrity** | ✅ Real Chromium viewports, WebGL, canvas | ❌ Easily fingerprinted as synthetic bot |
| **WAF Evasion** | ✅ High (simulates real browser environment) | ❌ Readily blocked by Cloudflare/AWS WAF |

---

## 🛡️ Fair Use & Ethical Disclaimer

This software is developed strictly for **educational, testing, QA benchmarking, and authorized infrastructure evaluation purposes**:
- **Authorization Required:** Only test websites, servers, and applications that you own or have explicit written authorization to test.
- **No Ad Fraud:** Never use this software to generate fraudulent clicks or impressions on Google AdSense, display ads, or affiliate networks.
- **Server Courtesy:** Calibrate your concurrency and session intervals to prevent unintended load spikes or Denial of Service (DoS) conditions on web servers.

---

## 👨‍💻 Author & Contact

This project is created and maintained by **Wahyu Andika Putra**.

<div align="center">

### **Wahyu Andika Putra**
*Fullstack Software Engineer • Cybersecurity Researcher • Web3 Specialist*  
Founder of **[AndikaDev](https://andikadev.com)**

</div>

| Channel | Link / Information |
| :--- | :--- |
| 🌐 **Official Website** | [https://andikadev.com](https://andikadev.com) |
| 💼 **LinkedIn** | [Wahyu Andika Putra](https://linkedin.com/in/wahyu-andika-putra) |
| 🐙 **GitHub** | [@andikaputradev](https://github.com/andikaputradev) |
| 📧 **Email** | [wahyuandikaputra.co.id@gmail.com](mailto:wahyuandikaputra.co.id@gmail.com) |
| 💬 **WhatsApp / Call** | [+62 877-3013-9582](https://wa.me/6287730139582) |
| ✈️ **Telegram** | [@andikaputradev](https://t.me/andikaputradev) |
| 📸 **Instagram** | [@andikaputradev](https://instagram.com/andikaputradev) & [@w.andikaputraa](https://instagram.com/w.andikaputraa) |
| 🎵 **TikTok** | [@andikaputradev](https://tiktok.com/@andikaputradev) |
| 📘 **Facebook** | [andikaputradev](https://facebook.com/andikaputradev) |

---

### 💼 Professional Services by AndikaDev
Need end-to-end digital engineering or custom software solutions? Visit **[andikadev.com](https://andikadev.com)** to consult directly with Wahyu Andika Putra:
- 💻 **[Jasa Pembuatan Website](https://andikadev.com/layanan/pembuatan-website)** – Modern, blazing-fast Next.js, React, and WordPress sites with high SEO performance.
- 📱 **[Jasa Pembuatan Aplikasi Mobile](https://andikadev.com/layanan/pembuatan-aplikasi)** – Cross-platform mobile applications for iOS & Android built with React Native / Flutter.
- 🚀 **[Jasa Upload Google Play Store](https://andikadev.com/layanan/upload-play-store)** – End-to-end publishing, target API compliance, privacy policy, and Google Play Console approval.
- 🛡️ **[Keamanan Siber & Defensive Security](https://andikadev.com/layanan/keamanan-siber)** – Web penetration testing, vulnerability assessment, and hardening.
- ⛓️ **[Web3 & Blockchain Development](https://andikadev.com/layanan/web3-blockchain)** – Smart contract development, security audits, and decentralized applications (dApps).

---

## 📝 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for complete details.

Copyright (c) 2026 **Wahyu Andika Putra** ([https://andikadev.com](https://andikadev.com)). All rights reserved.
