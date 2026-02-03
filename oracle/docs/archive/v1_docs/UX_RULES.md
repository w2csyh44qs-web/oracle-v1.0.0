# UX Rules Reference
**Last Updated:** December 20, 2025

**Purpose:** Consistent UX patterns across all pipeline scripts and L6 processors. Reference after compaction.

---

## Core Principles

1. **One-Handed Navigation** - No "Press Enter to continue" prompts
2. **Menu Auto-Return** - After any action, re-show the menu automatically
3. **Minimal Redundancy** - Only show info relevant to current context
4. **Consistent Checkpoints** - All layers use the same pattern

---

## Checkpoint Pattern (ALL Layers)

```python
def checkpoint(self):
    # 1. Show summary/overview
    print("\n" + "="*80)
    print("LAYER X: [NAME] - Summary")
    print("="*80)
    # ... show relevant stats ...

    # 2. Checkpoint header
    print("\n" + "="*80)
    print("CHECKPOINT: [Purpose]")
    print("="*80)

    # 3. Options menu
    print("\nOptions:")
    print("  [c] Continue to next layer")
    print("  [v] View details")
    print("  [e] Edit")
    print("  [q] Quit")

    # 4. While loop for navigation
    while True:
        choice = input("\nChoice: ").strip().lower()
        if choice == 'c':
            break
        elif choice == 'q':
            return  # or exit gracefully
        # ... handle other options ...
```

---

## Naming Conventions

| Pattern | Example | Notes |
|---------|---------|-------|
| Script names | `calendar_config.py` | NO "layer" prefix |
| Output files | `ideas_approved.json` | NO "layer" prefix |
| Folder names | `youtube_shorts (<60s)` | Duration in parens |

---

## Script Start Pattern

```python
def run(self):
    print()  # Blank line for readability
    print("\n" + "="*80)
    print("LAYER X: [NAME]")
    print("="*80)
```

---

## Menu Design

**DO:**
- Single-letter shortcuts: `[c]`, `[v]`, `[q]`
- Consistent quit option: `[q] Quit`
- Show current state before options
- Return to menu after sub-actions

**DON'T:**
- "Press Enter to continue"
- Full words in brackets: `[continue]`
- Require scrolling to see options
- Force two-hand keyboard use

---

## Layer Transitions

End each layer with:
```python
print("\n" + "="*80)
print("LAYER X COMPLETE")
print("="*80)
print(f"\nNext: python scripts/[next_script].py {phase} {week}")
```

---

## Error Handling

- No stack traces to end users
- Clear, actionable messages
- Suggest next steps
- Graceful degradation when possible

---

## Platform Selection (Layer 3+)

- Interactive prompt OR `--platforms` CLI flag
- Presets: `universal`, `buffer_only`, `youtube_all`, `quick_viral`
- Show effective duration/resolution after selection
- Confirmation before proceeding

---

## Cancel Options

Every interactive menu MUST have:
- Clear cancel option (`q`, `quit`, `c` for cancel)
- No changes saved on cancel
- Confirmation for destructive actions

---

## Bird's Eye Input Pattern (Strategic Observations)

**Input Prompt Pattern:**
```python
print("="*80)
print("🦅 BIRD'S EYE INPUT (Optional)")
print("="*80)
print("Share any strategic observations about:")
print("  - Social media trends")
print("  - Audience behavior")
print("  - Platform dynamics")
print("  - Content preferences")
print()
print("Press Enter to skip, or type your thoughts:")
print()

birds_eye_input = input("> ").strip()
```

**Sport-Specific Input Pattern:**
```python
print("="*80)
print("🦅 BIRD'S EYE INPUT - [SPORT] SPECIFIC (Optional)")
print("="*80)
print("Share observations specific to [SPORT] content and audience.")
print()
print("Examples:")
print("  - \"[SPORT] fans trending towards [topic]\"")
print("  - \"[Community] tired of [trend]\"")
print("  - \"Want more [content type]\"")
print()
print("Press Enter to skip, or type your thoughts:")
print()
```

**Management UI Pattern (Layer 2 Checkpoint):**
```
Bird's Eye Observations:
1. [GLOBAL] "Users burnt out from social media" (Dec 3)
   Applied to: Vision, L1, L2, L3, L5 | Status: Active
   [d]eactivate / [e]dit / [r]emove

2. [NFL] "Trending towards Xs & Os" (Dec 3)
   Applied to: Vision, L2, L3 | Status: Active
   [d]eactivate / [e]dit / [r]emove

[a]dd new / [b]ack
```

**Key Points:**
- Optional input (Enter to skip)
- Show examples relevant to context
- Confirm recording with checkmark
- Show what will be informed by the observations

---

## L6 Processor CLI Pattern

The PIL and FFmpeg processors follow a consistent CLI subcommand pattern:

```bash
# PIL Processor (pil_processor.py)
python3 scripts/pil_processor.py <command> <input> [options]

# Commands:
#   logo      - Add logo overlay
#   convert   - Aspect ratio conversion
#   watermark - Add text watermark (Phase 1)
#   gradient  - Create gradient background (Phase 1)
#   textcard  - Create text card image (Phase 1)

# Examples:
python3 scripts/pil_processor.py logo image.jpg --position top-left
python3 scripts/pil_processor.py convert image.jpg --to 9:16 --bg-color cream
```

```bash
# FFmpeg Processor (ffmpeg_processor.py)
python3 scripts/ffmpeg_processor.py <command> <input> [options]

# Commands:
#   static    - Image to video (still frame)
#   kenburns  - Ken Burns zoom effect
#   slideshow - Multiple images to video
#   audio     - Add audio to video
#   trim      - Cut video to time range (Phase 1)
#   concat    - Join multiple videos (Phase 1)
#   subtitles - Burn-in SRT subtitles (Phase 1)

# Examples:
python3 scripts/ffmpeg_processor.py kenburns image.jpg --zoom in -d 5
python3 scripts/ffmpeg_processor.py slideshow *.jpg -o reel.mp4 --kenburns
```

**CLI Design Principles:**
- Subcommand-based structure (`processor.py <command> ...`)
- Consistent output flag: `-o` or `--output`
- Duration in seconds: `-d` or `--duration`
- Position as words: `--position top-left`
- Named colors: `--bg-color cream`, `--colors charcoal navy`

---

*Last updated: December 20, 2025*
