---
name: yt-teardown
description: Tear down the YouTube videos that already rank for a topic to find the gap a new video can fill. Use after picking a topic, before planning or scripting, or when someone asks what competing videos cover, how long they are, or how to beat them. Reads views, length, chapters and descriptions through the YouTube Data API.
---

# YouTube teardown

Before planning a video, find out what the ranking videos already cover, and what none of them show.

## What you need
- `YOUTUBE_API_KEY` in the environment. It's the same free key the yt-topic-research skill uses: about 101 quota units per search phrase, and 1 per batch of video IDs.
- Python 3.9+ (standard library only).

## Steps
1. **Pull the top videos** for the main search phrase, or pass video IDs or URLs you already have:
   ```bash
   python scripts/teardown.py search "how to use claude for youtube" --top 10
   python scripts/teardown.py ids dQw4w9WgXcQ https://youtu.be/abc123
   ```
   For each video it prints the title, channel, views, length and upload date, plus the chapters parsed from the description and the description's first lines.
2. **For each video, note:**
   - its angle: tutorial, challenge, list or comparison
   - what it actually shows, and what is only talked about
   - sponsors in the description
   - its length
3. **Write the gap** in one or two sentences: the thing searchers want that no top video delivers. For example: "no one shows Claude producing the whole video; most only generate text."
4. **Name the bar to beat:** the typical length, which chapters every top video has, and the angle to avoid copying.

## Rules
- Quote chapter titles and numbers exactly as the API returns them. Don't guess at content you didn't read.
- When showing competitor videos on screen, blur their titles, thumbnails and channel names unless you have a reason to name them.
- If a video has no chapters, say so. Don't invent them from the title.
