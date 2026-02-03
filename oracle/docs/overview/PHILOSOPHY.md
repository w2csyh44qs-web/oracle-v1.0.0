# GOATED Content Automation - Philosophy & Goals

**Last Updated:** December 26, 2025 (P6 - Layer Architecture & Automation with Granular Control)
**Purpose:** Project goals, development principles, vision system concepts, and design decisions.

---

## Table of Contents

1. [End Goal](#1-end-goal)
2. [Development Philosophy](#2-development-philosophy)
   - 2.5 [Layer Architecture (Canonical Reference)](#25-layer-architecture-canonical-reference) ← **P6: AUTHORITATIVE**
   - 2.6 [Automation with Granular Control](#26-automation-with-granular-control-p6) ← **P6: CORE RULE**
3. [Vision System](#3-vision-system)
4. [Critical Feedback Loops](#4-critical-feedback-loops)
5. [Key Design Decisions](#5-key-design-decisions)
6. [Success Criteria](#6-success-criteria)
7. [Questions Before Building](#7-questions-before-building)
8. [Multi-User Considerations](#8-multi-user-considerations)
9. [Future Planning](#9-future-planning)

---

## 1. End Goal

**High production value output via a largely automated but interactive workflow, with minimal cost.**

The system should enable:
- **Comprehensive iterative creation** for marketing purposes
- **Polished media content** organized as segments and individual posts/reels/videos
- **Toggleable on/off** based on need, current trends, and analytics feedback
- **Bird's eye + granular control** - Strategic observations at script start + layer-specific adjustments
- **Multi-user usability** with clear UX and cancel options throughout
- **Minimal cost** through strategic tool selection and optimization

---

## 2. Development Philosophy

### 2.1 Core Principles

#### Modular & Lean Architecture
- Each layer is isolated and reusable
- Avoid tight coupling between components
- Periodic bloat scans to keep code clean
- Clear separation of concerns

#### Placeholder-First Development
- Build placeholders for future features (orchestrators, visions, analytics)
- Document integration points clearly
- Avoid premature implementation
- Build only what's needed for current milestone

#### Cost vs. Production Benefit
- Evaluate tools continuously (cost, quality, ease of use)
- Add/remove tools as necessary based on results
- Suggestions welcome and evaluated on merit
- Optimize for minimal cost without sacrificing quality

#### Multi-User Usability
- Cancel options in ALL menus without saving changes
- Clear prompts and helpful error messages
- Intuitive workflows
- Not just for technical users

#### Comprehensive Documentation
- Document conceptual AND technical foundations
- Survive context window compression/loss
- Include "why" not just "how"
- Keep timeline and build order visible

### 2.2 Build Philosophy

1. **Build modularly** - Avoid rework by keeping layers isolated
2. **Document placeholders** - Mark future integrations clearly
3. **Test incrementally** - Each milestone validates core flow
4. **Iterate based on feedback** - Real usage drives refinement
5. **Think multi-sport** - Architecture supports expansion
6. **Cost vs. production benefit** - Evaluate tools continuously, optimize for minimal cost
7. **Multi-user usability** - Clear UX, cancel options, helpful prompts
8. **Periodic bloat scans** - Keep code lean and clear
9. **Automation with Granular Control** - Every module supports full automation as the ideal, with granular manual control available when needed (see 2.5)

### 2.5 Layer Architecture (Canonical Reference)

> **AUTHORITATIVE LAYER DEFINITIONS** - Reference this when building or discussing layers.

| Layer | Name | Script | Purpose |
|-------|------|--------|---------|
| **L0** | Entry Point | `L0_pipeline.py` | Orchestrator, mode/preset selection, menu UI |
| **L1** | Data Source | `L1_data.py` | All data acquisition: APIs, web search, asset ingestion, local files |
| **L2** | Content Planning | `L2_calendar.py` | Calendar structure, scheduling |
| **L3** | Script/Prompt | `L3_ideas.py` | Transform data into ideas, prompts, text content |
| **L4** | Audio | `L4_audio.py` | Text-to-speech, audio processing |
| **L5** | Media Generation | `L5_media.py` | AI image generation, video creation |
| **L6** | Assembly | `L6_assembly.py` | Combine components, overlays, conversions |
| **L7** | Distribution | `L7_distribution.py` | Organize outputs, move to final folders |
| **L8** | Analytics | `L8_analytics.py` | Performance tracking, feedback loops |

**Key Distinctions:**
- **L0 is NOT a processing layer** - It's the entry point that orchestrates L1-L8
- **L1 handles ALL data acquisition** - APIs, web scraping, asset downloads, local file access
- **New data sources go in L1** - Asset ingestion, new APIs, etc. are L1 tools
- **Presets define which layers run** - Not all presets use all layers

### 2.6 Automation with Granular Control (P6)

> **CORE DESIGN RULE:** Every layer/module must support both full automation (ideal) and granular manual control (when needed), with production quality being customizable at every level.

#### The Three Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| **Full Automation** | Sensible defaults, auto-detection, minimal input | Daily production workflow |
| **Guided Control** | Auto-suggests with user confirmation | Testing new presets, QA passes |
| **Granular Manual** | Full parameter control, override everything | Edge cases, debugging, experimentation |

#### Implementation Pattern

Every function/method that processes content should support:

```python
def process_asset(
    source: str,
    # Auto-detection (full automation)
    auto_detect: bool = True,      # Enable smart defaults
    # Granular overrides (manual control)
    name: str = None,              # Override auto-naming
    timestamps: List[str] = None,  # Override auto-segmentation
    extract: List[str] = None,     # Specify components
    **kwargs                       # Future extensibility
) -> Dict:
    """
    Full automation: process_asset(url)
    Guided: process_asset(url, auto_detect=True)  # shows what it detected
    Manual: process_asset(url, auto_detect=False, timestamps=["0:05-0:12"])
    """
```

#### Rules for Module Design

1. **Defaults enable automation** - Running with no args should "just work"
2. **Parameters enable control** - Every auto-behavior can be overridden
3. **CLI exposes all options** - User-facing scripts expose full parameter set
4. **Presets configure automation level** - Preset config can lock automation or require manual steps
5. **Logging shows decisions** - In auto mode, log what was detected/decided for transparency

#### Example: Asset Ingestion (L1)

| Behavior | Auto Mode | Manual Override |
|----------|-----------|-----------------|
| Asset naming | From video title/metadata | `--name "custom_name"` |
| Segmentation | Scene detection | `--timestamps "0:05-0:12"` or `--no-segment` |
| Component extraction | Based on preset needs | `--extract audio keyframes` |
| Categorization | Infer from content | `--type meme_template` |

#### Why This Matters

- **Production speed**: Daily content creation uses automation
- **Quality control**: Manual mode for important releases
- **Debugging**: When auto-detection fails, manual mode bypasses it
- **Experimentation**: Test new approaches without changing defaults
- **Preset flexibility**: Different presets can require different control levels

#### Preset Creation Rule (P6)

> **When creating new presets, ALWAYS design for both pipeline integration AND standalone callable components.**

1. **Pipeline-First**: Every preset runs through full L0-L7 by default
   - Entry via `L0_pipeline.py --preset <name>`
   - Layers skipped automatically if not needed (preset config controls this)

2. **Layer Callability**: Each layer's work must be callable independently
   - CLI: `python3 scripts/L6_assembly.py --preset meme_mashup --clips ...`
   - Python: `from scripts.L6_assembly import assemble_meme_mashup; result = assemble_meme_mashup(...)`

3. **Granular Control at Every Layer**:
   - L1: Choose data source (API, local assets, URL ingestion)
   - L4: Optional audio (TTS, extracted, provided, or none)
   - L5: Optional generation (use existing clips OR generate new)
   - L6: Full parameter control (transitions, overlays, output format)

4. **Why Both Modes**:
   - **Pipeline**: Batch processing, scheduled runs, consistent workflow
   - **Direct Call**: Quick one-offs, testing, debugging, experimentation

### 2.3 Reasoning & Thinking Style

**How Claude should think when working on this project.**

#### Universal Over Hardcoded
- Changes should work for ALL presets (old and new), not just the one being tested
- Only hardcode shared reference data (e.g., `PLAYER_TEAMS`, `team_cities`)
- Preset-specific logic belongs in preset config, not code

#### Multi-Preset, Multi-Module Architecture
- Multiple presets can pull from multiple modules - this is a core strength
- Shared extraction functions work for any preset
- No duplicate logic - if two presets need it, it goes in a shared module

#### Deep Contextual Understanding
- Domain knowledge matters - "vrabel-led defense" = New England's defense
- Extract meaning from ALL sentences - reasoning spans multiple clauses
- Player → Team attribution - Zay Flowers stats = BAL
- City → Team mapping - "Baltimore's must-win" = BAL
- Word boundaries in patterns - avoid "NE" matching inside "tuNNEl-vision"

#### Thesis-Driven Coherence
- Identify betting thesis FIRST (pass_based, run_based, situational)
- All content flows from thesis - cover, edges, highlights align
- Pattern priority matters - search thesis-relevant stats before generic
- Fallbacks should be thesis-aligned

#### Reasoning Process Documentation
- Document the "why" not just the "what"
- Track which patterns work and which don't
- Root cause analysis over symptom fixes

### 2.4 Cross-Session Communication

#### Dev → Oracle
- After design decisions: Flag `🚩 NEEDS_ORACLE_PASS` for doc updates
- After principle discoveries: Tell Oracle to document them
- Include the "why" in descriptions

#### Oracle Responsibilities
- Capture principles from Dev feedback - user comments often contain philosophy
- Update reference docs (PHILOSOPHY, ARCHITECTURE, WORKFLOW)
- Don't lose meta-insights from conversation

---

## 3. Vision System

### 3.1 Overview

The **Creative Vision Layer** sits above the technical pipeline and influences content style, tone, and format. Same technical pipeline, different creative outputs.

### 3.2 Vision Types (5 Types, Build Order)

#### 1. Generic/Trend-Informed (CURRENT - Baseline)
- **No characters**
- **No theme continuity required**
- **Pure trend-based content**
- What we've already built
- Baseline for comparison

#### 2. Trend-Informed Organic Theme (Next Phase)
- **Trend detection CREATES the vision**
- Theme develops organically over time
- Vision evolves based on what's trending
- Maintains congruence as it evolves
- **Layer 1 → Vision Orchestrator feedback loop**
- Brand "voice" emerges naturally

#### 3. Gil & Goldie Character Vision (Next Phase)
- **Defined character-driven brand**
- Stable theme and personalities
- **[OPTIONAL]** Can be trend-informed over time
- Requires character asset generation
- Higher production complexity

#### 4. AI-Generated Visions (Post-Launch)
- AI creates vision from user prompt
- Can reroll and tweak
- Save as custom vision
- Experimental/iterative

#### 5. Manual Custom Visions (Post-Launch)
- User-created from scratch
- Full creative control
- Can combine elements from other visions

### 3.3 Vision Toggleability

**Key Feature:** Visions can be toggled on/off
- Switch between visions for different content types
- Test multiple visions simultaneously
- A/B test vision performance
- Turn off visions temporarily (revert to generic)

**Use Cases:**
- Weekly Rankings: Generic vision (data-focused)
- Daily Segments: Character vision (personality-driven)
- Special Events: Custom vision (one-off themes)

### 3.4 Vision Touch Points

The active vision influences each layer:

| Layer | Vision Influence |
|-------|------------------|
| L1 Trends | Search query adjustments based on vision themes |
| L2 Calendar | Segment emphasis, content mix preferences |
| L3 Ideas | Tone, style, format in AI prompts |
| L4 Audio | Voice selection, speaking style |
| L5 Media | Visual style, overlay design, colors |
| L6 Assembly | Pacing, transition preferences, character integration |
| L7 Distribution | Platform-specific formatting, thumbnails |

### 3.5 Organic Theme Evolution

**For "Trend-Informed Organic Theme" vision:**

Trend detection **CREATES** the vision. Theme develops organically over time, evolving based on what's trending while maintaining congruence.

**Example Evolution:**
```
Week 1: Trends = "bad beats" + "player trash talk" → Vision emphasizes humor
Week 2: Trends = "analytics deep dives" → Vision adds data storytelling
Week 3: Vision maintains both, creating consistent brand voice
Week 4: Trends = "character moments" → Vision layers in personality
```

This creates a **living brand** that:
- Responds to audience interests
- Maintains continuity
- Feels authentic (not forced)
- Evolves with the sports betting community

---

## 4. Critical Feedback Loops

### 4.1 Analytics → Layers (Post-Launch)

**Layer 8 → Layer 2:**
- Segment performance metrics
- Content mix optimization (entertainment/value ratio)
- Best posting times by segment

**Layer 8 → Layer 1:**
- High-performing topics
- Trending keywords that drove engagement
- Topics to avoid (low performance)

**Layer 8 → Vision Orchestrator:**
- Theme engagement data
- Character moment performance (for character visions)
- Trend alignment success rates

### 4.2 Trends → Vision Orchestrator

**Layer 1 → Vision Orchestrator:**
- Trend detection **CREATES** the vision for "Trend-Informed Organic Theme"
- Vision develops organically over time
- Theme evolves based on what's trending
- Maintains congruence as it evolves
- This is how the brand develops its own "voice" naturally

---

## 5. Key Design Decisions

### 5.1 Why Modular Layers?
- Easier to debug (isolate issues to specific layer)
- Reusable across sports (NFL → NBA → Soccer)
- Can update one layer without breaking others
- Team collaboration (different people can own different layers)

### 5.2 Why Checkpoints Everywhere?
- User maintains creative control
- Multi-user usability (non-technical users can review)
- Catch errors early (before expensive operations)
- Cancel options prevent wasted work/cost

### 5.3 Why Placeholder-First?
- Avoid premature optimization
- Build only what's needed for current milestone
- Clear integration points for future features
- Documentation survives context loss

### 5.4 Why Vision System Above Layers?
- Creative direction informs technical execution
- Same technical pipeline, different creative outputs
- Toggleable visions allow experimentation
- Trend-informed visions create organic brand evolution

### 5.5 Why 8 Layers?
- Clear separation of concerns
- Each layer has one responsibility
- Easy to test and debug individually
- Supports different execution paths (skip layers, rerun layers)

---

## 6. Success Criteria

### 6.1 Week 14 Test (MVP) ✅
- [x] One complete Weekly Rankings video (45-60s)
- [x] Audio syncs correctly
- [x] Text overlays readable and timed properly
- [x] Video exports as playable MP4
- [x] Total cost < $5 for test video

### 6.2 First Publishable Output ✅ (Dec 18, 2025)
- [x] Production-quality infographic with AI-generated images
- [x] Carousel workflow (3-slide Instagram carousel)
- [x] GoatedBets API integration for real-time data
- [x] Illustrated watercolor style established
- [x] Brand assets documented (logo prompts, color palette)

### 6.3 Current Focus (Week 16+)
- [x] Instagram carousel generator (`instagram_carousel_generator.py`)
- [x] API-driven content (GoatedBets matchup-analysis endpoint)
- [x] L6 PIL processor (logo overlay, aspect conversion, gradients)
- [x] L6 FFmpeg processor (Ken Burns, slideshows, video manipulation)
- [x] Full carousel pipeline (L3→L5→L6→L7) with real player data
- [ ] Multiple matchups per week (PHI@WAS, GB@CHI, etc.)
- [ ] Processor Phase 1 expansion (watermarks, text cards, video trim/concat)

### 6.4 Post-Launch (Ongoing)
- [ ] Layer 8 analytics feeding back to Layers 1-2
- [ ] Vision evolving organically based on trends
- [ ] Multi-sport support (NBA, Soccer)
- [ ] AI-generated vision option
- [ ] Full automation with manual review checkpoints

---

## 7. Questions Before Building

Before implementing any new feature:

1. **Is it needed for current milestone?** (If no → placeholder)
2. **Does it add cost?** (Evaluate alternatives)
3. **Is it modular?** (Can it be isolated?)
4. **Does it have a checkpoint?** (User review point)
5. **Can it be cancelled?** (No unwanted changes)
6. **Is it documented?** (Conceptual + technical)
7. **Does it follow UX patterns?** (One-handed nav, cancel options)
8. **What's the preset implication?** (Does it need a preset file?)

---

## 8. Multi-User Considerations

### 8.1 Not Just for Technical Users

- Clear error messages (no stack traces to end user)
- Helpful prompts with examples
- Sensible defaults
- Progress indicators for long operations
- Ability to save/resume workflows

### 8.2 Cancel Options Required

**EVERY interactive menu MUST have:**
- Clear cancel option ('c', 'cancel', 'q', 'quit', 'b' for back)
- No changes saved on cancel
- Confirmation prompts for destructive actions
- Ability to navigate back to previous menu
- Exit without errors

**Example:**
```
Choose an option: [c]ontinue / [e]dit / [q]uit: q
❌ Exiting without saving changes...
```

### 8.3 Error Handling

- No stack traces shown to end users
- Clear, actionable error messages
- Suggest next steps on errors
- Graceful degradation (continue with defaults if possible)

### 8.4 Progress Indicators

- Show progress for long operations
- Estimated time remaining where applicable
- Clear status updates
- Allow cancellation of long-running processes

---

## 9. Future Planning

See `optimization/IDEAS_BACKLOG.md` for consolidated future planning.

**Relevant sections:**
- YES > Vision System > Trend-Informed Organic Theme, Gil & Goldie
- YES > Architecture > L8 feedback loops, Multi-sport support
- Reference > Expansion Phases (Phases 1-5)
- Reference > Analytics Evolution, Automation Evolution

---

## Reference

For technical implementation details, see:
- **ARCHITECTURE.md** - Layer breakdown, file structures, system flows
- **WORKFLOW.md** - Operational processes, build breaks
- **UX_RULES.md** - UI patterns, checkpoint patterns
- **TOOLS_REFERENCE.md** - API pricing, tool comparisons

---

*This document captures the WHY of the GOATED automation project. Update when goals or principles change.*
