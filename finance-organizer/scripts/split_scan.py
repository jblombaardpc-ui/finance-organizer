#!/usr/bin/env python3
"""Split a bulk scan (one PDF holding several documents) into separate PDFs.

Boundary detection stays with the operator (Claude / the human): scanners can't
tell where one document ends and the next begins, but a reader can. So this script
has two modes — first inspect, then cut.

INSPECT (decide the boundaries):
  split_scan.py --file "<inbox.pdf>" --info
    Prints the page count and a one-line text snippet per page so you can see where
    the vendor / date / invoice number changes. Pages with no extractable text are
    flagged [IMAGE-ONLY] — open those visually before deciding.

CUT (write one PDF per document):
  split_scan.py --file "<inbox.pdf>" --ranges "1-2,3,4-6" --out-dir "<dir>"
    Writes one PDF per range: <stem>-part1-p1-2.pdf, <stem>-part2-p3.pdf, ...
  split_scan.py --file "<inbox.pdf>" --each-page --out-dir "<dir>"
    Shortcut: one PDF per page (use when every page is its own document).

The output PDFs are the things you then identify, dedup, name, and file exactly as
if each had arrived in the inbox on its own. The original bulk scan is left in place;
delete it (and log a row) only after every part is filed.

Ranges are 1-based and inclusive. "1-2,3,4-6" => [1,2] [3] [4,5,6]. Pages may not
repeat and must stay within the document; order is preserved as written.
"""
import argparse
import os
import re
import subprocess
import sys

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:  # pragma: no cover - environment guard
    print("ERROR: pypdf is required (pip install pypdf).", file=sys.stderr)
    sys.exit(2)


def page_count(path):
    return len(PdfReader(path).pages)


def page_text(path, page_1based):
    """One-line text snippet for a single page via pdftotext, else pypdf."""
    snippet = ""
    try:
        out = subprocess.run(
            ["pdftotext", "-q", "-f", str(page_1based), "-l", str(page_1based), path, "-"],
            capture_output=True,
        )
        if out.returncode == 0:
            snippet = out.stdout.decode("utf-8", "replace")
    except FileNotFoundError:
        pass
    if not snippet.strip():
        try:
            snippet = PdfReader(path).pages[page_1based - 1].extract_text() or ""
        except Exception:
            snippet = ""
    return re.sub(r"\s+", " ", snippet).strip()


def parse_ranges(spec, n):
    """'1-2,3,4-6' -> [[1,2],[3],[4,5,6]] validated against n pages."""
    groups = []
    seen = set()
    for chunk in (c.strip() for c in spec.split(",") if c.strip()):
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", chunk)
        if not m:
            raise ValueError(f"bad range token: {chunk!r}")
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        if lo < 1 or hi < lo or hi > n:
            raise ValueError(f"range {chunk!r} out of bounds (document has {n} pages)")
        pages = list(range(lo, hi + 1))
        for p in pages:
            if p in seen:
                raise ValueError(f"page {p} appears in more than one range")
            seen.add(p)
        groups.append(pages)
    if not groups:
        raise ValueError("no ranges given")
    return groups


def label(pages):
    return f"p{pages[0]}" if len(pages) == 1 else f"p{pages[0]}-{pages[-1]}"


def write_part(reader, pages, out_path):
    w = PdfWriter()
    for p in pages:
        w.add_page(reader.pages[p - 1])
    with open(out_path, "wb") as f:
        w.write(f)


def main():
    ap = argparse.ArgumentParser(description="Split a bulk scan into separate document PDFs.")
    ap.add_argument("--file", required=True, help="the multi-document PDF in the inbox")
    ap.add_argument("--info", action="store_true", help="inspect: print per-page text snippets")
    ap.add_argument("--ranges", help="cut: comma list of 1-based page ranges, e.g. '1-2,3,4-6'")
    ap.add_argument("--each-page", action="store_true", help="cut: one PDF per page")
    ap.add_argument("--out-dir", help="where to write the parts (default: <file dir>/_split)")
    ap.add_argument("--stem", help="base name for parts (default: original filename without .pdf)")
    ap.add_argument("--snippet-chars", type=int, default=160, help="snippet length in --info")
    a = ap.parse_args()

    if not os.path.exists(a.file):
        print("ERROR: file not found:", a.file, file=sys.stderr)
        sys.exit(2)
    if not a.file.lower().endswith(".pdf"):
        print("ERROR: only PDF bulk scans are supported. Convert images to PDF first.", file=sys.stderr)
        sys.exit(2)

    n = page_count(a.file)
    print("file:", os.path.basename(a.file))
    print("pages:", n)

    if a.info or (not a.ranges and not a.each_page):
        for p in range(1, n + 1):
            txt = page_text(a.file, p)
            if txt:
                print(f"--- page {p} ---  {txt[:a.snippet_chars]}")
            else:
                print(f"--- page {p} ---  [IMAGE-ONLY: no extractable text; inspect visually]")
        print()
        print("NEXT: pages where the vendor / date / invoice number changes start a new")
        print("document. Re-run with --ranges to cut, e.g.:")
        print(f'  split_scan.py --file "{a.file}" --ranges "1-2,3,4-{n}" --out-dir "<dir>"')
        return

    stem = a.stem or os.path.splitext(os.path.basename(a.file))[0]
    out_dir = a.out_dir or os.path.join(os.path.dirname(os.path.abspath(a.file)), "_split")
    os.makedirs(out_dir, exist_ok=True)

    if a.each_page:
        groups = [[p] for p in range(1, n + 1)]
    else:
        try:
            groups = parse_ranges(a.ranges, n)
        except ValueError as e:
            print("ERROR:", e, file=sys.stderr)
            sys.exit(2)

    reader = PdfReader(a.file)
    written = []
    for i, pages in enumerate(groups, 1):
        out_path = os.path.join(out_dir, f"{stem}-part{i}-{label(pages)}.pdf")
        write_part(reader, pages, out_path)
        written.append(out_path)
        print(f"wrote: {out_path}  ({'page ' + str(pages[0]) if len(pages)==1 else 'pages ' + label(pages)[1:]})")

    covered = sorted(p for g in groups for p in g)
    missing = [p for p in range(1, n + 1) if p not in covered]
    print()
    print(f"{len(written)} part(s) written to {out_dir}")
    if missing:
        print(f"NOTE: pages not included in any part: {missing} (intentional? blanks/separators are fine to drop)")
    print("NEXT: identify, dedup, name, and file each part as its own inbox document.")
    print("Then delete the original bulk scan and log a row in the rename ledger.")


if __name__ == "__main__":
    main()
