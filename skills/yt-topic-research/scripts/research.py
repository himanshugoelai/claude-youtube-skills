"""YouTube topic research: search suggestions + what ranks, via the official YouTube Data API v3.

  python research.py suggest PHRASE [PHRASE ...]
  python research.py rank [--fresh] [--json out.json] PHRASE [PHRASE ...]

`rank` needs YOUTUBE_API_KEY in the environment (free; ~101 quota units per phrase, ~202 with --fresh).
Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import statistics
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3"
UA = {"User-Agent": "yt-topic-research/1.0"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def suggest(phrase):
    """YouTube autocomplete phrases (Google's public suggest endpoint, not part of the Data API)."""
    url = "https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=en&q=" + urllib.parse.quote(phrase)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        text = r.read().decode("utf-8", errors="replace")
    m = re.search(r"\((.*)\)\s*$", text, re.S)
    if not m:
        return []
    try:
        return [s[0] for s in json.loads(m.group(1))[1]]
    except (ValueError, IndexError, TypeError):
        return []


def iso_minutes(d):
    """ISO 8601 duration (PT1H2M3S) -> minutes."""
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0.0
    days, h, mi, s = (int(x or 0) for x in m.groups())
    return days * 1440 + h * 60 + mi + s / 60


def age_days(published, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    t = dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
    return (now - t).days


def search_ids(key, q, published_after=None, n=25):
    p = {"part": "id", "q": q, "type": "video", "maxResults": n, "order": "relevance", "key": key}
    if published_after:
        p["publishedAfter"] = published_after
    data = get_json(f"{API}/search?" + urllib.parse.urlencode(p))
    return [it["id"]["videoId"] for it in data.get("items", []) if it.get("id", {}).get("videoId")]


def video_rows(key, ids):
    if not ids:
        return []
    p = {"part": "snippet,statistics,contentDetails", "id": ",".join(ids), "key": key}
    data = get_json(f"{API}/videos?" + urllib.parse.urlencode(p))
    by_id = {it["id"]: it for it in data.get("items", [])}
    rows = []
    for vid in ids:  # keep search (relevance) order
        it = by_id.get(vid)
        if not it:
            continue
        rows.append({
            "id": vid,
            "title": it["snippet"]["title"],
            "channel": it["snippet"]["channelTitle"],
            "published": it["snippet"]["publishedAt"],
            "views": int(it.get("statistics", {}).get("viewCount", 0)),
            "minutes": round(iso_minutes(it["contentDetails"]["duration"]), 1),
        })
    return rows


def summarize(rows, top=12, min_minutes=3.0):
    long = [r for r in rows if r["minutes"] >= min_minutes][:top]
    views = [r["views"] for r in long]
    return {
        "n": len(long),
        "median_views": int(statistics.median(views)) if views else 0,
        "max_views": max(views) if views else 0,
        "recent_90d": sum(1 for r in long if age_days(r["published"]) <= 90),
        "top": long,
    }


def fmt(n):
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}K" if n >= 1e3 else str(n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("suggest")
    s.add_argument("phrases", nargs="+")
    r = sub.add_parser("rank")
    r.add_argument("phrases", nargs="+")
    r.add_argument("--fresh", action="store_true", help="also measure uploads from the last 30 days")
    r.add_argument("--json", help="write raw rows to this file")
    a = ap.parse_args()

    if a.cmd == "suggest":
        for p in a.phrases:
            print(f"\n{p}\n  " + "\n  ".join(suggest(p) or ["(no suggestions)"]))
        return

    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("Set YOUTUBE_API_KEY first (free key: Google Cloud Console > YouTube Data API v3 > Credentials).")
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = {"date": dt.date.today().isoformat(), "phrases": {}}
    print(f"YouTube search, {out['date']} (top 12 long-form results, 3 min+)\n")
    print(f"{'phrase':44} {'median':>8} {'max':>8} {'<=90d':>6}" + (f" {'month med':>10}" if a.fresh else ""))
    for p in a.phrases:
        try:
            res = summarize(video_rows(key, search_ids(key, p)))
            line = f"{p[:44]:44} {fmt(res['median_views']):>8} {fmt(res['max_views']):>8} {res['recent_90d']:>3}/{res['n']:<2}"
            if a.fresh:
                fresh = summarize(video_rows(key, search_ids(key, p, published_after=since)))
                res["this_month"] = fresh
                line += f" {fmt(fresh['median_views']):>10}"
            out["phrases"][p] = res
            print(line)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            print(f"{p[:44]:44}  API error {e.code}: {body}")
            if e.code == 403:
                print("Quota exhausted or key not allowed; stopping. Report what you have.")
                break
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
        print(f"\nraw rows -> {a.json}")


if __name__ == "__main__":
    main()
