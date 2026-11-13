---
name: yt-script
description: Write a YouTube video script that is timed to the length the creator wants and written to be spoken aloud, with a hook in the first 15 seconds and a payoff in every chapter. Use when turning a plan, outline or topic into a voiceover or talking-head script, when a script runs too long or too short, or when timing a script to a voice clone or a creator's speaking pace.
---

# YouTube script

Turn a plan into a script that sounds like the creator, fits the target length, and keeps people watching.

## Inputs to ask for, or find in context
- The plan or outline: chapters, plus the search phrase each chapter serves.
- The target length as a range, for example 5 to 10 minutes.
- The voice:
  - Best is a recording of the creator or their voice clone; use it to measure pace.
  - If there's no recording, use 150 words a minute and say it's an estimate.
- If possible, one old script or transcript of theirs, so you learn how they talk.

## Measure the pace
```bash
python scripts/pace.py measure voice1.mp3 voice2.mp3 --words 911       # words a minute from real audio
python scripts/pace.py fit script.md --wpm 166                         # how long a script will run
```
`measure` adds up the audio length; pass the word count of those recordings with `--words`. `fit` counts the spoken words in a script (table rows or plain lines) and gives the minutes at that pace.

## Write it
1. **Hook in the first 15 seconds.** Show or say the payoff, and why it's believable. Don't open with a greeting.
2. **One idea per line, short sentences.** Write for the ear: if a line is hard to say out loud, it will sound robotic, cloned voice or not.
3. **A payoff in every chapter:** something the viewer can copy, see or use.
4. **Spell out numbers and versions** for voice tools: "two point six", "a hundred and sixty-six". Keep digits for on-screen text.
5. **Table format.** Use one row per line, with an ID, what's on screen, and the spoken text. Lines spoken on camera get an `a_` prefix, and voiceover gets `v_`.
6. **Time it** with `pace.py fit`, then cut or add to land inside the range. Report the words, the minutes of speech, and the expected cut length; holds and title cards usually add 10 to 20 percent.

## Honesty rules
- Every claim about what happened ("I asked…", "Claude did…") must match what actually happened. Check against the real conversation before recording. If it differs, rewrite the line.
- Mark lines that describe something that hasn't happened yet with `[VERIFY]`, and fill them in after the run.
- Disclose AI voices, AI avatars and sponsorships or employers on screen and in the description.
- Nothing gets recorded until the creator approves the script.
