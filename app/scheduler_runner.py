import json
import subprocess
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

scheduler = BackgroundScheduler()


def run_job():
    try:
        with open("app/config.json", "r") as f:
            cfg = json.load(f)

        cmd = [
            sys.executable,
            "main.py",
            "--country",
            str(cfg["country"]),
            "--topic-category",
            str(cfg["category_code"]),
            "--wordpress-sync",
            "--wordpress-status",
            "draft"
        ]

        print("\n" + "=" * 60)
        print("Running:", " ".join(cmd))
        print("=" * 60)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode != 0:
            print(
                f"Process exited with code {result.returncode}"
            )

    except Exception as e:
        print(f"Scheduler job failed: {e}")


def start_scheduler():
    try:
        with open("app/config.json", "r") as f:
            cfg = json.load(f)

        interval = int(cfg["interval_minutes"])

        scheduler.remove_all_jobs()

        scheduler.add_job(
            run_job,
            trigger="interval",
            minutes=interval,
            id="trend_agent",
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

        if scheduler.state != STATE_RUNNING:
            scheduler.start()

        print(
            f"Scheduler configured: every {interval} minute(s)"
        )

    except Exception as e:
        print(f"Failed to start scheduler: {e}")