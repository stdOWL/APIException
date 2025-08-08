"""
Ultimate Professional Benchmark Script for APIException

This script:
1️⃣ Runs Locust tests for both apps (control_app & test_app)
2️⃣ Collects CPU/RAM usage via `docker stats`
3️⃣ Parses Locust CSV outputs for latency/RPS metrics
4️⃣ Generates plots (latency comparison, RPS, CPU/RAM usage)
5️⃣ Saves a summary markdown + charts for Reddit/blog posts
"""

import subprocess
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==========================
# CONFIG
# ==========================
LOCUST_USERS = 500           # kaç concurrent user
LOCUST_SPAWN_RATE = 50       # saniyede kaç user spawn edilecek
LOCUST_RUN_TIME = "2m"       # test süresi
CONTROL_HOST = "http://localhost:8001"
TEST_HOST = "http://localhost:8002"
OUTPUT_DIR = "benchmark_results"

# ==========================
# UTILS
# ==========================
def run_locust(target_name: str, host: str):
    """
    Runs locust in headless mode for the given target (control/test)
    Saves CSV results into OUTPUT_DIR/<target_name>_*.csv
    """
    cmd = [
        "locust", "-f", "benchmark/locustfile.py",
        "--headless",
        "-u", str(LOCUST_USERS),
        "-r", str(LOCUST_SPAWN_RATE),
        "-t", LOCUST_RUN_TIME,
        "--csv", f"{OUTPUT_DIR}/{target_name}",
        "--host", host
    ]
    print(f"🚀 Running Locust for {target_name} ({host})...")
    subprocess.run(cmd, check=True)


def collect_docker_stats(stop_event):
    """
    Collects docker CPU/RAM stats while Locust is running.
    Writes stats to OUTPUT_DIR/docker_stats.csv
    """
    with open(f"{OUTPUT_DIR}/docker_stats.csv", "w") as f:
        f.write("timestamp,container,cpu,mem\n")
        while not stop_event.is_set():
            # docker stats --no-stream --format ...
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format", "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"],
                capture_output=True, text=True
            )
            now = datetime.now().strftime("%H:%M:%S")
            for line in result.stdout.strip().split("\n"):
                f.write(f"{now},{line}\n")
            time.sleep(2)  # every 2 sec


def parse_locust_results():
    """
    Reads locust CSVs, computes metrics (p50/p95/p99 latency, RPS).
    Returns Pandas DataFrames for control & test.
    """
    control_df = pd.read_csv(f"{OUTPUT_DIR}/control_stats.csv")
    test_df = pd.read_csv(f"{OUTPUT_DIR}/test_stats.csv")

    # TODO: extract metrics (we’ll calculate p50/p95/p99 etc.)
    return control_df, test_df


def plot_results(control_df, test_df):
    """
    Generates comparison charts (latency, RPS) & saves them as PNG.
    """
    # TODO: matplotlib plots (latency distribution, RPS, CPU usage)
    pass


def generate_summary_report():
    """
    Create a Markdown summary with metrics and attach plot references.
    """
    # TODO: generate report.md
    pass


# ==========================
# MAIN BENCHMARK LOGIC
# ==========================
if __name__ == "__main__":
    print("📊 Starting Ultimate Professional Benchmark...")

    # ✅ 1. Docker stats thread başlat
    stop_event = threading.Event()
    stats_thread = threading.Thread(target=collect_docker_stats, args=(stop_event,))
    stats_thread.start()

    # ✅ 2. Locust’u control_app için çalıştır
    run_locust("control", CONTROL_HOST)

    # ✅ 3. Locust’u test_app için çalıştır
    run_locust("test", TEST_HOST)

    # ✅ 4. Docker stats thread’i durdur
    stop_event.set()
    stats_thread.join()

    # ✅ 5. Sonuçları işle & plot
    control_df, test_df = parse_locust_results()
    plot_results(control_df, test_df)

    # ✅ 6. Markdown summary üret
    generate_summary_report()

    print("✅ Benchmark completed! Check benchmark_results/ for outputs.")