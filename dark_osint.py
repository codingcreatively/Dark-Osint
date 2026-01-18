import requests
import socks
import socket
import sys
import re
import time
import json
import random
from collections import Counter, deque
from urllib.parse import urlparse
from tqdm import tqdm
from colorama import Fore, Style

# ===================== USER AGENTS =====================
USER_AGENTS = {
    "1": "Mozilla/5.0 (Windows NT 10.0; rv:119.0) Gecko/20100101 Firefox/119.0",
    "2": "Mozilla/5.0 (X11; Linux x86_64; TorBrowser/13.0) Gecko/20100101 Firefox/115.0",
    "3": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
}

# ===================== DARK BANNER =====================
BANNER = f"""
{Fore.RED}{Style.BRIGHT}
██████╗  █████╗ ██████╗ ██╗  ██╗     ██████╗  ██████╗ ██╗███╗   ██╗████████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝     ██╔═══██╗██╔════╝ ██║████╗  ██║╚══██╔══╝
██║  ██║███████║██████╔╝█████╔╝      ██║   ██║███████╗██║██╔██╗ ██║   ██║   
██║  ██║██╔══██║██╔══██╗██╔═██╗      ██║   ██║╚════██║██║██║╚██╗██║   ██║   
██████╔╝██║  ██║██║  ██║██║  ██╗     ╚██████╔╝███████║██║██║ ╚████║   ██║   
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   

{Fore.CYAN}Dark Osint – Onion Intelligence Framework
{Fore.MAGENTA}Author     : Alexxx
{Fore.YELLOW}Instagram  : @arcane.__01
{Fore.WHITE}════════════════════════════════════════════════════════════════════════
"""


# ===================== CRAWLER =====================
class TorOnionCrawler:

    def __init__(self):
        self.base_onion_dirs = [
            "http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion",
            "http://darkweblistd25olwffudgvtnr5yvalwcbnf7g5ftysnv4wzzxey2id.onion",
            "http://tor.taxi",
            "http://dark.fail",
            "http://onion.live",
            "http://ahmia.fi"
        ]
        self.setup_tor()
        self.reset()

    def reset(self):
        self.results = []
        self.visited = set()
        self.keyword_scores = Counter()

    # ===================== TOR =====================
    def setup_tor(self):
        try:
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            self.session = requests.Session()
            print(f"{Fore.GREEN}✓ Tor connected (127.0.0.1:9050)")
        except Exception as e:
            print(f"{Fore.RED}Tor error: {e}")
            sys.exit(1)

    def check_tor(self):
        try:
            r = self.session.get("http://httpbin.org/ip", timeout=10)
            print(f"{Fore.GREEN}✓ Tor IP: {r.json()['origin']}")
            return True
        except:
            return False

    # ===================== USER AGENT =====================
    def choose_user_agent(self):
        print(f"""
{Fore.CYAN}[ User-Agent Selection ]
1) Firefox
2) Tor Browser
3) Chrome
4) Random
""")
        choice = input("Select UA [4]: ").strip() or "4"

        if choice == "4":
            ua = random.choice(list(USER_AGENTS.values()))
        else:
            ua = USER_AGENTS.get(choice, USER_AGENTS["2"])

        self.session.headers.update({"User-Agent": ua})
        print(f"{Fore.GREEN}✓ User-Agent set")

    # ===================== PAGE CRAWL =====================
    def crawl_page(self, url, keywords, depth, max_depth):
        if depth > max_depth or url in self.visited:
            return []

        self.visited.add(url)
        print(f"{Fore.CYAN}[DEPTH {depth}] {urlparse(url).netloc}")

        try:
            r = self.session.get(url, timeout=20)
            if r.status_code != 200:
                return []

            content = r.text.lower()
            score = sum(content.count(k) for k in keywords)

            links = set(re.findall(
                r'https?://[a-z2-7]{16,56}\.onion',
                content
            ))

            self.results.append({
                "url": url,
                "keyword_score": score,
                "status": r.status_code,
                "depth": depth
            })

            return list(links)

        except:
            return []

    # ===================== SMART CRAWL =====================
    def smart_crawl(self, keywords, max_depth, max_sites):
        queue = deque()

        for seed in self.base_onion_dirs:
            queue.append((seed, 0))

        with tqdm(total=max_sites, desc="🕷 Dark OSINT Crawl", colour="red") as bar:

            while queue and len(self.results) < max_sites:
                url, depth = queue.popleft()

                links = self.crawl_page(url, keywords, depth, max_depth)
                bar.update(1)

                time.sleep(1)

                for link in links:
                    if link not in self.visited and depth + 1 <= max_depth:
                        queue.append((link, depth + 1))

    # ===================== RESULTS =====================
    def rank(self, top_n):
        return sorted(
            self.results,
            key=lambda x: x["keyword_score"],
            reverse=True
        )[:top_n]

    def show_results(self, results):
        print(f"\n{Fore.RED}{'='*90}")
        print(f"{Fore.WHITE}Rank  Score  Depth  Status  URL")
        print(f"{Fore.RED}{'='*90}")
        for i, r in enumerate(results, 1):
            print(f"{i:<4}  {r['keyword_score']:<5}  {r['depth']:<5}  {r['status']:<6}  {r['url']}")
        print(f"{Fore.RED}{'='*90}")

    def save(self, keywords):
        name = f"dark_osint_{'_'.join(keywords)}_{int(time.time())}.json"
        with open(name, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"{Fore.GREEN}✓ Saved: {name}")

# ===================== MAIN =====================
def get_keywords():
    raw = input(f"{Fore.YELLOW}Enter keywords: {Style.RESET_ALL}")
    return [k.lower() for k in re.split(r"[,\s]+", raw) if k]

def main():
    print(BANNER)

    crawler = TorOnionCrawler()
    if not crawler.check_tor():
        print(f"{Fore.RED}Tor not running!")
        return

    crawler.choose_user_agent()

    while True:
        crawler.reset()

        keywords = get_keywords()
        if not keywords:
            continue

        depth = min(int(input("Max depth [10]: ") or 10), 10)
        max_sites = int(input("Max sites [100]: ") or 100)
        top_n = int(input("Top results [20]: ") or 20)

        crawler.smart_crawl(keywords, depth, max_sites)
        results = crawler.rank(top_n)
        crawler.show_results(results)

        if input("Save results? (y/n): ").lower() == "y":
            crawler.save(keywords)

        if input("\n[1] New Search\n[2] Exit\nSelect: ") != "1":
            break

    print(f"{Fore.GREEN}Exiting Dark OSINT")

if __name__ == "__main__":
    main()