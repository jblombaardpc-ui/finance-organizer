#!/usr/bin/env python3
"""Append a row to a set's File Rename Ledger.csv (creates the header if missing).

Usage:
  append_rename_ledger.py --ledger <csv> --new <new_path> \
      [--original <orig_path_or_name>] [--action move] \
      [--fiscal-year ""] [--notes ""] [--base <dir>]

Computes the md5 of --new (also for delete/dedupe-delete rows, when the file
still exists at logging time — log BEFORE deleting). With --base, new_path is
stored relative to that dir.
Actions are free text; common: move, folder-rename, dedupe-delete, delete, copy, generate.
"""
import argparse, csv, hashlib, os, datetime, sys

HEADER = ["timestamp", "action", "fiscal_year", "original_path",
          "original_name", "md5", "new_path", "notes"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--original", default="")
    ap.add_argument("--action", default="move")
    ap.add_argument("--fiscal-year", dest="fy", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--base", default="")
    a = ap.parse_args()

    is_delete = a.action in ("dedupe-delete", "delete")
    if not is_delete and not os.path.exists(a.new):
        print("ERROR: new file not found:", a.new); sys.exit(2)

    digest = md5(a.new) if os.path.exists(a.new) else ""
    new_p = os.path.relpath(a.new, a.base) if a.base else a.new
    orig_name = os.path.basename(a.original) if a.original else ""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    need_header = not os.path.exists(a.ledger)
    d = os.path.dirname(a.ledger)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(a.ledger, "a", newline="") as f:
        w = csv.writer(f)
        if need_header:
            w.writerow(HEADER)
        w.writerow([ts, a.action, a.fy, a.original, orig_name, digest, new_p, a.notes])
    print("appended:", ts, a.action, "|", new_p, "| md5", digest or "(none)")


if __name__ == "__main__":
    main()
