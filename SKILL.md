---
name: reaction-sticker-pack
description: Source real static internet reaction cutouts and turn them into numbered TikTok-style PNG sticker packs with transparent backgrounds, smooth white die-cut outlines, previews, provenance, and downloadable ZIPs. Use when asked to create, expand, modernize, process, or package reaction stickers or meme stickers.
---

# Reaction Sticker Pack

Produce packs matching the approved reaction sticker look: one expressive cutout per PNG, transparent canvas, and a smooth medium white border. The subject comes from a real sourced image; editing only prepares the sticker.

## Inputs

Infer these from context: requested count, numbering start, classic or modern mix, existing pack folder, and delivery location. Ask only when a missing choice materially changes the result.

## Workflow

1. Use the agent's image editing tool. In Codex, load the built-in `imagegen` skill. In Claude, use its configured image editing tool. Confirm it can produce transparent PNGs before processing the set.
2. Create a new run directory outside the repo unless the user requests committed assets. Keep `sources/`, `processed/`, and `sources.csv` with `slot,source_page,asset_url,creator,license_or_terms,notes`.
3. Browse current sources. Start with Reaction Stash when it still provides suitable cutouts, then use comparable reaction-sticker libraries. Open the source pages and record provenance. Never describe an image as open source or commercially licensed unless its terms say so.
4. Curate at least 1.5 times the requested count. Prefer static reaction cutouts with a strong silhouette, expressive pose, and legibility at chat size. A tightly grouped two-subject cutout like the woman pointing at the cat is suitable. For a modern pack, browse current reaction categories and favor recent internet visual language.
5. Reject multi-panel memes, caption templates, screenshots, prominent text, logos, watermarks, emoji-only art, weak crops, tiny subjects, and near duplicates. Do not use animated GIFs.
6. Build and inspect numbered source contact sheets before processing. Keep only candidates that already read as stickers.
7. Process one source per image editing call with the prompt in [EDIT-PROMPT.md](EDIT-PROMPT.md). Set `transparent_background: true` when the tool supports it. Calls may run in batches of 10–20. Carry `{slot, source}` through each call; never infer slot order from completion time.
8. Save the resulting PNG for each slot. For Codex imagegen, take the final absolute `.png` path in `output_hint`. Preserve originals. Copy each accepted output to `processed/<slot>-reaction-sticker.png`.
9. Inspect every result on a dark contact sheet. Replace redraws, lost details, opaque corners, malformed borders, duplicate subjects, or unreadable silhouettes. Retry failures with unused curated sources until every numbered slot exists.
10. Run the deterministic packager. It validates numbering, real alpha transparency, visible pixels, and unique hashes; then creates the preview, manifest, additions ZIP, combined folder, and combined ZIP.

Run the script beside this `SKILL.md` (from the skill directory):

```bash
python3 scripts/package_stickers.py \
  --additions /tmp/sticker-run/processed \
  --expected-additions 100 \
  --start-index 101 \
  --existing /tmp/sticker-pack-100 \
  --output-root /tmp/sticker-delivery \
  --slug reaction-stickers
```

Omit `--existing` for a new pack. Use a fresh output directory so previous deliveries remain intact.

## Acceptance criteria

- Exact requested count and continuous numbering.
- Static PNGs with genuinely transparent pixels and visible opaque content.
- One readable reaction cutout per sticker with a consistent smooth white outline.
- No exact duplicate files, obvious near duplicates, meme panels, captions, or watermarks.
- Preview reviewed at full size; ZIP entry counts match the validated manifest.
- Final response links the additions ZIP, combined ZIP when applicable, and preview. State that the images were sourced and processed, and that commercial rights require checking the recorded source terms.
