#!/usr/bin/env python3
"""Load your extract and print lines, orders and customers. Your analysis goes below.

    python3 analysis.py

Set EXTRACT to the CSV your extract script writes into your group folder
(M1_sheet.pdf, Task 1). It is searched next to this file and in the folders above.
"""
from pathlib import Path

import pandas as pd

# ── set this to YOUR extract file ────────────────────────────────────────────
EXTRACT = "<e.g. extract_S14.csv>"
# ─────────────────────────────────────────────────────────────────────────────


def find_extract():
    """EXTRACT, next to this file or in a folder above it."""
    here = Path(__file__).resolve()
    for base in [here.parent] + list(here.parents):
        c = base / EXTRACT
        if c.exists():
            return c
    raise SystemExit(f"{EXTRACT} not found -- set EXTRACT at the top of this "
                     f"file to the CSV your extract script writes.")


def load():
    d = pd.read_csv(find_extract())
    if d.empty:
        raise SystemExit(f"{EXTRACT} has no rows -- run your extract script first")
    if "OrderDate" in d:
        d["OrderDate"] = pd.to_datetime(d.OrderDate)
    if "SalesOrderDetailID" in d:  # one row per order line, in a fixed order
        d = d.sort_values("SalesOrderDetailID").reset_index(drop=True)
    return d


if __name__ == "__main__":
    d = load()
    for col in ("TerritoryName", "Category"):
        if col in d:
            print(f"  {col}: {', '.join(map(str, d[col].unique()))}")
    print(f"  lines:     {len(d):,}")
    print(f"  orders:    {d.SalesOrderID.nunique():,}")
    print(f"  customers: {d.CustomerID.nunique():,}")
    print("\nCompare with your row of slices.csv, then put the three numbers "
          "into manifest.yaml -> findings.")
    print("The rest of the findings block is yours to compute.")
    # ── your analysis from here ──────────────────────────────────────────────
