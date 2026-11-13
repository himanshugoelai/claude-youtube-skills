# Claude skills for YouTube

These are five Claude skills built from the workflow I used to make a whole YouTube video with Claude: topic, script, voice, edit, thumbnail and upload.

| Skill | What Claude does with it |
|---|---|
| [`yt-topic-research`](skills/yt-topic-research/SKILL.md) | Finds topics a small channel can rank for. It pulls YouTube's search suggestions plus the views and upload dates of the videos ranking for each phrase, then ranks the topics on that evidence instead of brainstorming. |
| [`yt-teardown`](skills/yt-teardown/SKILL.md) | Reads the chapters, length and views of the top videos for a topic and finds the gap your video can fill. |
| [`yt-script`](skills/yt-script/SKILL.md) | Writes a script that's timed to your speaking pace, with the pace measured from a real recording, and written to be spoken: a hook in the first 15 s and a payoff in every chapter. |
| [`yt-thumbnail-check`](skills/yt-thumbnail-check/SKILL.md) | Pitches three thumbnail concepts and checks them at phone-feed size. Anything you can't read gets cut, and two go to YouTube's A/B test. |
| [`yt-upload-kit`](skills/yt-upload-kit/SKILL.md) | Writes titles with the searched phrase first, the description, chapters (checked against YouTube's rules), tags, a pinned comment and the upload checklist. |

## Install

**Claude Code** (CLI, IDE, or the desktop app's Code tab): copy the skill folders into your skills directory.
```bash
git clone https://github.com/himanshugoelai/claude-youtube-skills
cp -r claude-youtube-skills/skills/* ~/.claude/skills/        # all your projects
# or: cp -r claude-youtube-skills/skills/* .claude/skills/    # just this project
```

**Claude app** (claude.ai and desktop chat): download a zip from [`dist/`](dist/). Then go to Settings → Capabilities, make sure code execution is on, and upload the zip under Skills. Do this once per skill.

Then just ask, for example: *"Use yt-topic-research to find five video topics for my channel @yourhandle."*

## What you need
- **A YouTube Data API key** for research and teardown. It's free: Google Cloud Console → enable *YouTube Data API v3* → Credentials → API key. Set it as `YOUTUBE_API_KEY`. The free quota is 10,000 units a day, and one search costs about 100.
- **Python 3.9+.** The research, teardown, chapters and pace scripts use only the standard library. The thumbnail check needs Pillow (`pip install pillow`), and `pace.py measure` needs `ffprobe` (part of ffmpeg).

The search-suggestion step uses Google's public autocomplete endpoint, which isn't part of the official API. Everything else goes through the official YouTube Data API. Nothing scrapes YouTube pages.

## Tests
```bash
python -m unittest discover tests
```

## License
MIT
