"""Self-initiated API monitoring demonstration.

Reads endpoint configuration, performs health checks, writes structured logs,
and exits non-zero when one or more checks fail.
"""
from __future__ import annotations

import json
import logging
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    status: int | None
    elapsed_ms: int
    error: str | None = None

def check_endpoint(name: str, url: str, timeout: int) -> CheckResult:
    started = time.perf_counter()
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "portfolio-api-monitor/1.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            elapsed = round((time.perf_counter() - started) * 1000)
            return CheckResult(name, 200 <= response.status < 400, response.status, elapsed)
    except (urllib.error.URLError, TimeoutError) as exc:
        elapsed = round((time.perf_counter() - started) * 1000)
        return CheckResult(name, False, None, elapsed, str(exc.reason if hasattr(exc, "reason") else exc))

def main() -> int:
    config = json.loads(Path("endpoints.json").read_text(encoding="utf-8"))
    results = [check_endpoint(item["name"], item["url"], item.get("timeout_seconds", 5)) for item in config["endpoints"]]
    Path("latest-report.json").write_text(json.dumps([result.__dict__ for result in results], indent=2), encoding="utf-8")
    for result in results:
        logging.info("%s | status=%s | %sms | %s", result.name, result.status, result.elapsed_ms, "OK" if result.ok else result.error)
    return 0 if all(result.ok for result in results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
