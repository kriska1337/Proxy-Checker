import requests
import threading
from queue import Queue
import time
from typing import List, Tuple
import argparse

class ProxyChecker:
    def __init__(self, proxy_list: List[str], threads: int = 50, timeout: int = 10):
        self.proxy_list = proxy_list
        self.working_proxies = []
        self.queue = Queue()
        self.threads = threads
        self.test_url = "http://www.google.com"
        self.timeout = timeout
        
    def check_proxy(self, proxy: str) -> Tuple[str, float] | None:
        try:
            start_time = time.time()
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            
            response = requests.get(
                self.test_url,
                proxies=proxies,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                response_time = time.time() - start_time
                return (proxy, response_time)
            return None
            
        except Exception:
            return None

    def worker(self):
        while True:
            try:
                proxy = self.queue.get_nowait()
            except:
                break
                
            result = self.check_proxy(proxy)
            if result:
                self.working_proxies.append(result)
            self.queue.task_done()

    def check_proxies(self):
        for proxy in self.proxy_list:
            self.queue.put(proxy)

        threads = []
        for _ in range(min(self.threads, len(self.proxy_list))):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.working_proxies.sort(key=lambda x: x[1])
        return self.working_proxies

    def save_results(self, filename: str):
        with open(filename, "w") as f:
            for proxy, _ in self.working_proxies:  
                f.write(f"{proxy}\n")

def load_proxies(filename: str) -> List[str]:
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
        return []

def main():
    parser = argparse.ArgumentParser(description="HTTP Proxy Checker")
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="proxies.txt",
        help="Input file with proxies (default: proxies.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="checked.txt",
        help="Output file for working proxies (default: checked.txt)"
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=50,
        help="Number of threads (default: 50)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Connection timeout in seconds (default: 10)"
    )

    args = parser.parse_args()

    proxy_list = load_proxies(args.input)
    
    if not proxy_list:
        print("Список прокси пуст!")
        return

    print(f"Загружено {len(proxy_list)} прокси из {args.input}")
    print(f"Используется {args.threads} потоков, таймаут {args.timeout} секунд")
    
    checker = ProxyChecker(proxy_list, threads=args.threads, timeout=args.timeout)
    start_time = time.time()
    
    working_proxies = checker.check_proxies()
    
    checker.save_results(args.output)
    
    execution_time = time.time() - start_time
    print(f"Проверка завершена за {execution_time:.1f} секунд")
    print(f"Найдено {len(working_proxies)} рабочих прокси")
    print(f"Результаты сохранены в {args.output}")
    if working_proxies:
        print(f"Лучший прокси: {working_proxies[0][0]} ({working_proxies[0][1]:.1f}s)")

if __name__ == "__main__":
    main()
