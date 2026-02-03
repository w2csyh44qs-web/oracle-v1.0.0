# P29: Meme Support & Processor Restructure

**Status:** ✅ COMPLETE
**Created:** January 18, 2026
**Completed:** January 18, 2026
**Session:** D107

---

## Summary

1. Move `pil_processor.py` and `ffmpeg_processor.py` from L5 to L6 (they're assembly tools)
2. Add `create_image_meme()` function to pil_processor.py
3. Add `create_video_meme()` function for video memes with text overlay
4. Display modes:
   - **Image memes** → `single_image` (existing)
   - **Video memes** → `meme_overlay` (existing - single clip with text/logo)
   - **Video mashups** → `meme_mashup` (existing - multi-clip with transitions)

---

## Part 1: Restructure Processors (L5 → L6)

### Move Files

```
FROM: app/core/pipeline/layers/_L5/processors/pil_processor.py
TO:   app/core/pipeline/layers/_L6/processors/pil_processor.py

FROM: app/core/pipeline/layers/_L5/processors/ffmpeg_processor.py
TO:   app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py
```

### Rationale

- **L5** = Media Generation (AI image generation, stock fetching)
- **L6** = Assembly (combining media, overlays, effects)
- PIL and FFmpeg are assembly tools, not generation tools

---

## Part 2: Add Meme Functions

### `create_image_meme()`

Classic top/bottom text meme using Impact font with black stroke.

### `create_video_meme()`

Video meme with burned-in text overlay using FFmpeg drawtext filter.

---

## Part 3: Add Preset

Add `image_meme` preset to `script_presets.json` using `single_image` display mode.

Note: `meme_mashup` and `meme_overlay` presets already exist for video memes.

---

## Files Changed

| Action | File |
|--------|------|
| MOVE | `_L5/processors/pil_processor.py` → `_L6/processors/pil_processor.py` |
| MOVE | `_L5/processors/ffmpeg_processor.py` → `_L6/processors/ffmpeg_processor.py` |
| EDIT | `_L6/processors/__init__.py` - add exports |
| EDIT | `_L5/processors/__init__.py` - deprecation note |
| EDIT | `_L6/processors/pil_processor.py` - add meme functions |
| ADD | `config/script_presets.json` - image_meme preset |
