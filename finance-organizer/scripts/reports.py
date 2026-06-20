#!/usr/bin/env python3
"""Generate basic financial statements from the configured ledger.

Usage:
  reports.py --config .finance-organizer/config.yaml --set <set-id> \
      --period <YYYY | YYYY-MM | YYYY-Qn> [--out report.md] [--csv <ledger.csv>]

Beancount backend: reads the set's ledger via the loader -> income statement (period
flows) + balance sheet (as of period end, with earnings-to-date folded into equity so
it balances). Simple backend: aggregates the set's CSV ledger by category for the
period (income/cash summary; a full balance sheet needs the Beancount backend).
Operating currency comes from the config. Writes/prints Markdown.
"""
import argparse, csv, os, sys, datetime, calendar


def period_bounds(p):
    p = p.strip().upper()
    if len(p) == 4 and p.isdigit():
        y = int(p); return datetime.date(y, 1, 1), datetime.date(y, 12, 31)
    if "-Q" in p:
        ys, qs = p.split("-Q"); y = int(ys); q = int(qs)
        m0 = (q - 1) * 3 + 1; m1 = m0 + 2
        return datetime.date(y, m0, 1), datetime.date(y, m1, calendar.monthrange(y, m1)[1])
    if len(p) == 7 and p[4] == "-":
        y = int(p[:4]); m = int(p[5:7])
        return datetime.date(y, m, 1), datetime.date(y, m, calendar.monthrange(y, m)[1])
    raise SystemExit(f"bad --period: {p} (use YYYY, YYYY-MM, or YYYY-Qn)")


def money(x):
    return f"{float(x):,.2f}"


def beancount_report(ledger_main, start, end, cur):
    from beancount import loader
    from beancount.core import data
    entries, errors, _ = loader.load_file(ledger_main)
    if errors:
        print(f"; note: {len(errors)} ledger error(s) ignored for reporting", file=sys.stderr)
    is_acc, bs_acc, earn = {}, {}, 0.0
    for e in entries:
        if not isinstance(e, data.Transaction):
            continue
        for p in e.postings:
            if p.units is None or p.units.currency != cur:
                continue
            amt = float(p.units.number)
            root = p.account.split(":")[0]
            if root in ("Income", "Expenses"):
                if start <= e.date <= end:
                    is_acc[p.account] = is_acc.get(p.account, 0.0) + amt
                if e.date <= end:
                    earn += amt
            elif root in ("Assets", "Liabilities", "Equity") and e.date <= end:
                bs_acc[p.account] = bs_acc.get(p.account, 0.0) + amt
    return is_acc, bs_acc, -earn  # earnings-to-date positive = -(income+expense postings)


def fmt_is(is_acc, cur):
    rev = {a: -v for a, v in is_acc.items() if a.startswith("Income")}
    exp = {a: v for a, v in is_acc.items() if a.startswith("Expenses")}
    tr, te = sum(rev.values()), sum(exp.values())
    out = ["## Income statement", "", "**Revenue**"]
    out += [f"- {a}: {money(v)} {cur}" for a, v in sorted(rev.items())] or ["- (none)"]
    out += [f"- **Total revenue: {money(tr)} {cur}**", "", "**Expenses**"]
    out += [f"- {a}: {money(v)} {cur}" for a, v in sorted(exp.items())] or ["- (none)"]
    out += [f"- **Total expenses: {money(te)} {cur}**", "", f"**Net income: {money(tr - te)} {cur}**"]
    return "\n".join(out)


def fmt_bs(bs_acc, earn, cur):
    assets = {a: v for a, v in bs_acc.items() if a.startswith("Assets")}
    liab = {a: -v for a, v in bs_acc.items() if a.startswith("Liabilities")}
    eq = {a: -v for a, v in bs_acc.items() if a.startswith("Equity")}
    ta, tl, teq = sum(assets.values()), sum(liab.values()), sum(eq.values()) + earn
    out = ["## Balance sheet (as of period end)", "", "**Assets**"]
    out += [f"- {a}: {money(v)} {cur}" for a, v in sorted(assets.items())] or ["- (none)"]
    out += [f"- **Total assets: {money(ta)} {cur}**", "", "**Liabilities**"]
    out += [f"- {a}: {money(v)} {cur}" for a, v in sorted(liab.items())] or ["- (none)"]
    out += [f"- **Total liabilities: {money(tl)} {cur}**", "", "**Equity**"]
    out += [f"- {a}: {money(v)} {cur}" for a, v in sorted(eq.items())]
    out += [f"- Earnings to date (not yet closed): {money(earn)} {cur}",
            f"- **Total equity: {money(teq)} {cur}**", ""]
    bal = "balances" if abs(ta - (tl + teq)) < 0.01 else "DOES NOT BALANCE"
    out += [f"_Check: assets {money(ta)} vs liabilities + equity {money(tl + teq)} -> {bal}_"]
    return "\n".join(out)


def simple_report(csv_path, start, end, cur):
    cats, accts = {}, {}
    with open(csv_path, newline="") as f:
        for r in csv.DictReader(f):
            try:
                dd = datetime.date.fromisoformat((r.get("date") or "").strip())
            except ValueError:
                continue
            if not (start <= dd <= end):
                continue
            net = (float(r.get("money_in") or 0) - float(r.get("money_out") or 0))
            cats[r.get("category") or "(uncategorized)"] = cats.get(r.get("category") or "(uncategorized)", 0.0) + net
            accts[r.get("account") or "(unknown)"] = accts.get(r.get("account") or "(unknown)", 0.0) + net
    inflow = sum(v for v in cats.values() if v > 0)
    outflow = sum(-v for v in cats.values() if v < 0)
    out = ["## Income / cash summary (simple ledger)", "", "**By category (net in - out)**"]
    out += [f"- {c}: {money(v)} {cur}" for c, v in sorted(cats.items(), key=lambda kv: -kv[1])]
    out += [f"- **Net: {money(inflow - outflow)} {cur}**  (in {money(inflow)} / out {money(outflow)})",
            "", "**By account (net movement in period)**"]
    out += [f"- {a}: {money(v)} {cur}" for a, v in sorted(accts.items())]
    out += ["", "_A full balance sheet needs opening balances — use the Beancount backend for that._"]
    return "\n".join(out)


def main():
    try:
        import yaml
    except ImportError:
        sys.exit("pyyaml required: pip install pyyaml --break-system-packages")
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--set", required=True, dest="setid")
    ap.add_argument("--period", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--csv", default="")
    a = ap.parse_args()

    cfg = yaml.safe_load(open(a.config))
    cur = (cfg.get("company", {}).get("locality", {}) or {}).get("currency", "USD")
    sets = {s["id"]: s for s in cfg.get("sets_of_books", [])}
    if a.setid not in sets:
        sys.exit(f"set '{a.setid}' not in config")
    s = sets[a.setid]
    start, end = period_bounds(a.period)
    backend = cfg.get("ledger", {}).get("backend", "beancount")
    base = os.path.dirname(os.path.dirname(os.path.abspath(a.config)))  # working folder (config is in .finance-organizer/)

    head = [f"# Financial report - {s.get('label', a.setid)}",
            f"_Period: {a.period} ({start} to {end}) · {cur} · {backend} ledger_", ""]
    body = []
    if backend == "beancount":
        main_path = s.get("ledger_main") or cfg.get("ledger", {}).get("beancount_main")
        if not main_path:
            sys.exit("no beancount ledger_main for this set in config")
        if not os.path.isabs(main_path):
            main_path = os.path.join(base, main_path)
        is_acc, bs_acc, earn = beancount_report(main_path, start, end, cur)
        body += [fmt_is(is_acc, cur), "", fmt_bs(bs_acc, earn, cur)]
    else:
        csv_path = a.csv or os.path.join(base, s.get("folder", ""), "Ledger", f"{a.setid}-ledger.csv")
        if not os.path.exists(csv_path):
            sys.exit(f"simple ledger not found: {csv_path}")
        body.append(simple_report(csv_path, start, end, cur))

    text = "\n".join(head + body) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w") as f:
            f.write(text)
        print("wrote", a.out)
    else:
        print(text)


if __name__ == "__main__":
    main()
