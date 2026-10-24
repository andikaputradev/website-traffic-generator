<div align="center">

# Website Traffic Generator

**Python-Based Browser Automation and Website Testing**

Developed and maintained by **[Wahyu Andika Putra](https://andikadev.com)**  
Founder of **[AndikaDev](https://andikadev.com)**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Chromium%20%7C%20Firefox-2EAD33?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![Website](https://img.shields.io/badge/Website-andikadev.com-0F766E?style=flat-square)](https://andikadev.com)

[Overview](#overview) · [Features](#features) · [Architecture](#architecture) · [Installation](#installation) · [Usage](#usage) · [Configuration](#configuration) · [Deployment](#deployment) · [Author](#author)

</div>

---

## Overview

**Website Traffic Generator** is a Python-based browser automation project built with Playwright. It automates browser sessions, page navigation, website interactions, and configurable execution workflows using Chromium.

The project is intended for authorized website testing, analytics implementation checks, browser workflow validation, and controlled infrastructure testing.

### Use Cases

- Validate analytics tags, events, and UTM parameters.
- Test page navigation and interactive elements.
- Verify responsive layouts across device viewports.
- Exercise multi-page browser workflows.
- Review website behavior under controlled concurrent sessions.
- Validate caching and infrastructure behavior on systems you own or are authorized to test.

> **Important:** Automated browser sessions are not equivalent to genuine human visitors. Referrer settings do not guarantee real organic or social traffic, and analytics platforms may identify or filter automated activity.

## Features

### Browser Automation

- Playwright-powered Chromium browser sessions.
- Headless and visible browser execution.
- Automated navigation and internal-link interaction.
- Configurable session duration and page limits.
- Scrolling, pauses, and interactive element testing.

### Traffic Source Configuration

- Configurable referrer values.
- Direct, search, social, and referral source test scenarios.
- Custom URL parameters for campaign and UTM validation.
- Adjustable source distribution for controlled tests.

### Proxy Management

- HTTP, HTTPS, and SOCKS5 proxy configuration, where supported by the installed dependencies.
- Random and round-robin proxy selection.
- Proxy connectivity checks.
- Configurable proxy lists for authorized testing environments.

### Device and Viewport Profiles

- Desktop, mobile, and tablet viewport settings.
- Configurable user-agent strings.
- Responsive layout verification.
- Browser locale and timezone configuration, where implemented.

### Asynchronous Execution

- Python `asyncio` integration.
- Concurrent browser context management.
- Configurable concurrency and execution intervals.
- Application logging and JSON reports, where implemented.

## Architecture

```text
                  Configuration (YAML / CLI)
                            |
                            v
                 Browser Execution Engine
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
       Navigation       Session        Proxy
       & Interaction    Management     Management
             |              |              |
             +--------------+--------------+
                            |
                            v
                   Logs and Reports
```

## Requirements

- Python 3.8 or newer.
- Git.
- Playwright and its supported browser dependencies.
- Windows, macOS, or Linux.

For new deployments, use a currently supported Python release compatible with the project's dependencies.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/andikaputradev/website-traffic-generator.git
cd website-traffic-generator
```

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

On supported Linux systems, install browser system dependencies if needed:

```bash
python -m playwright install-deps chromium
```

## Usage

The following commands illustrate the intended command-line interface. Available options depend on the implementation in the checked-out repository.

### Run Browser Sessions

```bash
python run_traffic.py --url "https://example.com" --sessions 30 --concurrent 5
```

### Use a Proxy List

```bash
python run_traffic.py --url "https://example.com" --sessions 30 --concurrent 4 --proxy-file proxies.txt
```

### Load a YAML Configuration

```bash
python run_traffic.py --config config.yaml
```

Replace `example.com` with a website you own or have permission to test. Keep concurrency and request frequency within the target system's safe limits.

## Configuration

Example `config.yaml`:

```yaml
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
```

**Configuration note:** This is an example structure. Confirm that each key is supported by the version of the source code you are running; unused configuration values will not affect execution.

## Proxy Generation and Validation

If the repository contains `generate_proxies.py`, run it with:

```bash
python generate_proxies.py
```

Use trusted proxy providers or endpoints you are authorized to access. Public proxies may be unstable and can expose traffic or credentials to third parties.

## Scheduling

If the repository contains `run_scheduler.py`, start it with:

```bash
python run_scheduler.py
```

Scheduling intervals, recovery behavior, and supported options depend on the actual implementation.

## Deployment

For long-running workloads on Linux, use a dedicated unprivileged service account, an isolated virtual environment, resource limits, and persistent logs.

Example systemd unit:

```ini
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
```

Save it as `/etc/systemd/system/traffic-generator.service`. Update the user, directory, and entry point to match your deployment, then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now traffic-generator
sudo systemctl status traffic-generator
```

## Testing and Analytics Validation

Use controlled test cases to verify website behavior:

- Confirm analytics tags load.
- Verify event names and parameters.
- Test navigation and conversion flows.
- Check layouts across viewport sizes.
- Review logs and generated reports.

Automated activity must not be represented as genuine human engagement, organic search performance, or authentic advertising activity.

## Responsible Use

Use this software only on websites and infrastructure you own or are explicitly authorized to test.

- Do not generate fraudulent advertising clicks or impressions.
- Do not manipulate analytics or business metrics deceptively.
- Do not overload websites or third-party infrastructure.
- Respect access controls, rate limits, and applicable terms of service.
- Protect credentials, proxy details, and sensitive logs.

## Author

**Wahyu Andika Putra**  
Full-Stack Software Engineer · Cybersecurity Researcher  
Founder of **[AndikaDev](https://andikadev.com)**

| Channel | Link |
|---|---|
| Website | [andikadev.com](https://andikadev.com) |
| LinkedIn | [Wahyu Andika Putra](https://linkedin.com/in/wahyu-andika-putra) |
| GitHub | [@andikaputradev](https://github.com/andikaputradev) |
| Email | [wahyuandikaputra.co.id@gmail.com](mailto:wahyuandikaputra.co.id@gmail.com) |
| WhatsApp | [+62 877-3013-9582](https://wa.me/6287730139582) |
| Telegram | [@andikaputradev](https://t.me/andikaputradev) |
| Instagram | [@andikaputradev](https://instagram.com/andikaputradev) |
| TikTok | [@andikaputradev](https://tiktok.com/@andikaputradev) |

## Professional Services

Explore software development services at **[AndikaDev.com](https://andikadev.com)**.

- [Website Development](https://andikadev.com/layanan/pembuatan-website)
- [Mobile Application Development](https://andikadev.com/layanan/pembuatan-aplikasi)
- [Google Play Store Publishing](https://andikadev.com/layanan/upload-play-store)
- [Cybersecurity and Defensive Security](https://andikadev.com/layanan/keamanan-siber)
- [Web3 and Blockchain Development](https://andikadev.com/layanan/web3-blockchain)

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for the complete license terms.

Copyright (c) 2026 **Wahyu Andika Putra**  
[https://andikadev.com](https://andikadev.com)
