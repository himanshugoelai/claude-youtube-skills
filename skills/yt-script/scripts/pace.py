"""Speaking pace for scripts.

  python pace.py measure AUDIO [AUDIO ...] --words N    words a minute of real recordings (needs ffprobe)
  python pace.py fit SCRIPT.md [--wpm 150]              spoken words + minutes of a script

`fit` reads markdown tables (last column = spoken line; rows whose first cell starts with a_ or v_) or, if there
are none, every non-empty line that is not a heading. Bracketed notes like [VERIFY] are not counted.
"""
import argparse
import re
import subprocess
import sys


def duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except (FileNotFoundError, subprocess.CalledProcessError, ValueError):
        sys.exit(f"could not read {path} (is ffprobe installed?)")


def spoken_lines(text):
    rows = []
    for line in text.splitlines():
        m = re.match(r"\|\s*([a-z]_[\w]+)\s*\|.*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            rows.append(m.group(2))
    if rows:
        return rows
    return [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith(("#", "|", "-", ">"))]


def count_words(s):
    s = re.sub(r"\[[^\]]*\]", "", s)
    return len(re.findall(r"[A-Za-z0-9'’-]+", s))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("audio", nargs="+")
    m.add_argument("--words", type=int, required=True, help="total words spoken in these files")
    f = sub.add_parser("fit")
    f.add_argument("script")
    f.add_argument("--wpm", type=float, default=150.0)
    a = ap.parse_args()
    if a.cmd == "measure":
        secs = sum(duration(p) for p in a.audio)
        print(f"{a.words} words / {secs:.1f} s = {a.words / (secs / 60):.1f} words a minute ({len(a.audio)} files)")
        return
    text = open(a.script, encoding="utf-8").read()
    lines = spoken_lines(text)
    words = sum(count_words(l) for l in lines)
    mins = words / a.wpm
    print(f"{len(lines)} lines, {words} words -> {mins:.2f} min of speech at {a.wpm:g} wpm "
          f"(expect a cut of about {mins * 1.1:.1f}-{mins * 1.2:.1f} min with holds and cards)")


if __name__ == "__main__":
    main()
