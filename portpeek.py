#!/usr/bin/env python3
"""portpeek: peek at processes listening on TCP ports."""

import argparse
import json as _json
import os
import re
import signal
import subprocess
import sys


def run_lsof():
    """Run lsof and return its stdout text."""
    try:
        result = subprocess.run(
            ["lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        print("error: 'lsof' not found on PATH", file=sys.stderr)
        sys.exit(2)
    if result.returncode not in (0, 1):  # 1 == no results
        msg = result.stderr.strip() or "lsof failed"
        print(f"error: {msg}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


def parse(text):
    """Parse lsof output into a list of dicts."""
    rows = []
    lines = text.splitlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 9:
            continue
        name = " ".join(parts[8:])
        match = re.search(r":(\d+)", name)
        if not match:
            continue
        rows.append(
            {
                "command": parts[0],
                "pid": int(parts[1]),
                "user": parts[2],
                "address": name,
                "port": int(match.group(1)),
            }
        )
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="portpeek", description="Peek at processes listening on TCP ports."
    )
    parser.add_argument("port", nargs="?", type=int, help="filter by port number")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--kill", action="store_true", help="terminate matching processes")
    args = parser.parse_args(argv)

    rows = parse(run_lsof())
    if args.port is not None:
        rows = [r for r in rows if r["port"] == args.port]

    if args.json:
        print(_json.dumps(rows, indent=2))
        return 0

    if not rows:
        print("no listening processes found")
        return 0

    print(f"{'PORT':>6}  {'PID':>7}  {'USER':<12}  {'COMMAND':<20}  ADDRESS")
    for r in sorted(rows, key=lambda x: x["port"]):
        print(
            f"{r['port']:>6}  {r['pid']:>7}  {r['user']:<12}  "
            f"{r['command']:<20}  {r['address']}"
        )

    if args.kill:
        for r in rows:
            try:
                os.kill(r["pid"], signal.SIGTERM)
                print(f"killed {r['pid']} ({r['command']})")
            except OSError as exc:
                print(f"failed to kill {r['pid']}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
