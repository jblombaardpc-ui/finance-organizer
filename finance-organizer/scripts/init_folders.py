#!/usr/bin/env python3
"""Create/refresh a finance-organizer user's folder structure from their config.

Usage: init_folders.py --config .finance-organizer/config.yaml [--base <working folder>]

Idempotent (mkdir -p). Lays out the Finance Inbox plus a tidy tree for each set of
books so every document has a home and the structure stays consistent. Safe to re-run
any time the structure drifts.
"""
import argparse, os, sys

# Per references/conventions.md "Folder structure (per set)":
# business sets keep Receipts/ at the set root (subfolders YYYY-MM/ appear as receipts are filed).
BUSINESS = ["Income", "Expenses", "Receipts", "Travel", "Bank Statements", "Reports"]
PERSONAL = ["Bank Statements", "Receipts", "Property", "Investments", "Insurance", "Tax", "Reports"]


def main():
    try:
        import yaml
    except ImportError:
        sys.exit("pyyaml required: pip install pyyaml --break-system-packages")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--base", default="")
    a = ap.parse_args()

    with open(a.config) as f:
        cfg = yaml.safe_load(f)
    base = a.base or os.path.dirname(os.path.dirname(os.path.abspath(a.config)))
    backend = cfg.get("ledger", {}).get("backend", "beancount")
    modules = cfg.get("modules", {}) or {}
    created = []

    def mk(rel):
        full = os.path.join(base, rel)
        if not os.path.isdir(full):
            os.makedirs(full, exist_ok=True)
            created.append(rel)

    mk(cfg.get("filing", {}).get("inbox", "Finance Inbox"))
    for s in cfg.get("sets_of_books", []):
        folder = s.get("folder") or s["id"]
        for d in (BUSINESS if s.get("type") == "business" else PERSONAL):
            mk(os.path.join(folder, d))
        mk(os.path.join(folder, "Beancount" if backend == "beancount" else "Ledger"))
        if modules.get("claims_helper") and s.get("type") == "personal":
            mk(os.path.join(folder, "Claims"))
        if modules.get("payment_plan") and s.get("type") == "business":
            mk(os.path.join(folder, "Payment Plans"))

    # Overlap: the copies dir for business expenses paid on personal accounts,
    # plus the Candidates subfolder file-inbox relies on (see conventions.md).
    ov = cfg.get("overlap", {}) or {}
    if ov:
        copies = ov.get("personal_card_expense_copies_dir")
        if not copies:
            biz = [s for s in cfg.get("sets_of_books", []) if s.get("type") == "business"]
            if biz:
                folder = biz[0].get("folder") or biz[0]["id"]
                copies = os.path.join(folder, "Expenses", "Paid on Personal Accounts")
        if copies:
            mk(copies)
            mk(os.path.join(copies, "Candidates (pending review)"))

    print(f"folders ready under {base}: {len(created)} created, rest already existed")
    for c in created:
        print("  +", c)


if __name__ == "__main__":
    main()
