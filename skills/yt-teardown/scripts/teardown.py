"""Tear down ranking YouTube videos: views, length, chapters, description (official YouTube Data API v3).

  python teardown.py search "PHRASE" [--top 10] [--json out.json]
  python teardown.py ids VIDEO_ID_OR_URL [...] [--json out.json]

Needs YOUTUBE_API_KEY. Standard library only.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3"
UA = {"User-Agent": "yt-teardown/1.0"}
TS = re.compile(r"^\s*[\(\[]?((?:\d{1,2}:)?\d{1,2}:\d{2})[\)\]]?\s*[-–—:|·]?\s*(.+?)\s*$")


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def to_id(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", s)
    return m.group(1) if m else s.strip()


def secs(ts):
    p = [int(x) for x in ts.split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))


def chapters(description):
    """YouTube-style chapters: lines starting with a timestamp; valid only if the first is 0:00."""
    out = []
    for line in (description or "").splitlines():
        m = TS.match(line)
        if m:
            out.append((secs(m.group(1)), m.group(2)))
    if not out or out[0][0] != 0:
        return []
    return out


def iso_minutes(d):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0.0
    days, h, mi, s = (int(x or 0) for x in m.groups())
    return days * 1440 + h * 60 + mi + s / 60


def search_ids(key, q, n):
    p = {"part": "id", "q": q, "type": "video", "maxResults": min(50, n * 2), "order": "relevance", "key": key}
    data = get_json(f"{API}/search?" + urllib.parse.urlencode(p))
    return [it["id"]["videoId"] for it in data.get("items", []) if it.get("id", {}).get("videoId")]


def details(key, ids):
    rows = []
    for i in range(0, len(ids), 50):
        p = {"part": "snippet,statistics,contentDetails", "id": ",".join(ids[i:i + 50]), "key": key}
        rows += get_json(f"{API}/videos?" + urllib.parse.urlencode(p)).get("items", [])
    order = {v: k for k, v in enumerate(ids)}
    return sorted(rows, key=lambda it: order.get(it["id"], 999))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("phrase")
    s.add_argument("--top", type=int, default=10)
    s.add_argument("--json")
    i = sub.add_parser("ids")
    i.add_argument("ids", nargs="+")
    i.add_argument("--json")
    a = ap.parse_args()
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("Set YOUTUBE_API_KEY first (free key: Google Cloud Console > YouTube Data API v3 > Credentials).")
    try:
        ids = search_ids(key, a.phrase, a.top) if a.cmd == "search" else [to_id(x) for x in a.ids]
        items = details(key, ids)
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode('utf-8', errors='replace')[:300]}")
    if a.cmd == "search":
        items = [it for it in items if iso_minutes(it["contentDetails"]["duration"]) >= 3][: a.top]
    out = []
    for it in items:
        sn, st = it["snippet"], it.get("statistics", {})
        mins = iso_minutes(it["contentDetails"]["duration"])
        ch = chapters(sn.get("description", ""))
        row = {"id": it["id"], "title": sn["title"], "channel": sn["channelTitle"], "published": sn["publishedAt"][:10],
               "views": int(st.get("viewCount", 0)), "minutes": round(mins, 1), "chapters": ch,
               "description_head": "\n".join(sn.get("description", "").splitlines()[:6])}
        out.append(row)
        print(f"\n## {row['title']}\n{row['channel']} · {row['views']:,} views · {int(mins)}:{int(mins % 1 * 60):02d} · {row['published']} · https://youtu.be/{row['id']}")
        if ch:
            print("chapters: " + " | ".join(f"{t // 60}:{t % 60:02d} {name}" for t, name in ch))
        else:
            print("chapters: (none)")
        print("description: " + row["description_head"].replace("\n", " / ")[:400])
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
