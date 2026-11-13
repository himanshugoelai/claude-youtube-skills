"""Check YouTube chapters before you paste them into a description.

  python chapters.py chapters.txt [--length 6:08]

chapters.txt: one chapter per line, "M:SS Title" or "H:MM:SS Title".
YouTube only shows chapters when: the first is 0:00, there are at least 3, each is at least 10 seconds,
and they are in ascending order. --length (the video's duration) also checks the last chapter.
"""
import argparse
import re
import sys

LINE = re.compile(r"^\s*((?:\d{1,2}:)?\d{1,2}:\d{2})\s+(.+?)\s*$")


def secs(ts):
    p = [int(x) for x in ts.split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(p)))


def check(lines, length=None):
    rows, problems = [], []
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        m = LINE.match(line)
        if not m:
            problems.append(f"line {n}: not 'M:SS Title' -> {line.strip()!r}")
            continue
        rows.append((secs(m.group(1)), m.group(2), m.group(1)))
    if not rows:
        return rows, problems + ["no chapters found"]
    if rows[0][0] != 0:
        problems.append(f"first chapter must start at 0:00 (got {rows[0][2]})")
    if len(rows) < 3:
        problems.append(f"need at least 3 chapters (got {len(rows)})")
    ends = [r[0] for r in rows[1:]] + ([length] if length else [])
    for (t, title, ts), end in zip(rows, ends):
        if end <= t:
            problems.append(f"{ts} {title}: not in ascending order")
        elif end - t < 10:
            problems.append(f"{ts} {title}: only {end - t} s long (minimum 10 s)")
    return rows, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--length", help="video length, e.g. 6:08")
    a = ap.parse_args()
    rows, problems = check(open(a.file, encoding="utf-8").read().splitlines(), secs(a.length) if a.length else None)
    for t, title, ts in rows:
        print(f"{ts:>8}  {title}")
    if problems:
        print("\nPROBLEMS:\n- " + "\n- ".join(problems))
        sys.exit(1)
    print(f"\nOK: {len(rows)} chapters, YouTube will show them.")


if __name__ == "__main__":
    main()
