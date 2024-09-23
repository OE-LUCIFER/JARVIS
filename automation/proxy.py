import random
import threading
import requests
import time
import json
import os
import concurrent.futures

DATA_FOLDER = "DATA"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PROXY_FILE = os.path.join(DATA_FOLDER, "proxies.json")

class ProxyManager:
    def __init__(self, refresh_interval=60):
        self.refresh_interval = refresh_interval
        self.proxies = self.load_proxies()
        self.last_refresh = 0
        self.thread = None
        self.running = False

    def load_proxies(self):
        """Loads proxies from a JSON file."""
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Error decoding proxies.json. Starting with an empty list.")
                    return []
        return []

    def save_proxies(self):
        """Saves proxies to a JSON file."""
        with open(PROXY_FILE, "w") as f:
            json.dump(self.proxies, f, indent=2)

    def fetch_proxies(self, limit=50):
        """Fetches a list of proxies from a proxy scraping service."""
        try:
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
            response = requests.get(url)
            proxies = response.text.split('\r\n')
            return [proxy for proxy in proxies if proxy][:limit]
        except Exception as e:
            print(f"Error fetching proxies: {e}")
            return []

    def test_proxy(self, proxy):
        """Tests a proxy for functionality and returns its response time."""
        try:
            start_time = time.time()
            response = requests.get('http://httpbin.org/ip', 
                                    proxies={'http': proxy, 'https': proxy}, 
                                    timeout=5) 
            end_time = time.time()
            if response.status_code == 200:
                return proxy, end_time - start_time
        except:
            pass
        return None

    def refresh_proxies(self):
        """Fetches new proxies, tests them, and updates the proxy list."""
        new_proxies = self.fetch_proxies(limit=50)  # Fetch only 50 proxies
        working_proxies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in new_proxies}
            for future in concurrent.futures.as_completed(future_to_proxy):
                result = future.result()
                if result:
                    working_proxies.append(result)
                    # print(f'{result[0]} (Response time: {result[1]:.2f} seconds)')  # Removed print

        self.proxies = [proxy for proxy, _ in working_proxies] 
        self.save_proxies()

    def get_proxy(self):
        """Returns a random proxy from the list."""
        if self.proxies:
            return random.choice(self.proxies)
        else:
            return None

    def run(self):
        """Continuously refreshes the proxy list at the specified interval."""
        self.running = True
        while self.running:
            current_time = time.time()
            if current_time - self.last_refresh >= self.refresh_interval:
                self.last_refresh = current_time
                self.refresh_proxies()
            time.sleep(1)

    def start(self):
        """Starts the proxy refresh thread if it's not already running."""
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        """Stops the proxy refresh thread."""
        self.running = False
        if self.thread:
            self.thread.join() 