import concurrent.futures
import sys
import time
import urllib.request
import json

def send_request(url):
    try:
        start = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": "LoadGen/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            duration = time.time() - start
            return resp.status, duration, len(data)
    except Exception as e:
        return 500, 0, str(e)

def run_load_test(target_url, concurrency=10, duration_seconds=60):
    print(f"[*] Starting load test on: {target_url}")
    print(f"[*] Concurrency: {concurrency} workers | Duration: {duration_seconds}s")
    
    end_time = time.time() + duration_seconds
    total_reqs = 0
    success_reqs = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        while time.time() < end_time:
            futures = [executor.submit(send_request, target_url) for _ in range(concurrency)]
            for f in concurrent.futures.as_completed(futures):
                status, dur, _ = f.result()
                total_reqs += 1
                if status == 200:
                    success_reqs += 1
            print(f"Completed {total_reqs} requests (Success: {success_reqs}) ...", end="\r")
            time.sleep(0.1)

    print(f"\n[+] Test Finished! Total Requests: {total_reqs}, Successful: {success_reqs}")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000/heavy?iterations=4000000"
    conc = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    dur = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    run_load_test(url, conc, dur)
