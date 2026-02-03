# GOATED Content Automation

Automated content pipeline for sports betting social media - from trend detection to video distribution.

---

## Overview

8-layer pipeline that transforms trending topics into ready-to-publish video content:

```
Layer 1: Entry Point         - Choose mode (Discovery or Generate)
Layer 2: Calendar & Segments - Configure weekly content
Layer 3: Idea Creation       - AI-generated content ideas
Layer 4: Audio Generation    - ElevenLabs/OpenAI TTS with presets
Layer 5: Media Components    - AI images, stock footage, overlays
Layer 6: Video Assembly      - Final MP4 with caption styles
Layer 7: Distribution        - Platform profiles, caption generation
Layer 8: Analytics           - Performance tracking, feedback loops
```

### Two Content Creation Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Discovery Mode** | Web search → trends → L2/L3 → video | Find what's trending, create content from it |
| **Generate Mode** | LLM-direct → video | Create content directly via AI (e.g., Best Bets) |

```
DISCOVERY MODE                  GENERATE MODE
┌─────────────────────┐         ┌─────────────────────┐
│  Web Search         │         │  LLM Direct         │
│  (Tavily)           │         │  (Perplexity)       │
│         ↓           │         │         ↓           │
│  all_trends.json    │         │  ideas_approved.json│
│         ↓           │         │         │           │
│  L2 → L3 → L4+      │         │  L4 → L5 → L6 → L7  │
└─────────────────────┘         └─────────────────────┘
```

---

## Quick Start

### 1. Setup Environment

```bash
# Navigate to project
cd "/Users/Vanil/Library/Mobile Documents/com~apple~CloudDocs/*VITAL SIGNS/LIFE/INVESTMENTS/Goated Bets/Marketing/*AutomationScript"

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file with:
```
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
FAL_KEY=your_key_here
PEXELS_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
```

### 3. Run Pipeline

#### Recommended: Use L0 Entry Point
```bash
# Start the content pipeline (interactive mode selection)
python3 scripts/content_pipeline.py
```

This presents a menu to choose between Discovery Mode and Generate Mode, configure tools, and load/save presets.

#### Discovery Mode (Trend-based content)
```bash
# Or run directly: Layer 1 - Detect trends via web search
python3 scripts/web_search_trend_detector.py

# Layer 2: Configure calendar & segments
python3 scripts/calendar_config.py regular_season week14

# Layer 3: Generate ideas from trends
python3 scripts/idea_creation.py regular_season week14 --num-ideas 10

# Layer 3b: Approve ideas
python3 scripts/approve_ideas.py regular_season week14

# Layer 4-7: Production pipeline
python3 scripts/audio_sync.py regular_season week14
python3 scripts/media_generation.py regular_season week14
python3 scripts/assembly.py regular_season week14
python3 scripts/distribution.py regular_season week14

# Layer 8: Analytics (post-publish)
python3 scripts/analytics.py regular_season week14
```

#### Generate Mode (LLM-direct content)
```bash
# Skip L1/L2 - Generate content directly via preset
python3 scripts/idea_creation.py --content-preset best_bets_slate --no-checkpoint

# Continue with production pipeline (L4-L7)
python3 scripts/audio_sync.py regular_season week16 --no-checkpoint
python3 scripts/media_generation.py regular_season week16 --no-checkpoint
python3 scripts/assembly.py regular_season week16 --no-checkpoint
python3 scripts/distribution.py regular_season week16 --no-checkpoint
```

### Auto Mode (Skip Checkpoints)
```bash
python3 scripts/audio_sync.py regular_season week14 --no-checkpoint
python3 scripts/media_generation.py regular_season week14 --no-checkpoint
python3 scripts/assembly.py regular_season week14 --no-checkpoint
python3 scripts/distribution.py regular_season week14 --no-checkpoint
```

### Post-Processing Tools (L6 Processors)

**PIL Processor** - Image manipulation:
```bash
# Logo overlay
python3 scripts/pil_processor.py logo image.jpg --position top-left

# Aspect ratio conversion
python3 scripts/pil_processor.py convert image.jpg --to 9:16 --bg-color cream
python3 scripts/pil_processor.py convert image.jpg --to 9:16 --blur-bg

# Watermark
python3 scripts/pil_processor.py watermark image.jpg --text "@GoatedBets"

# Gradient background
python3 scripts/pil_processor.py gradient 1080 1920 --colors charcoal navy -o bg.png

# Text card
python3 scripts/pil_processor.py textcard "BEST BET" --bg cream --size 60
```

**FFmpeg Processor** - Video generation:
```bash
# Static image to video
python3 scripts/ffmpeg_processor.py static image.jpg -d 5

# Ken Burns effect
python3 scripts/ffmpeg_processor.py kenburns image.jpg --zoom in -d 5

# Carousel to slideshow
python3 scripts/ffmpeg_processor.py slideshow slide1.jpg slide2.jpg -o reel.mp4 --kenburns

# Video trimming
python3 scripts/ffmpeg_processor.py trim video.mp4 --start 0:05 --end 0:30

# Concatenate videos
python3 scripts/ffmpeg_processor.py concat video1.mp4 video2.mp4 -o merged.mp4

# Burn-in subtitles
python3 scripts/ffmpeg_processor.py subtitles video.mp4 --srt captions.srt
```

---

## Project Structure

```
*AutomationScript/
|-- context/                 # Session state documents
|   |-- DEV_CONTEXT.md                 # Development session state
|   |-- ORACLE_CONTEXT.md              # Maintenance session state
|
|-- scripts/                 # Pipeline scripts (Layers 0-8)
|   |-- content_pipeline.py            # L0: Entry point & mode selection
|   |-- web_search_trend_detector.py   # L1: Discovery Mode web search
|   |-- calendar_config.py             # L2: Calendar + segments
|   |-- idea_creation.py               # L3: AI idea generation
|   |-- approve_ideas.py               # L3b: Approval checkpoint
|   |-- audio_sync.py                  # L4: TTS generation
|   |-- media_generation.py            # L5: Video components
|   |-- assembly.py              # L6: Final assembly
|   |-- distribution.py                # L7: Platform distribution
|   |-- analytics.py                   # L8: Performance analytics
|
|-- config/                  # Configuration files
|   |-- nfl_calendar.py              # Season structure
|   |-- platforms.py                 # Platform definitions
|   |-- tool_config.json             # Tool selection & fallbacks
|   |-- script_presets.json          # Content presets (Generate Mode)
|   |-- audio_presets.json           # L4 presets
|   |-- media_presets.json           # L5 presets
|   |-- assembly_presets.json        # L6 presets
|   |-- distribution_presets.json    # L7 presets
|
|-- content/                 # Generated content
|   |-- nfl/2025-2026/[phase]/[week]/
|       |-- ideas_approved.json
|       |-- audio/*.mp3
|       |-- media/[idea_id]/
|       |-- assembled/*.mp4
|       |-- final/[platform]/*.mp4
|
|-- maintenance/             # Project health tools
|   |-- project_oracle.py            # Health & optimization agent
|   |-- health_monitor.py            # Real-time health dashboard
|   |-- ORACLE_README.md             # Oracle documentation
|
|-- optimization/            # Optimization tracking
|   |-- OPTIMIZATION_LOG.md          # Running log by date
|   |-- IDEAS_BACKLOG.md             # Future planning
|
|-- docs/                    # Reference documentation
|   |-- ARCHITECTURE.md              # Technical specs
|   |-- PHILOSOPHY.md                # Goals & principles
|   |-- WORKFLOW.md                  # Operational processes
|   |-- TOOLS_REFERENCE.md           # API pricing
|   |-- UX_RULES.md                  # UI/UX patterns
|   |-- CODE_HISTORY.md              # Architecture decisions & design history
|
|-- reports/                 # Oracle outputs
|   |-- snapshots/                   # Context snapshots
|   |-- ORACLE_REPORT_*.md           # Health reports
|
|-- output/                  # Trend detection output
|   |-- all_trends.json
|
|-- README.md                # This file
|-- .env                     # API keys (git-ignored)
|-- venv/                    # Virtual environment
```

---

## Platform Support

| Platform | Max Duration | Buffer.com | Aspect Ratio |
|----------|--------------|------------|--------------|
| YouTube Shorts | 60s | Yes | 9:16 |
| Instagram Reels | 90s | Yes | 9:16 |
| TikTok | 600s | No (manual) | 9:16 |
| X/Twitter | 140s | Yes | 9:16 |
| YouTube Long | No limit | No (manual) | 16:9 |

**Presets:**
- `universal` - All short-form (less than 60s, works everywhere)
- `buffer_only` - Buffer-supported platforms
- `quick_viral` - TikTok + Instagram

---

## Output Folders

After distribution (L7), each video is placed in **one folder** based on duration:

| Duration | Folder | Platform Support |
|----------|--------|------------------|
| 60s or less | `universal (<60s)/` | All platforms |
| 61-90s | `instagram_reels (<90s)/` | IG Reels, TikTok, X |
| 91-140s | `x_twitter (<140s)/` | X/Twitter, TikTok |
| 141-600s | `tiktok (<600s)/` | TikTok only |
| Over 600s | `youtube_long (no limit)/` | YouTube only |

---

## API Costs

| Service | Cost | Usage |
|---------|------|-------|
| OpenAI GPT-4o-mini | ~$0.001/run | Trend analysis, idea generation |
| ElevenLabs | ~$0.30/min | TTS audio |
| Tavily | Free tier | Web search |
| FAL AI | ~$0.03/image | Image generation |
| Pexels | Free | Stock footage |

**Estimated weekly cost:** ~$0.65 for typical usage

---

## Documentation

| Document | Purpose |
|----------|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical architecture, layer details |
| [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) | Goals, principles, vision system |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | Operational processes, build breaks |
| [docs/TOOLS_REFERENCE.md](docs/TOOLS_REFERENCE.md) | API pricing, tool comparisons |
| [docs/UX_RULES.md](docs/UX_RULES.md) | UI/UX patterns for scripts |
| [docs/CODE_HISTORY.md](docs/CODE_HISTORY.md) | Architecture decisions & design history |

### Session Documents

| Document | Purpose |
|----------|---------|
| [context/DEV_CONTEXT.md](context/DEV_CONTEXT.md) | Development session state - Claude reads first |
| [context/ORACLE_CONTEXT.md](context/ORACLE_CONTEXT.md) | Maintenance session state |

---

## Project Health (Oracle)

The project includes automated health monitoring tools:

```bash
# Quick health check
python3 maintenance/project_oracle.py status

# Full audit
python3 maintenance/project_oracle.py audit

# Save context before compaction
python3 maintenance/project_oracle.py autosave
```

### Health Monitor (Optional)

Real-time dashboard in a dedicated terminal:

```bash
# Start health monitor
python3 maintenance/health_monitor.py

# Minimized mode (single status line)
python3 maintenance/health_monitor.py --mode min
```

**Features:** Real-time health score, autosave tracking, file change monitoring, escalating alerts.

See [maintenance/ORACLE_README.md](maintenance/ORACLE_README.md) for full documentation.

---

## Troubleshooting

### No trends found
- Run `web_search_trend_detector.py` first
- Check `output/all_trends.json` exists

### OPENAI_API_KEY not found
- Create `.env` file in project root
- Add your API keys

### Audio generation fails
- Check ELEVENLABS_API_KEY in `.env`
- Verify account has credits

### Import errors
- Activate venv: `source venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

---

## Development

### Running Tests
```bash
python3 tests/test_layer2.py
```

### UX Guidelines
All interactive scripts follow patterns in [docs/UX_RULES.md](docs/UX_RULES.md):
- One-handed navigation (single-letter shortcuts)
- Consistent checkpoints
- Cancel options in all menus

---

## Glossary

| Term | Definition |
|------|------------|
| **Layer** | One stage of the content pipeline (L1-L8) |
| **Mode** | Content creation approach: Discovery (trend-based) or Generate (LLM-direct) |
| **Vision** | Creative direction that influences content style across all layers |
| **Preset** | Pre-configured settings for a layer (e.g., voice style, caption format) |
| **Content Preset** | Full production chain settings for Generate Mode (e.g., `best_bets_slate`) |
| **Discovery Preset** | Saved search configuration for Discovery Mode |
| **Tool Config** | User's default tool selections with fallback chains (`config/tool_config.json`) |
| **Data Sources** | External APIs for content/data (tavily, perplexity, goatedbets_api) - part of Tool Config |
| **ToolResolver** | Shared class that resolves which tool to use based on CLI > Preset > Config > Fallback |
| **Checkpoint** | Interactive pause point for user review and approval |
| **Segment** | Content category (e.g., Bad Beats Monday, Lock of the Week) |
| **Phase** | Season period (preseason, regular_season, playoffs, etc.) |
| **Context File** | Session state document (DEV_CONTEXT.md, ORACLE_CONTEXT.md) |
| **Oracle** | Automated health monitoring agent |
| **Health Monitor** | Real-time dashboard for project health visibility |

---

**Status:** Layers 1-8 complete | Discovery Mode built | Generate Mode building
