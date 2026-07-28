from __future__ import annotations

import csv
import html
import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PROFILE_URL = "https://scholar.google.es/citations?user=IsAjXHwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=100"


def clean(value: str) -> str:
    value = re.sub(r"<.*?>", "", value, flags=re.S)
    value = html.unescape(value)
    return " ".join(value.split())


def fetch_html() -> str:
    request = urllib.request.Request(
        PROFILE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_metrics(page: str) -> dict[str, int | str]:
    description = re.search(r'<meta name="description" content="([^"]+)"', page)
    metrics: dict[str, int | str] = {"source_url": PROFILE_URL}
    if description:
        cited = re.search(r"Cited by\s+(\d+)", html.unescape(description.group(1)))
        if cited:
            metrics["citations_all"] = int(cited.group(1))

    values = re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', page)
    if len(values) >= 3:
        metrics["citations_all"] = int(values[0])
        metrics["h_index_all"] = int(values[2])
    if len(values) >= 5:
        metrics["i10_index_all"] = int(values[4])
    return metrics


def parse_publications(page: str) -> list[dict[str, str | int]]:
    rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, flags=re.S)
    publications: list[dict[str, str | int]] = []

    for row in rows:
        title_match = re.search(r'class="gsc_a_at">(.+?)</a>', row, flags=re.S)
        if not title_match:
            continue

        gray_blocks = re.findall(r'<div class="gs_gray">(.*?)</div>', row, flags=re.S)
        cite_match = re.search(r'class="gsc_a_ac gs_ibl">(\d*)</a>', row)
        year_match = re.search(r'class="gsc_a_h gsc_a_hc gs_ibl">(\d*)</span>', row)
        link_match = re.search(r'href="([^"]+)" class="gsc_a_at"', row)

        title = clean(title_match.group(1))
        journal = clean(gray_blocks[1]) if len(gray_blocks) > 1 else ""
        journal = re.sub(r",\s*\d{4}$", "", journal)

        publications.append(
            {
                "title": title,
                "authors": clean(gray_blocks[0]) if gray_blocks else "",
                "journal": journal,
                "year": int(year_match.group(1)) if year_match and year_match.group(1) else "",
                "citations": int(cite_match.group(1)) if cite_match and cite_match.group(1) else 0,
                "scholar_link": "https://scholar.google.es" + html.unescape(link_match.group(1))
                if link_match
                else "",
                "theme": "",
                "quartile": "",
            }
        )

    return publications


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    page = fetch_html()
    metrics = parse_metrics(page)
    publications = parse_publications(page)

    (DATA_DIR / "scholar_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with (DATA_DIR / "scholar_publications.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["title", "authors", "journal", "year", "citations", "scholar_link", "theme", "quartile"],
        )
        writer.writeheader()
        writer.writerows(publications)

    print(f"Imported {len(publications)} Scholar records")
    print(json.dumps(metrics, ensure_ascii=False))


if __name__ == "__main__":
    main()
