#!/usr/bin/env python3
"""Check whether an inbox file is already filed, per a set's rename ledger.

Usage: dedup_check.py --file <path> --ledger <File Rename Ledger.csv>

Prints: NEW | DUPLICATE_MD5 | NAME_MATCH | LEDGER_MISSING, plus an md5 and a
pdftotext content hash (when available) so re-downloads can be compared by content.
"""
import argparse, csv, hashlib, os, subprocess, sys


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_text_sha1(path):
    if not path.lower().endswith(".pdf"):
        return None
    try:
        out = subprocess.run(["pdftotext", "-q", path, "-"], capture_output=True)
    except FileNotFoundError:
        return None
    if out.returncode == 0 and out.stdout.strip():
        return hashlib.sha1(out.stdout).hexdigest()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--ledger", required=True)
    a = ap.parse_args()

    if not os.path.exists(a.file):
        print("RESULT: ERROR"); print("file not found:", a.file); sys.exit(2)

    fmd5 = md5(a.file); fname = os.path.basename(a.file); ftext = pdf_text_sha1(a.file)
    print("file:", fname); print("md5:", fmd5)
    print("pdftext_sha1:", ftext if ftext else "(n/a)")

    if not os.path.exists(a.ledger):
        print("RESULT: LEDGER_MISSING")
        print("no ledger yet at", a.ledger, "- treat as NEW; create/append when filing")
        return

    md5_hits, name_hits = [], []
    with open(a.ledger, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("md5") and row["md5"] == fmd5:
                md5_hits.append(row)
            if row.get("original_name") == fname or os.path.basename(row.get("new_path", "")) == fname:
                name_hits.append(row)

    if md5_hits:
        print("RESULT: DUPLICATE_MD5")
        for r in md5_hits[:3]:
            print("  in ledger ->", r.get("action"), "|", r.get("new_path"), "|", r.get("notes"))
        print("Do NOT refile; dedupe-delete from the inbox and log it.")
    elif name_hits:
        print("RESULT: NAME_MATCH")
        for r in name_hits[:3]:
            print("  same name, different md5 ->", r.get("new_path"), "|", r.get("notes"))
        print("Likely a re-download. Compare content (pdftext_sha1 + vendor/date/amount) before refiling.")
    else:
        print("RESULT: NEW")
        print("Not in ledger. File it, then log with append_rename_ledger.py.")


if __name__ == "__main__":
    main()
