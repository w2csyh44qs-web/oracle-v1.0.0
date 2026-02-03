# Ideas Backlog

Consolidated future planning for the GOATED content automation project. Single source of truth for all ideas.

## Tiers
- **YES** - Approved for implementation when time allows
- **MAYBE** - Worth considering, needs more thought
- **NO** - Considered and rejected (kept for reference)
- **UNREVIEWED** - New ideas, not yet categorized

## How to Use
- Auto-updated when user responds "future" or "backlog" to recommendations
- Manually add ideas to UNREVIEWED section
- Periodically review UNREVIEWED and categorize
- Move YES items to Pending Tasks when ready to implement

---

## YES (Approved)

### Architecture
- L8 feedback loops implementation (L8 -> L7, L2, L1, Vision)
- Multi-sport support structure (NBA, Soccer, Tennis)
- Master orchestrator with full automation

### Content Features
- **Intelligent tagging system** - Auto-tag outputs with categories (game, player, bet type), links to L8 analytics for performance tracking
- **Poll generation capability** - Generate engagement content: "Which bet would you pick?", "What's the accurate line?", betting polls
- **Best Bets preset** - Web-grounded betting analysis with multi-model support (Gemini, Perplexity, GPT)

### AI Model Integrations
- **Gemini API** - Fast, cheap, good reasoning (gemini-1.5-flash) - preferred for Best Bets analysis
- **Perplexity Pro API** - Real-time web search built-in, citations - good for slate-wide picks

### Image/Video Generation Research
- **Midjourney** - High-quality image generation, investigate API access and pricing
- **Hailuo AI** - Video generation tool, investigate capabilities and integration

### Automation
- ~~Oracle Health Monitor~~ ✅ **IMPLEMENTED** (2025-12-08)
  - See `maintenance/health_monitor.py`
  - Full implementation: dashboard, file watching, alerts, oracle integration

### Package Structure
- `__init__.py` refactor when adding second maintenance tool
- Proper package structure for maintenance/ folder

### Vision System
- Trend-Informed Organic Theme vision implementation
- Gil & Goldie Character Vision implementation
- Vision metadata flow through all layers

### Context Management
- Cross-session briefing enhancements (context/oracle merge)

### Oracle Features
- **Gap check / optimization pass** - Scan code and docs for context rule violations (Rule 17 comprehensiveness, Rule 18 no hardcoded data, etc.)
- **ADR draft system** - Auto-create CODE_HISTORY.md drafts with 14-day stale tracking, user review at own pace
- **Claude usage monitor panel** - Display account usage % in health monitor (beneath health bar). Requires Anthropic Admin API key (`sk-ant-admin...`) which needs organization account. Endpoints: `/v1/organizations/usage_report/messages` for tokens, `/v1/organizations/cost_report` for costs. Individual accounts can use manual JSON file (`reports/.claude_usage.json`) as fallback.

### Optimization System
- **Pattern detection for repeated recommendations** - Track declined/backlogged items, avoid re-suggesting same session

---

## MAYBE (Considering)

### Architecture
- Real-time trend detection
- Vision system expansion (AI-Generated, Custom)
- Platform API integration for analytics (TikTok, Instagram, YouTube)

### Tools/Skills
- Custom goated-pipeline MCP skill
- MCP server for content management
- xlsx skill for analytics exports

### Optimization System
- Adjustable priority weights per category
- Category enable/disable toggles

### Oracle Features
- Context digest generation (condensed summaries for large files)
- Automated triggers (VS Code open, git commit) - *deferred, session rules sufficient for now*
- Auto-write Recent Changes during autosave - *deferred, Claude's manual entries have better context/quality*

### Workflow
- Scheduled content generation
- CI/CD integration with git hooks
- Agent-based optimization

### Vision System
- AI vision generator with reroll/save
- Custom vision editor
- Vision marketplace/sharing

---

## NO (Rejected)

### Workflow
- Git hooks for oracle automation - *user unfamiliar with git hooks, session rules work well* - 2025-12-08

### Architecture
- Microservices architecture - *too complex for current scale, 8-layer pipeline sufficient* - 2025-12-05

---

## UNREVIEWED

*No items currently pending review.*

---

## Recently Reviewed

### Documentation
- ~~**BRAND_UX_RULES.md**~~ → **Merged into Task #10 (Brand Rules System)** - The STYLE_GUIDE.md created by Task #10 will cover visual brand UX: colors, typography, layout patterns, carousel specs, illustrated style guidelines. No need for separate doc. *Reviewed 2025-12-19*

---

## Migrated From

This file consolidates Future Planning sections from:
- `context/DEV_CONTEXT.md` - Planned Context Documents, Planned Features, Orchestrator Flow Design
- `context/ORACLE_CONTEXT.md` - Pending Features, Deferred Features, Multi-Agent Architecture, Background Health Monitor
- `docs/ARCHITECTURE.md` - Future Expansion (Phases 1-5)
- `docs/PHILOSOPHY.md` - Future Planning (Vision, Multi-Sport, Analytics, Automation evolution)
- `docs/CODE_HISTORY.md` - Future Decisions table

Original sections replaced with: `See optimization/IDEAS_BACKLOG.md`

---

## Reference: Expansion Phases

### Phase 1: Layer 8 Full Implementation
- Integrate platform APIs (TikTok, Instagram, YouTube)
- Automated data collection
- Advanced analytics dashboards
- Auto-adjustment of earlier layers

### Phase 2: Implement Feedback Loops
- Layer 8 -> Layer 7 integration (posting time optimization)
- Layer 8 -> Layer 2 integration (segment performance)
- Layer 8 -> Layer 1 integration (trending topics)
- Analytics-informed content mix

### Phase 3: Vision System Expansion
- Build trend-informed organic theme vision
- Build Gil & Goldie character vision
- AI vision generator
- Custom vision creator

### Phase 4: Multi-Sport Support
- NBA calendar and segments
- Soccer calendar and segments
- Tennis calendar and segments
- Sport-specific vision templates

### Phase 5: Automation & Agents
- Master orchestrator with full automation
- Scheduled content generation
- Agent-based optimization (Oracle pattern)
- CI/CD integration

---

## Reference: Multi-Agent Architecture

### Current Implementation
Oracle supports dynamic multi-agent context management via `CONTEXT_FILES` list:

```python
CONTEXT_FILES = [
    CONTEXT_DIR / "DEV_CONTEXT.md",
    CONTEXT_DIR / "ORACLE_CONTEXT.md",
    # Future agents:
    # CONTEXT_DIR / "CONTENT_CONTEXT.md",
    # CONTEXT_DIR / "ANALYTICS_CONTEXT.md",
    # CONTEXT_DIR / "SOCIAL_CONTEXT.md",
]
```

### Planned Agents
```
context/
├── DEV_CONTEXT.md           # Main development (active)
├── ORACLE_CONTEXT.md        # Health/maintenance (active)
├── CONTENT_CONTEXT.md       # Future: content generation agent
├── ANALYTICS_CONTEXT.md     # Future: analytics agent
└── SOCIAL_CONTEXT.md        # Future: social media management agent
```

---

## Reference: Analytics Evolution

| Phase | Description |
|-------|-------------|
| Phase 1 | Manual entry, basic tracking (current) |
| Phase 2 | Platform API integration |
| Phase 3 | Automated feedback loops |
| Phase 4 | Predictive optimization |

---

## Reference: Automation Evolution

| Phase | Description |
|-------|-------------|
| Phase 1 | Interactive with checkpoints (current) |
| Phase 2 | Auto-mode with approval points |
| Phase 3 | Scheduled generation |
| Phase 4 | Full automation with exception alerts |

---

*Ideas Backlog - Consolidated future planning for the GOATED content automation project.*
