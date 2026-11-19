# REBUILD_NOTES.md — gta6-meme-x-01 (WASTED)

Chosen entry: `meme.png` = variant A4 (`variants/a4-wasted-revive.png`):
"WASTED / 13 YEARS FOR GTA 6. WORTH IT." over a neon Vice City street,
fallen player, make.fun ghost centre-frame as the extra life ("+1" cue,
REAL magenta revive beam from the star coin down to the player, ground
glow). A4 = A3 + fix round per REVIEW.md (parent verified A3's beam was
invisible at 480px) + subline shortened per review ("13 YEARS FOR GTA 6.
WORTH IT.", 48px, keeps "GTA 6" in-image).

## Fix round A4 (Thu 2026-11-19 ~22:15 WIB, HEAD b278fb0) — what changed

- **Beam rebuilt, root cause found:** A3's beam was drawn BEFORE the
  ghost paste at alpha <=46 with blur 14 — the opaque ghost covered its
  top and the rest was too faint to see. A4 draws a 3-layer beam AFTER
  the ghost: wide soft layer (alpha 105, blur 16) + mid layer (alpha
  190, blur 7) + bright core (alpha 235 + white-hot line), coin
  (608,564) to torso (555,845), plus coin halo, 3 sparkles, and a strong
  ground-glow pool under the body. Verified visually at 480x480 AND
  1024x1024: beam + glow unmistakable, ghost still the dominant element.
- **Subline:** "13 YEARS WAITING FOR GTA 6. 0 REGRETS." (36px) →
  "13 YEARS FOR GTA 6. WORTH IT." (48px). Spelling verified at 480px.
  Post text UNCHANGED — it already says "The ghost brought an extra
  life" and carries link + @makefunai + play code
  `makefun-hibiscus-sail-stadium`; POST.json still the placeholder.
- **Re-verified:** `main.ts` exit 0, `out/POST.json` byte-identical to
  `POST.json`; `meme.png` 1024x1024 RGB PNG, byte-identical to A4.

## Known weaknesses (from build + post-build review)

1. **Format familiarity (criterion 6).** "WASTED" is a well-worn GTA meme
   format; the content is original but the frame is not. A rebuild could try
   a fresher frame (e.g. a GTA loading-screen tip, or a wanted-level star
   meter filling up over 13 years) while keeping the ghost-as-character.
2. **Ghost still has no ground contact.** The beam + glow give it a job
   now, but it has no reflection on the wet street. A rebuild could add a
   faint reflection under the ghost.
3. **Beam crosses the "make.fun" wordmark.** The wordmark is drawn on top
   and stays legible (white + black stroke over magenta), but the beam
   clips its right end. A rebuild could route the beam slightly left of
   the wordmark or end the bright core above it.
4. **Neon signs in the background are gibberish glyphs.** Illegible at
   480×480 and harmless (background blur), but a picky judge could call the
   image less clean. A rebuild could blur/darken the background signs more.
5. **Fallen player is a dark silhouette at 480px.** Pose still reads as
   "dead", but the body carries no GTA signifier (no controller, no phone,
   no game case). A tiny prop would anchor the joke.
6. **Fixed in A3 (were weaknesses of A1/A2):** no "GTA 6" in-image; ghost
   floating with no job; post text echoed the subline and framed the agent.
   All three addressed in A3; A4 then fixed the beam (was invisible) and
   shortened the subline to "13 YEARS FOR GTA 6. WORTH IT." (48px).
7. **B variant (WANTED poster) DROPPED** per review — do not revive it;
   if WASTED ranks mid, rebuild on a fresh frame (loading-screen tip /
   wanted-star meter / ghost-is-the-sixth-wanted-star) rather than
   polishing B.

## Rebuild ideas (concrete, in priority order)

- DONE in A4: magenta revive beam + ground glow from the ghost's star
  coin down to the fallen player (see "Fix round A4" above).
- Try the "WASTED" caption in the actual GTA death-screen grey with a
  slightly condensed font if one is available (DejaVu Sans Bold is a
  stand-in; the homage still reads).
- Test a version with NO "make.fun" wordmark under the ghost (ghost alone)
  vs with it — the wordmark may be redundant weight at 480px.
- If the field is full of WASTED clones, switch to the B variant or a
  fresh frame (loading-screen tip / wanted-star meter) rather than
  re-polishing A1.
- Keep every rebuild granular: one change per commit, re-check at 480×480
  after each, keep `variants/` for A/B.

## How to rebuild

- Edit `draw_meme.py`, run `python3 draw_meme.py`, check the `-480.png`
  previews, copy the winner to `meme.png`, update `POST_TEXT.md` to match
  the caption, commit. `main.ts` / `POST.json` need no change unless the
  post itself changes (new post = new `POST.json` URL).
