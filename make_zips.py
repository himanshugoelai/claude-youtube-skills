"""Build one upload-ready zip per skill into dist/ (for the Claude app's skill upload): python make_zips.py"""
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
for skill in sorted((ROOT / "skills").iterdir()):
    if not (skill / "SKILL.md").exists():
        continue
    out = DIST / f"{skill.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(skill.parent).as_posix())
    print(out.relative_to(ROOT))
