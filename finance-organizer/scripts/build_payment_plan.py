#!/usr/bin/env python3
"""Batch invoices into a <=daily-limit payment plan and write a Markdown table.

Usage:
  build_payment_plan.py --invoices invoices.(csv|json) [--limit 6000] [--currency CAD] \
      [--start-date YYYY-MM-DD] [--out plan.md] [--batch-name "May 2026 (Batch 3)"]

CSV/JSON fields per invoice: invoice, date (YYYY-MM-DD), description, amount, [gst].
Greedy oldest-first packing; an invoice larger than the limit gets its own day (flagged).
Dates are assigned consecutively from --start-date; adjust in the saved plan if needed.
"""
import argparse, csv, json, os, datetime, sys


def load(path):
    if path.lower().endswith(".json"):
        with open(path) as f:
            return json.load(f)
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def num(x):
    return float(str(x).replace("$", "").replace(",", "").strip() or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--invoices", required=True)
    ap.add_argument("--limit", type=float, default=6000.0)
    ap.add_argument("--currency", default="")
    ap.add_argument("--start-date", dest="start", default=datetime.date.today().isoformat())
    ap.add_argument("--out", default="")
    ap.add_argument("--batch-name", dest="batch", default="")
    a = ap.parse_args()

    inv = load(a.invoices)
    if not inv:
        sys.exit("no invoices found in " + a.invoices)
    for r in inv:
        r["amount"] = num(r.get("amount"))
        r["gst"] = num(r.get("gst")) if r.get("gst") else 0.0
    inv.sort(key=lambda r: (r.get("date", ""), str(r.get("invoice", ""))))

    days, cur, curtot = [], [], 0.0
    for r in inv:
        if cur and curtot + r["amount"] > a.limit:
            days.append(cur); cur, curtot = [], 0.0
        cur.append(r); curtot += r["amount"]
    if cur:
        days.append(cur)

    y, m, d = (int(x) for x in a.start.split("-"))
    cd = datetime.date(y, m, d)
    sym = (a.currency + " ") if a.currency else "$"

    title = f"Payment Plan - {a.batch}" if a.batch else "Payment Plan"
    out = [f"# {title}\n",
           f"_Daily limit {sym}{a.limit:,.0f}. {len(inv)} invoice(s) over {len(days)} day(s)._\n"]
    running = grand = 0.0
    for i, grp in enumerate(days, 1):
        dtot = sum(r["amount"] for r in grp)
        grand += dtot; running += dtot
        over = "  (exceeds daily limit)" if dtot > a.limit else ""
        out.append(f"\n## Day {i} - {cd.isoformat()} - {sym}{dtot:,.2f}{over}\n")
        out.append("| Invoice | Date | Description | Amount |")
        out.append("|---|---|---|---:|")
        for r in grp:
            out.append(f"| {r.get('invoice','')} | {r.get('date','')} | "
                       f"{r.get('description','')} | {sym}{r['amount']:,.2f} |")
        out.append(f"| | | **Day total** | **{sym}{dtot:,.2f}** |")
        out.append(f"| | | Running total | {sym}{running:,.2f} |")
        cd += datetime.timedelta(days=1)

    gst = sum(r["gst"] for r in inv)
    out.append(f"\n**Grand total: {sym}{grand:,.2f}**" + (f" (incl. tax {sym}{gst:,.2f})" if gst else ""))
    text = "\n".join(out) + "\n"

    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w") as f:
            f.write(text)
        print("wrote", a.out)
    print(f"{len(inv)} invoice(s) -> {len(days)} day(s); grand total {sym}{grand:,.2f}")


if __name__ == "__main__":
    main()
