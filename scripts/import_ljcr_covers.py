#!/usr/bin/env python3
"""Import La Jolla Covering Repository covers into the local cache.

Default ranges match the assignment rather than the whole repository:
v/n = 7..25, k = 4..7, t = 3..7.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager


BASE_URL = "https://ljcr.dmgordon.org/cover/show_cover.php?v={v}&k={k}&t={t}"


def fetch_cover(v: int, k: int, t: int) -> dict | None:
    url = BASE_URL.format(v=v, k=k, t=t)
    with urllib.request.urlopen(url, timeout=30) as response:
        text = response.read().decode("utf-8", errors="replace")

    title_match = re.search(r"<h1[^>]*>\s*(.*?)\s*</h1>", text, re.IGNORECASE | re.DOTALL)
    if not title_match:
        title_match = re.search(r"#\s*(.+)", text)
    if not title_match:
        return None

    title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1))).strip()
    exact_match = re.search(r"C\(\d+,\d+,\d+\)\s*=\s*(\d+)", title)
    range_match = re.search(r"(\d+)\s*[≤<=]+\s*C\(\d+,\d+,\d+\)\s*[≤<=]+\s*(\d+)", title)

    if exact_match:
        lower_bound = upper_bound = int(exact_match.group(1))
    elif range_match:
        lower_bound = int(range_match.group(1))
        upper_bound = int(range_match.group(2))
    else:
        return None

    method_match = re.search(r"Method of Construction:\s*([^<\n]+)", text)
    method = html.unescape(method_match.group(1)).strip() if method_match else None

    blocks = []
    pre_match = re.search(r"<pre[^>]*>(.*?)</pre>", text, re.IGNORECASE | re.DOTALL)
    block_text = pre_match.group(1) if pre_match else re.sub(r"<[^>]+>", "", text)
    for line in block_text.splitlines():
        numbers = [int(value) for value in re.findall(r"\d+", line)]
        if len(numbers) == k and all(1 <= value <= v for value in numbers):
            blocks.append(tuple(numbers))

    if not blocks:
        return None

    return {
        "v": v,
        "k": k,
        "t": t,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "is_proven_optimal": lower_bound == upper_bound == len(blocks),
        "blocks": blocks,
        "source_url": url,
        "construction_method": method,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Import La Jolla covering designs.")
    parser.add_argument("--min-v", type=int, default=7)
    parser.add_argument("--max-v", type=int, default=25)
    parser.add_argument("--min-k", type=int, default=4)
    parser.add_argument("--max-k", type=int, default=7)
    parser.add_argument("--min-t", type=int, default=3)
    parser.add_argument("--max-t", type=int, default=7)
    parser.add_argument("--db-folder", default=None)
    args = parser.parse_args()

    db = DatabaseManager(db_folder=args.db_folder)
    imported = 0
    skipped = 0

    for v in range(args.min_v, args.max_v + 1):
        for k in range(args.min_k, min(args.max_k, v - 1) + 1):
            for t in range(args.min_t, min(args.max_t, k - 1) + 1):
                try:
                    cover = fetch_cover(v, k, t)
                except Exception as exc:
                    skipped += 1
                    print(f"skip C({v},{k},{t}): {exc}")
                    continue

                if not cover:
                    skipped += 1
                    print(f"skip C({v},{k},{t}): no cover data")
                    continue

                db.save_standard_cover(
                    cover["v"], cover["k"], cover["t"],
                    cover["lower_bound"], cover["upper_bound"],
                    cover["blocks"], cover["is_proven_optimal"],
                    cover["source_url"],
                    source_updated_at=None,
                    construction_method=cover["construction_method"],
                )
                imported += 1
                print(
                    f"imported C({v},{k},{t}) upper={cover['upper_bound']} "
                    f"blocks={len(cover['blocks'])} exact={cover['is_proven_optimal']}"
                )

    print(f"done: imported={imported}, skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
