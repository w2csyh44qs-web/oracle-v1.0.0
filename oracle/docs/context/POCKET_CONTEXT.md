# Pocket Context Document

> **YOU ARE POCKET** - M1 Air portable workstation with fallback ports.

**Last Updated:** January 7, 2026 (P24)
**Session:** P24
**Purpose:** Portable session context for M1 MacBook Air - read this FIRST

---

## CURRENT DATE & SEASON

> **Today's Date:** January 7, 2026
> **Current NFL Season:** 2025-2026 (NOT 2024-2025)
> **Current Week:** Week 18 NFL (Final Regular Season)

---

## POCKET SESSION PROTOCOL

### Resume Prompt
```
you are pocket - read POCKET_CONTEXT.md
```

### On Every Resume:
1. **Read this entire file FIRST**
2. **Start in fallback mode**: `python oracle/daemon.py start --fallback`
3. **Check daemon status**: `python oracle/daemon.py status`
4. **Continue pending tasks** - From Pending Tasks section

### Essential Rules

1. **Pocket = M1 Air Context** - Portable, fallback ports, mobile development
2. **Fallback Ports**: Backend 5002, Frontend 5174 (avoid main machine conflicts)
3. **All Contexts Available**: Can do Dev, Dash, Crank, Oracle work as needed
4. **Sync with Oracle**: Report sync_complete, fallback_active via daemon
5. **iCloud Sync**: Project auto-syncs - check for conflicts before starting
6. **Efficiency Focus**: M1 Air has limited resources - be mindful
7. **Test Locally**: Verify changes work on Air before committing
8. **Document Machine-Specific**: Note if something only works on Air

---

## FALLBACK MODE

### Why Fallback Ports?

When working on M1 Air while main Mac Studio is running:
- Main machine: Backend 5001, Frontend 5173
- M1 Air: Backend 5002, Frontend 5174

This prevents port conflicts when both machines are active.

### Starting in Fallback Mode

```bash
# Start daemon in fallback mode
python oracle/daemon.py start --fallback

# Or export environment variable
export GOATED_FALLBACK=1
python oracle/daemon.py start

# Check which mode is active
python oracle/daemon.py context
```

### V2 Servers in Fallback

```bash
# Backend (fallback port 5002)
FLASK_PORT=5002 python3 -m app.main

# Frontend (fallback port 5174)
cd app/frontend
VITE_PORT=5174 npm run dev
```

---

## MULTI-MACHINE WORKFLOW

### iCloud Sync Protocol

1. **Before Starting on Air:**
   - Close VS Code on main machine
   - Wait ~30s for iCloud sync
   - Open VS Code on Air
   - Check for merge conflicts in git status

2. **Before Switching Back:**
   - Run `python oracle/daemon.py send pocket oracle "sync_complete"`
   - Close VS Code on Air
   - Wait for iCloud sync
   - Open on main machine

3. **Conflict Resolution:**
   - If conflicts: Keep the most recent version
   - Check file timestamps
   - Use `git stash` if needed

### Machine-Specific Notes

| Feature | Main (Mac Studio) | Pocket (M1 Air) |
|---------|-------------------|-----------------|
| Backend Port | 5001 | 5002 |
| Frontend Port | 5173 | 5174 |
| Performance | Full | Limited (8GB RAM) |
| Daemon Mode | Normal | Fallback |
| Primary Use | Development | Mobile/Testing |

---

## QUICK COMMANDS

### Daemon Commands

```bash
# Start/stop
python oracle/daemon.py start --fallback
python oracle/daemon.py status

# Messaging
python oracle/daemon.py send pocket oracle "sync_complete"
python oracle/daemon.py messages --context pocket

# Health
python oracle/daemon.py audit --quick
```

### Development

```bash
# Activate venv
source venv/bin/activate

# Start backend (fallback)
FLASK_PORT=5002 python3 -m app.main

# Start frontend (fallback)
cd app/frontend && VITE_PORT=5174 npm run dev

# Test adapters
python3 -c "from app.core.pipeline.adapters import *; print('OK')"
```

### Content Generation

```bash
# Quick carousel
python3 scripts/L0_pipeline.py --preset insights_carousel

# Single matchup
python3 scripts/L0_pipeline.py --away DET --home MIN

# View outputs
ls content/nfl/2025-2026/regular_season/week18/
```

---

## CURRENT STATE

| Metric | Value |
|--------|-------|
| Machine | M1 MacBook Air (8GB) |
| Mode | Fallback (5002/5174) |
| Daemon | oracle/daemon.py --fallback |
| Sync | iCloud automatic |
| Contexts | Can work on all 5 contexts |

---

## PENDING TASKS

- [ ] Pokemon Pipeline Integration - Implement Phase 1 (Backend Infrastructure)
  - See: `docs/plans/pokemon-pipeline-integration.md`
  - Create Pokemon generator processors (sprite, battle, card)
  - Integrate Gemini/Veo APIs for generation
  - Add AI enhancement for creative assistance
- [ ] Test V2 dashboard on M1 Air
- [ ] Verify fallback ports work correctly

---

## RECENT CHANGES

### January 17, 2026 - Session 24 (P24)
- **Pokemon Pipeline Integration Plan**
  - Created comprehensive implementation plan (docs/plans/pokemon-pipeline-integration.md)
  - 6 granular presets: Sprite Gen, Battle Scene, Battle Card, Pokedex, Trading Card, Assembler
  - Meta-commentary + educational stats focus
  - AI enhancement via Claude for descriptions, animations, commentary
  - Template library with hybrid approach (pre-built + custom uploads)
  - Timeline: 12-15 days, 22 new files, 8 files to modify
- **Video Concatenation**
  - Combined divisional round Pokemon clips with audio balancing
  - First clip audio boosted 2x for volume consistency
  - Bears/Rams clips assembled successfully

### January 7, 2026 - Session 21 (P21)
- **V2 Context Update**
  - Trimmed from 1000+ lines to ~200 lines
  - Toolkit docs moved to TOOLS_REFERENCE.md
  - Updated for V2 daemon commands
  - Simplified multi-machine workflow

### December 29, 2025 - Session 20 (P20)
- Week 17 Sunday slate generation (11 matchups, 66 slides + 66 reels)
- Ink splatter intensity reduced (15-40%)
- LLM extraction toggle tested

### Earlier Sessions (P1-P19)
**See `docs/CHANGELOG.md` for archived session details.**

Key milestones:
- P9-P12: Display Mode Registry, Smart Text Toolkit
- P16-P17: Meme creation experiments
- P18: Vision system design

---

## TOOLKIT REFERENCE

All toolkit documentation has been consolidated to **TOOLS_REFERENCE.md**:

- **Smart Text Analysis** - `analyze_for_highlights()`, `analyze_for_buckets()`, etc.
- **LLM Extraction** - `extract_betting_thesis_llm()`, `extract_cover_insight_llm()`
- **Preset Building Rules** - Tool audit checklist

See: `docs/overview/TOOLS_REFERENCE.md` > "Smart Text Analysis Toolkit (P9)"

---

## SESSION END CHECKLIST

Before ending a Pocket session:
1. Update "Recent Changes" with today's work
2. Run: `python oracle/daemon.py send pocket oracle "sync_complete"`
3. Close VS Code
4. Wait for iCloud sync before switching machines

---

*Pocket Context Document - M1 Air portable workstation*
