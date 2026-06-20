#!/usr/bin/env python3
"""Read a dotted key from the finance-organizer config and print its value.

Usage: config_get.py --config .finance-organizer/config.yaml --key company.locality.region
List items are addressed by index: --key accounts.0.last4
Missing keys print nothing and exit 1. Dict/list values print as JSON.
"""
import argparse, sys


def main():
    try:
        import yaml
    except ImportError:
        sys.exit("pyyaml required: pip install pyyaml --break-system-packages")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--key", required=True)
    a = ap.parse_args()

    with open(a.config) as f:
        cur = yaml.safe_load(f)
    for part in a.key.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                sys.exit(1)
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            sys.exit(1)
    if isinstance(cur, (dict, list)):
        import json
        print(json.dumps(cur, ensure_ascii=False))
    else:
        print(cur)


if __name__ == "__main__":
    main()
