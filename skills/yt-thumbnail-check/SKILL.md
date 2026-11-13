---
name: yt-thumbnail-check
description: Pitch YouTube thumbnail concepts and check them the way viewers see them, tiny on a phone next to other videos, then pick an A/B pair. Use when making or choosing a thumbnail, when someone asks whether a thumbnail works, or before uploading a video.
---

# Thumbnail check

Most views come from a phone feed where a thumbnail is about 170 pixels wide. If it doesn't read there, it doesn't work.

## Steps
1. **Pitch three different concepts,** not three versions of one. Each one gets:
   - **One idea:** what the viewer gets, in a single picture.
   - **Text:** three words at most, big and heavy, never repeating the title word for word.
   - **The person:** a face with a clear expression, if the creator is on camera. When generating with an image model, pass a real frame of the creator as the reference, and describe their features so identity holds.
   - **High contrast** between subject, text and background.
2. **Generate or design them** at 16:9 (1280×720 or larger).
3. **Run the phone-size check:**
   ```bash
   python scripts/phone_check.py thumb-a.png thumb-b.png thumb-c.png --out phone-check.png
   ```
   This makes one strip at feed size (246×138), a smaller row at 168×94, and a grey dummy beside each so you judge it among neighbours. Open `phone-check.png` and look at it.
4. **Judge each one at that size.** Can you read the text? Can you tell what it's about in one second? Does the face or subject still register? Is anything muddy or busy? Cut any that fail. Say exactly why, for example "the dark half turns to mud."
5. **Keep two for YouTube's thumbnail test** (Test & Compare in YouTube Studio), and say which one you'd lead with.

## Rules
- Don't use other brands' logos, or faces of people who didn't consent.
- If an image model misspells the text, regenerate or fix it. Never ship a typo.
