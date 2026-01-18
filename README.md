# Dark Osint â Onion Intelligence Framework

![Dark Osint Banner](https://img.shields.io/badge/Dark-OSINT-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Dark Osint** is a Python-based Dark Web OSINT (Open Source Intelligence) crawler and analyzer.  
It is designed to crawl `.onion` sites anonymously over Tor, extract and rank pages based on keyword relevance, and save the results for offline analysis.

---

## Features

- Anonymous crawling through **Tor network** (SOCKS5 proxy at 127.0.0.1:9050)
- Crawl multiple `.onion` directories (Dark Fail, Tor Taxi, Dark Web List, etc.)
- **Customizable User-Agent selection** for stealth
- Configurable **maximum depth** (default 10)
- Keyword-based ranking system
- Progress tracking via **TQDM** CLI progress bar
- Save results to **JSON** files
- Color-coded professional CLI interface
- Modular, easy to extend with new engines or features
