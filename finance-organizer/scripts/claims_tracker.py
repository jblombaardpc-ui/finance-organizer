#!/usr/bin/env python3
"""Maintain a per-period benefit/health claim tracker (CSV) and report totals.

Usage:
  claims_tracker.py --tracker "Claims/claim-2026.csv" \
      --item "Patient|YYYY-MM-DD|Description|Amount|Y" [--item "..."] \
      [--admin-fee-pct 0.05] [--tax-on-fee-pct 0.05]

Each --item is  Patient|ServiceDate|Description|Amount|Eligible(Y/N).
Appends rows (creating the header if needed), then reports cumulative totals for the
period: Total Claim (eligible only), admin fee, tax on fee, and Total Payable.
"""
import argparse, csv, os, sys

HEADER = ["date", "patient", "description", "amount", "eligible", "notes"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracker", required=True)
    ap.add_argument("--item", action="append", default=[])
    ap.add_argument("--admin-fee-pct", type=float, default=0.0, dest="admin")
    ap.add_argument("--tax-on-fee-pct", type=float, default=0.0, dest="tax")
    a = ap.parse_args()

    # Validate ALL items first so a bad one can't leave a partial append.
    rows = []
    for it in a.item:
        parts = [p.strip() for p in it.split("|")]
        if len(parts) < 4:
            sys.exit(f"Bad --item (need Patient|Date|Desc|Amount[|Y/N]): {it}")
        if len(parts) > 5:
            sys.exit(f"Too many '|' fields in --item: {it}\n"
                     "  '|' is the field separator — remove it from the description "
                     "(use a dash or 'and' instead).")
        patient, sdate, desc, amt = parts[0], parts[1], parts[2], parts[3]
        elig = (parts[4] if len(parts) > 4 else "Y").upper()[:1]
        try:
            amt = float(amt)
        except ValueError:
            sys.exit(f"Bad amount in --item: {parts[3]}")
        rows.append([sdate, patient, desc, f"{amt:.2f}", elig, ""])

    d = os.path.dirname(a.tracker)
    if d:
        os.makedirs(d, exist_ok=True)
    need_header = not os.path.exists(a.tracker)
    with open(a.tracker, "a", newline="") as f:
        w = csv.writer(f)
        if need_header:
            w.writerow(HEADER)
        for row in rows:
            w.writerow(row)

    # cumulative totals over eligible rows
    total = 0.0
    excluded = 0.0
    with open(a.tracker, newline="") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (ValueError, KeyError):
                continue
            if row.get("eligible", "Y").upper().startswith("Y"):
                total += amt
            else:
                excluded += amt
    fee = round(total * a.admin, 2)
    tax = round(fee * a.tax, 2)
    payable = round(total + fee + tax, 2)
    print(f"tracker: {os.path.basename(a.tracker)} (+{len(a.item)} line(s))")
    print(f"Total Claim (eligible): {total:.2f} | Admin fee: {fee:.2f} | Tax on fee: {tax:.2f} | Total Payable: {payable:.2f}")
    if excluded:
        print(f"(excluded as ineligible: {excluded:.2f})")


if __name__ == "__main__":
    main()
