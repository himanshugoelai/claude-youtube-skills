---
name: yt-topic-research
description: Find YouTube video topics that a small channel can rank for in search, using evidence instead of brainstorming. Use when someone asks what video to make next, which topics get YouTube search traffic, or how much demand a topic has. Pulls YouTube search suggestions and the views and upload dates of the videos ranking for each phrase, then ranks topics.
---

# YouTube topic research

Pick topics from search data, not ideas. The question to answer is: **what do people type into YouTube, and can a channel this size rank for it?**

## What you need
- A YouTube Data API v3 key in the environment as `YOUTUBE_API_KEY`. It's free: Google Cloud Console → create a project → enable "YouTube Data API v3" → Credentials → API key.
- Quota: 10,000 units a day. Each search costs about 101 units, and `--fresh` doubles that. So budget about 40 to 90 phrases a day.
- Python 3.9+ (standard library only).

## Steps
1. **Learn the channel.** Ask for the channel handle, or read it from context: its size, its niche, and what it already posts. Small channels need searches where the top results are recent or come from small creators.
2. **List seed phrases.** Write 10 to 30 short phrases a viewer might type, for example "how to use claude", "ai ads", "claude code video". Include "how to …" and tool-plus-task forms.
3. **Expand with YouTube's own suggestions.**
   ```bash
   python scripts/research.py suggest "how to use claude" "claude code" "ai ads"
   ```
   This prints the autocomplete phrases. They're what people actually type, so keep the specific, task-shaped ones.
4. **Measure what ranks.**
   ```bash
   python scripts/research.py rank --fresh "how to use claude for youtube" "claude motion graphics"
   ```
   For each phrase, the script reports:
   - the median and max views of the top 12 long-form results (3 min or longer)
   - how many of them were uploaded in the last 90 days
   - with `--fresh`, the same numbers for this month's uploads
   
   Add `--json out.json` to keep the raw rows.
5. **Read the evidence.**
   - **Demand is live** when recent uploads, and especially small channels, pull big views.
   - **Rankable** means the top results are old, weak or off-target. A thin set of exact matches is an opening.
   - **Skip** phrases where years-old million-view videos hold every slot, and phrases where this month's uploads get almost nothing.
6. **Report a ranked shortlist.** Give each topic a working title with the search phrase first, the phrases it targets, and one line of evidence (numbers plus dates). Also list what you skipped and why. Date the research, because the numbers go stale.

## Rules
- Never invent numbers. If a call fails or the quota runs out, say so and show what you have.
- View counts include browse and suggested traffic, so treat them as a demand signal, not a search count.
- `suggest` uses Google's public autocomplete endpoint, which isn't part of the official API. Everything else goes through the official Data API.
