---
name: yt-upload-kit
description: Write everything needed to upload a YouTube video for search, from the research and the finished edit - title options with the searched phrase first, description, chapters, tags, pinned comment, and the disclosure and end-screen checklist. Use when a video is ready to upload, or when someone asks for a title, description, chapters or tags.
---

# Upload kit

Package a finished video so it gets found for the searches it was made for.

## Inputs
- The research: the target search phrases and their evidence, for example from yt-topic-research.
- The final cut's chapter times. Take them from the edit's timeline, not the script.
- The script, so you can describe what's in the video and pull quotable lines.
- Links: the creator's resources, the skill pack or download, and their socials.

## Write
1. **Titles.** Give three options, each 70 characters or fewer, with the exact searched phrase first. For example: "How to Use Claude for YouTube (I Made This Entire Video With It)". Promise only what the video shows.
2. **Description:**
   - The first two lines carry the hook and the main search phrase in plain words; they show above the fold.
   - Then the links: the main call to action first.
   - Then the chapters.
   - Then any disclosures: AI voice or avatar, sponsors, the creator's employer if a product they work on appears.
   - Then two or three more phrasings of the topic, written as sentences, not a keyword dump.
3. **Chapters.** Check them with `python scripts/chapters.py chapters.txt`. YouTube shows chapters only when the first is 0:00, there are at least three, and each is 10 seconds or longer. Name chapters after what people search for.
4. **Tags:** 10 to 15 search phrases, about 500 characters at most. Start with the target phrases, then their variants.
5. **Pinned comment:** one question the viewer can answer in a word or two, plus the main link.
6. **Checklist for the uploader:**
   - Tick "Altered or synthetic content" if the video has a realistic AI voice, face or scene.
   - Set the thumbnail pair in Test & Compare.
   - Set the end screen to what the creator wants: subscribe, a playlist, or none.
   - Add a playlist.
   - Make sure the links work.

## Rules
- No clickbait the video doesn't pay off, and no false urgency.
- Every number you quote must come from the research or the video itself.
- Output one paste-ready markdown file, `UPLOAD-KIT.md`, with a section per field.
