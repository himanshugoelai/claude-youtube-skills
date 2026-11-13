"""Offline tests for the skill scripts (no API key needed): python -m unittest discover tests"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent / "skills"


def load(rel):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_"), ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


research = load("yt-topic-research/scripts/research.py")
teardown = load("yt-teardown/scripts/teardown.py")
chapters = load("yt-upload-kit/scripts/chapters.py")
pace = load("yt-script/scripts/pace.py")


class Research(unittest.TestCase):
    def test_iso_minutes(self):
        self.assertAlmostEqual(research.iso_minutes("PT12M46S"), 12 + 46 / 60)
        self.assertAlmostEqual(research.iso_minutes("PT1H0M5S"), 60 + 5 / 60)
        self.assertEqual(research.iso_minutes("P0D"), 0)

    def test_summarize_filters_shorts_and_takes_median(self):
        rows = [{"views": v, "minutes": m, "published": "2026-11-01T00:00:00Z"} for v, m in
                [(100, 0.5), (1000, 10), (3000, 12), (2000, 8), (5, 2.0)]]
        s = research.summarize(rows)
        self.assertEqual(s["n"], 3)
        self.assertEqual(s["median_views"], 2000)
        self.assertEqual(s["max_views"], 3000)


class Teardown(unittest.TestCase):
    def test_chapters_from_description(self):
        desc = "Great video\n\nTIMESTAMPS:\n0:00 Intro\n0:40 Interface\n4:38 Skills\n11:39 Thumbnail Ideator Skill"
        self.assertEqual(teardown.chapters(desc), [(0, "Intro"), (40, "Interface"), (278, "Skills"), (699, "Thumbnail Ideator Skill")])

    def test_no_chapters_unless_zero_first(self):
        self.assertEqual(teardown.chapters("1:00 Not a chapter list"), [])

    def test_to_id(self):
        self.assertEqual(teardown.to_id("https://www.youtube.com/watch?v=abcdefghijk&t=3"), "abcdefghijk")
        self.assertEqual(teardown.to_id("https://youtu.be/abcdefghijk"), "abcdefghijk")


class Chapters(unittest.TestCase):
    def test_valid(self):
        rows, problems = chapters.check(["0:00 Intro", "0:30 Setup", "1:05 Find a topic"], length=120)
        self.assertEqual(problems, [])

    def test_rules(self):
        _, problems = chapters.check(["0:05 Intro", "0:10 Too short"])
        self.assertTrue(any("0:00" in p for p in problems))
        self.assertTrue(any("at least 3" in p for p in problems))


class Pace(unittest.TestCase):
    def test_table_rows_and_notes(self):
        text = "| a_open | visual | Hello there, world. |\n| v_x | visual | Two words [VERIFY: later] |\n| — | x | — |"
        lines = pace.spoken_lines(text)
        self.assertEqual(len(lines), 2)
        self.assertEqual(sum(pace.count_words(l) for l in lines), 5)


if __name__ == "__main__":
    unittest.main()
