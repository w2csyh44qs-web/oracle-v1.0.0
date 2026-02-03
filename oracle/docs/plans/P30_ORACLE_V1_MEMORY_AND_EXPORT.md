# P30: Oracle v1.0 - Automatic Memory + Export-Ready Architecture

**Status:** Planning Complete - Ready for Implementation
**Created:** February 2, 2026 (O104)
**Target:** Transform Oracle into universal project management substrate

---

## Vision

Transform Oracle from a project-specific tool into a **universal project management substrate** that can:

1. **Automatically capture and learn from sessions** - No manual context updates required
2. **Deploy onto ANY Python project** via `oracle init` - Project-agnostic bootstrap
3. **Provide semantic memory** for cross-session intelligence and debugging
4. **Scale to other users** without requiring Oracle expertise

**Implementation Priority:**
1. Get CURRENT project (AutomationScript) working first with memory + export-ready features
2. Then expand to Goated Bets app (2.5 years old, large, disorganized - will test project-agnostic capabilities)
3. Package for GitHub release (anyone can use)

---

## Architecture: Memory System (Hippocampus)

**Neural Metaphor:** Hippocampus consolidates short-term memories before transfer to cortex (long-term storage). Similarly, this module consolidates session observations before updating context files.

**Important Note on Naming:**
- **Hippocampus** and **Cortex** are LOCATIONS (brain regions)
- Other modules are CELL TYPES (microglia, astrocytes, oligodendrocytes, etc.)
- This breaks from our cell-type convention but provides clear metaphor for memory consolidation

**Alternative Cell Type Suggestions:**
- **Pyramidal neurons** - Main excitatory neurons in hippocampus that encode memories
- **Place cells** - Hippocampal neurons that fire when observing specific locations (could metaphorically "observe" specific code locations)
- For now, keeping "Hippocampus" as the location-based name

### Components

```
oracle/memory/
├── hippocampus.py        # Core memory manager (~600 lines)
├── memory_hooks.py       # Lifecycle event capture (~200 lines)
├── context_updater.py    # Auto-update contexts (~300 lines)
├── memory_api.py         # Query interface (~250 lines)
└── memory_worker.py      # Background service (~200 lines)
```

### Storage

```
oracle/data/memory/
├── observations.db       # SQLite: structured metadata
├── embeddings/           # ChromaDB: semantic vectors
├── context_updates.json  # Pending updates queue
└── memory_config.json    # Configuration
```

### Key Features

1. **Automatic Capture** - Hooks into:
   - File changes (via sync_watcher integration)
   - Tool usage (via lifecycle hooks)
   - Session events (via context_manager)
   - Health audits (via microglia)

2. **3-Layer Progressive Disclosure:**
   - Layer 1: `search()` → Summaries only (~50 tokens/result)
   - Layer 2: `get_timeline()` → Context + relationships (~200 tokens)
   - Layer 3: `get_observations()` → Full details (~500 tokens)
   - **Result:** 50% token savings vs loading everything

3. **Automatic Context Updates:**
   - Pattern detection (repeated files, new features, decisions)
   - Markdown generation for context sections
   - Validation (line limits, format, no conflicts)
   - Auto-apply (confidence > 0.8) or queue for review

4. **Cross-Context Memory Sharing:**
   - Oracle coordinates knowledge links
   - Relevant observations injected into resume prompts
   - Example: Dev changes API → Dash session auto-notified

---

## Architecture: Export-Ready System

### Bootstrap Components

```
oracle/
├── cli.py (NEW)              # Main CLI entry point
├── bootstrap/                # Bootstrap system
│   ├── initializer.py        # oracle init command
│   ├── detector.py           # Project structure detection
│   ├── templates/            # Config templates
│   └── validator.py          # Post-init validation
├── config/                   # Project-specific (generated)
│   ├── oracle_config.json    # Paths, structure, settings
│   ├── layer_registry.json   # Layer definitions
│   └── tool_registry.json    # Tool/API definitions
└── project/
    └── cortex.py (MODIFIED)  # Now loads from configs
```

### Bootstrap Workflow

```bash
oracle init /path/to/project

# Steps:
1. Detect structure (framework, dirs, layers, tools)
2. Validate environment (Python 3.9+, permissions)
3. Generate configs (oracle_config.json, layer_registry.json)
4. Scaffold directories (oracle/config/, oracle/docs/)
5. Generate context files from templates
6. Validate installation (paths, imports, CLI)
7. Report success with next steps
```

---

## Critical Files to Modify/Create

### High Priority (Weeks 1-2)

1. **oracle/memory/hippocampus.py** (NEW - ~600 lines)
   - Core memory manager with SQLite + ChromaDB hybrid storage
   - Capture, query, and update methods

2. **oracle/bootstrap/initializer.py** (NEW - ~400 lines)
   - `oracle init` command implementation

3. **oracle/bootstrap/detector.py** (NEW - ~300 lines)
   - ProjectStructureDetector class

4. **oracle/validation/helicase.py** (MODIFY - add ~200 lines)
   - Add template generation and config file generation

5. **oracle/project/cortex.py** (MODIFY - remove ~100 lines, add ~50)
   - Remove hardcoded LAYER_DEFINITIONS dict (lines 41-100)
   - Load from oracle/config/layer_registry.json

### Medium Priority (Weeks 3-4)

6. **oracle/memory/memory_hooks.py** (NEW - ~200 lines)
7. **oracle/memory/context_updater.py** (NEW - ~300 lines)
8. **oracle/context/sync_watcher.py** (MODIFY - add ~50 lines)
9. **oracle/context/session_spawner.py** (MODIFY - add ~30 lines)
10. **oracle/cli.py** (NEW - ~150 lines)

---

## Implementation Phases

### Phase 1: Config Foundation (Weeks 1-2)

**Goals:**
- Extract hardcoded paths/layers to config files
- Make cortex.py config-driven

**Tasks:**
1. Create oracle/config/oracle_config.json template
2. Create oracle/config/layer_registry.json schema
3. Modify cortex.py to load layers from JSON
4. Test on current project (no regression)

**Success:**
✅ No hardcoded paths in cortex.py
✅ All Oracle commands still work
✅ Config validation catches errors

### Phase 2: Memory Core (Weeks 2-4)

**Goals:** Build automatic observation capture and semantic search

**Tasks:**
1. Create oracle/memory/hippocampus.py with SQLite + ChromaDB
2. Implement observation capture from sync_watcher
3. Build 3-layer query interface
4. Test memory capture across sessions

**Success:**
✅ Observations auto-captured
✅ Semantic search returns relevant results
✅ 50% token reduction via progressive disclosure

### Phase 3: Auto-Context Updates (Weeks 3-5)

**Goals:** Pattern detection and automatic markdown updates

**Tasks:**
1. Create oracle/memory/context_updater.py
2. Implement pattern detection
3. Build markdown generation
4. Add validation logic
5. Integrate with autosave

**Success:**
✅ Context files stay current without manual edits
✅ 80%+ auto-applied updates are correct
✅ Context files remain under 500 lines

### Phase 4: Bootstrap System (Weeks 3-5) *Parallel with Phase 3*

**Goals:** `oracle init` works on any Python project

**Tasks:**
1. Create oracle/bootstrap/detector.py
2. Extend helicase.py with template generation
3. Create oracle/bootstrap/initializer.py
4. Build template system
5. Test on current project + 5 other project types

**Success:**
✅ `oracle init` succeeds on current project
✅ Generated configs are valid
✅ Helpful errors for validation failures

### Phase 5: Polish & Documentation (Weeks 6-8)

**Goals:** Production-ready quality and external user testing

**Tasks:**
1. Error handling overhaul
2. CLI improvements
3. Performance optimization
4. Comprehensive documentation
5. Test on Goated Bets
6. Onboard 3 external users

**Success:**
✅ Documentation complete
✅ 3 external users onboard successfully
✅ Performance targets met (<3s audit, <1s status)

---

## Verification Steps

### After Phase 1 (Config Foundation)
```bash
python oracle/project_oracle.py status
python oracle/project_oracle.py audit --quick
python -c "import json; json.load(open('oracle/config/oracle_config.json'))"
```

### After Phase 2 (Memory System)
```bash
python oracle/memory/hippocampus.py search "L6 carousel changes"
python oracle/memory/hippocampus.py benchmark-tokens
```

### After Phase 4 (Bootstrap)
```bash
# Test on current project first
oracle init .

# Then test on other projects
oracle init /path/to/goated-bets-app
```

### End-to-End (Current Project First)
```bash
# Test on THIS project (AutomationScript) first
oracle init .
python oracle/project_oracle.py audit --quick
python oracle/memory/hippocampus.py start
python oracle/memory/hippocampus.py search "recent changes"

# Then test on Goated Bets
cd /path/to/goated-bets-app
oracle init .
python oracle/memory/hippocampus.py search "API changes"
```

---

## Success Criteria for v1.0

### Must Have
1. ✅ Works on current project (AutomationScript) first
2. ✅ Then works on ANY Python project without modification
3. ✅ `oracle init` succeeds on 5+ different project types
4. ✅ Memory system with semantic search operational
5. ✅ No hardcoded paths
6. ✅ Actionable error messages (no silent failures)
7. ✅ Automatic context updates maintain readability
8. ✅ Goated Bets deployment validated
9. ✅ 3 external users onboarded successfully
10. ✅ Documentation complete

### Performance Targets
- <3s for audit --quick
- <1s for status
- <200ms for semantic search

### Timeline
**6-8 weeks** with phases 2-4 running in parallel

---

## Risk Mitigation

1. **Memory performance impact**
   - Mitigation: Async processing, feature flags, caching
   - Fallback: Disable memory if performance degrades

2. **Bootstrap fails on unknown projects**
   - Mitigation: Extensive testing, safe defaults
   - Fallback: Manual config with helper prompts

3. **Breaking current project compatibility**
   - Mitigation: Parallel config system, comprehensive regression tests
   - Fallback: Rollback mechanism via git

---

## Implementation Notes

- Phases 2 (Memory) and 3 (Auto-Updates) can run in parallel
- Phase 4 (Bootstrap) can also run parallel to Phase 3
- **Priority: Get current project working first, then expand**
- Memory system is optional (feature flag)
- Config system is backwards compatible
- Plan to share on GitHub for public use after validation

---

**Next Steps:**
1. Review and approve this plan
2. Begin Phase 1: Config Foundation
3. Document progress in ORACLE_CONTEXT.md Recent Changes
