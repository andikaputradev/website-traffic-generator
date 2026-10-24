Website Traffic Generator

Automated Website Traffic Processing and Browser Automation Engine

Developed and maintained by "Wahyu Andika Putra" (https://andikadev.com)
Founder and Full-Stack Software Engineer at "AndikaDev" (https://andikadev.com)

""Python" (https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)" (https://python.org)
""Playwright" (https://img.shields.io/badge/Playwright-Chromium%20%7C%20Firefox-2EAD33?style=flat-square&logo=playwright)" (https://playwright.dev/)
""License: MIT" (https://img.shields.io/badge/License-MIT-yellow?style=flat-square)" (https://opensource.org/licenses/MIT)
""Website" (https://img.shields.io/badge/Website-andikadev.com-0F766E?style=flat-square)" (https://andikadev.com)

---

Overview

Website Traffic Generator is a Python-based browser automation engine built with Playwright. It automates website navigation, page rendering, interaction workflows, and session management through real browser engines.

The project is designed for developers, QA engineers, and system administrators who need to evaluate website behavior, validate analytics implementations, and test browser-based workflows in controlled environments.

Key Use Cases

- Website functionality and browser compatibility testing.
- Analytics event and UTM parameter validation.
- Multi-page navigation and interaction testing.
- Responsive layout and viewport verification.
- CDN, caching, and infrastructure performance testing.
- Automated browser workflows for authorized environments.

Key Features

Browser Automation

- Chromium and Firefox browser support through Playwright.
- Automated page navigation and internal link traversal.
- Configurable page interaction and scrolling.
- Adjustable session duration and navigation depth.
- Headless and headed execution modes.

Traffic Source Configuration

- Configurable referrer information.
- Support for direct, search, social, and referral source classifications.
- Customizable URL parameters and search-related test scenarios.
- Configurable traffic distribution for controlled testing.

Referrer information does not independently establish genuine organic or social traffic.

Proxy Management

- HTTP, HTTPS, and SOCKS5 proxy configuration.
- Random and round-robin proxy selection.
- Proxy connectivity validation.
- Configurable proxy lists for authorized testing environments.

Device and Viewport Configuration

- Desktop, mobile, and tablet viewport profiles.
- Configurable browser user-agent strings.
- Responsive layout verification.
- Browser locale and timezone configuration.

Asynchronous Execution

- Python "asyncio" integration.
- Concurrent browser context management.
- Configurable concurrency and execution intervals.
- Logging and JSON report generation.

Architecture

Configuration
     |
     v
Traffic Execution Engine
     |
     +-- Browser Automation
     |      +-- Page Navigation
     |      +-- Element Interaction
     |      +-- Scroll and Viewport Testing
     |
     +-- Session Management
     |      +-- Duration and Page Limits
     |      +-- Concurrency Control
     |
     +-- Proxy Management
     |      +-- Proxy Configuration
     |      +-- Connectivity Validation
     |
     +-- Logging and Reporting
            +-- Execution Logs
            +-- JSON Reports

Requirements

- Python 3.8 or newer.
- Git.
- Playwright and its supported browser dependencies.
- Linux, macOS, or Windows.

For production environments, use a supported Python version and keep project dependencies updated.

Installation

1. Clone the Repository

git clone https://github.com/andikaputradev/website-traffic-generator.git
cd website-traffic-generator

2. Create a Virtual Environment

Windows PowerShell

python -m venv venv
.\venv\Scripts\Activate.ps1

Linux and macOS

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt
python -m playwright install chromium

On supported Linux systems, install additional browser dependencies if required:

python -m playwright install-deps chromium

Usage

Run a Browser Automation Session

python run_traffic.py --url "https://example.com" --sessions 30 --concurrent 5

Configure a Proxy List

python run_traffic.py --url "https://example.com" --sessions 30 --concurrent 4 --proxy-file proxies.txt

Run with a Configuration File

python run_traffic.py --config config.yaml

Replace "example.com" with a website you own or are authorized to test.

Configuration

The "config.yaml" file provides centralized configuration for target URLs, session limits, browser settings, and execution behavior.

target:
  url: "https://example.com"
  pages:
    - "/"
    - "/about"
    - "/contact"

sessions:
  total: 30
  concurrent: 5
  delay_min: 5
  delay_max: 15
  pages_per_session_min: 1
  pages_per_session_max: 3

browser:
  headless: true
  engine: "chromium"
  timeout: 30000

behavior:
  scroll: true
  scroll_speed: "random"
  click_links: true
  click_content: true
  mouse_movement: true
  random_pauses: true

referrers:
  organic_search_percent: 50
  social_percent: 25
  referral_percent: 15
  direct_percent: 10

devices:
  desktop_percent: 55
  mobile_percent: 40
  tablet_percent: 5

proxy:
  enabled: false
  file: "proxies.txt"
  rotation: "random"

output:
  logging: true
  log_file: "traffic_generator.log"
  log_level: "INFO"
  report_file: "report.json"

Note: Configuration options must match the parameters implemented in the current source code. The values above are an example configuration, not a guarantee that every option is supported by every version.

Proxy Generation and Validation

The project may include a "generate_proxies.py" utility for collecting and checking proxy endpoints.

python generate_proxies.py

Use trusted proxy providers or endpoints you are authorized to access. Public proxies can be unreliable and may expose traffic or credentials to third parties.

Scheduling and Automation

If the repository includes "run_scheduler.py", scheduled execution can be started with:

python run_scheduler.py

Scheduling behavior, execution intervals, recovery mechanisms, and supported options depend on the implementation in the repository.

Deployment

The application can run on a Linux VPS or another compatible environment.

For long-running workloads, configure a dedicated, unprivileged service account, an isolated Python environment, appropriate resource limits, and persistent application logs.

Example systemd service:

[Unit]
Description=Website Traffic Generator
After=network.target

[Service]
Type=simple
User=trafficbot
WorkingDirectory=/opt/website-traffic-generator
ExecStart=/opt/website-traffic-generator/venv/bin/python run_scheduler.py
Restart=on-failure
RestartSec=15

[Install]
WantedBy=multi-user.target

Save the configuration as "/etc/systemd/system/traffic-generator.service", then run:

sudo systemctl daemon-reload
sudo systemctl enable --now traffic-generator
sudo systemctl status traffic-generator

Adjust the service account, working directory, and entry point to match your deployment.

Testing and Analytics Validation

The browser automation engine can be used to verify website functionality and inspect analytics implementations in controlled test environments.

Recommended validation scenarios include:

- Confirming that analytics tags load correctly.
- Verifying event names and parameters.
- Testing navigation and conversion workflows.
- Checking responsive layouts across viewport profiles.
- Reviewing execution logs and generated reports.

Automated browser sessions should not be treated as evidence of genuine human visitors, genuine search rankings, or authentic advertising engagement. Analytics platforms may classify or filter automated activity.

Responsible Use

Use this software only on websites and infrastructure you own or have explicit authorization to test.

- Do not generate fraudulent advertising impressions or clicks.
- Do not manipulate analytics or business metrics deceptively.
- Do not overload websites or third-party infrastructure.
- Respect applicable terms of service, access controls, and rate limits.
- Protect credentials, proxy information, and sensitive execution logs.

Author

Wahyu Andika Putra
Full-Stack Software Engineer and Cybersecurity Researcher
Founder of "AndikaDev" (https://andikadev.com)

Channel| Contact
Website| "andikadev.com" (https://andikadev.com)
LinkedIn| "Wahyu Andika Putra" (https://linkedin.com/in/wahyu-andika-putra)
GitHub| "@andikaputradev" (https://github.com/andikaputradev)
Email| "wahyuandikaputra.co.id@gmail.com" (mailto:wahyuandikaputra.co.id@gmail.com)
WhatsApp| "+62 877-3013-9582" (https://wa.me/6287730139582)
Telegram| "@andikaputradev" (https://t.me/andikaputradev)
Instagram| "@andikaputradev" (https://instagram.com/andikaputradev)
TikTok| "@andikaputradev" (https://tiktok.com/@andikaputradev)

Professional Services

Explore software development and engineering services at "AndikaDev.com" (https://andikadev.com).

- "Website Development" (https://andikadev.com/layanan/pembuatan-website)
- "Mobile Application Development" (https://andikadev.com/layanan/pembuatan-aplikasi)
- "Google Play Store Publishing" (https://andikadev.com/layanan/upload-play-store)
- "Cybersecurity and Defensive Security" (https://andikadev.com/layanan/keamanan-siber)
- "Web3 and Blockchain Development" (https://andikadev.com/layanan/web3-blockchain)

License

This project is distributed under the MIT License. See ""LICENSE"" (LICENSE) for the complete license terms.

Copyright (c) 2026 Wahyu Andika Putra
"https://andikadev.com" (https://andikadev.com)
