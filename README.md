# 🕵️ HackerNews Stealth Scraper & Analyzer

A privacy-focused Data Engineering pipeline that performs anonymous ETL operations on Hacker News using **Tor Network routing** and **SOCKS5 proxies**.

## 🚀 Key Features

* **Anonymous Extraction:** Routes requests via SOCKS5/Tor to prevent fingerprinting.
* **Resilient Crawler:** Implements pagination, random delays, and User-Agent rotation.
* **ETL Pipeline:** Extracts HTML, cleanses data, and loads into structured CSV.
* **Visualization:** Generates trend analysis charts.

## 🛠️ Tech Stack

* **Python 3.10+**
* **ProxyChains / Tor**
* **Pandas & Matplotlib**

## 📦 How to Run

1. **Install Dependencies:**
   `pip install -r requirements.txt`

2. **Run Extractor (Safe Mode):**
   `MY_PROXY_URL="socks5h://127.0.0.1:9050" python3 etl_extractor.py`

3. **Visualize:**
   `python3 visualizer.py`

