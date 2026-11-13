"""Render thumbnails at phone-feed size so you can judge them like a viewer.

  python phone_check.py A.png B.png [C.png ...] [--out phone-check.png]

Top row: 246x138 (a large phone feed). Bottom row: 168x94 (compact feed / search results).
Each thumbnail sits next to a grey dummy video so it is judged among neighbours. Needs Pillow (pip install pillow).
"""
import argparse
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is required: pip install pillow")

PAD, GAP = 24, 18


def tile(img, w, h):
    t = img.convert("RGB").copy()
    t.thumbnail((w * 4, h * 4))
    return t.resize((w, h), Image.LANCZOS)


def dummy(w, h):
    d = Image.new("RGB", (w, h), (226, 222, 214))
    ImageDraw.Draw(d).rectangle([w * 0.1, h * 0.7, w * 0.6, h * 0.8], fill=(200, 196, 188))
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", default="phone-check.png")
    a = ap.parse_args()
    imgs = [Image.open(p) for p in a.images]
    rows = [(246, 138), (168, 94)]
    width = PAD * 2 + max(len(imgs) * (w + GAP) + w for w, _ in rows)
    height = PAD * 2 + sum(h + 40 for _, h in rows)
    sheet = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    y = PAD
    for w, h in rows:
        x = PAD
        draw.text((x, y), f"{w}x{h}", fill=(120, 120, 120))
        y += 16
        for i, im in enumerate(imgs):
            sheet.paste(tile(im, w, h), (x, y))
            draw.text((x + 4, y + h + 4), chr(65 + i), fill=(60, 60, 60))
            x += w + GAP
        sheet.paste(dummy(w, h), (x, y))
        y += h + 24
    sheet.save(a.out)
    print(f"wrote {a.out} ({len(imgs)} thumbnails) - open it and judge each at this size")


if __name__ == "__main__":
    main()
