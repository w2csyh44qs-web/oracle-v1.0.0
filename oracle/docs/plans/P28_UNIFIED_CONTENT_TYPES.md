# P28: Content Preset Validator

**Status:** Draft
**Created:** January 18, 2026
**Session:** D107

---

## Problem

Content presets in `script_presets.json` can be incomplete - missing `display_mode`, `visual_style`, or other layer-required fields. There's no way to check if a preset will work end-to-end without running the pipeline.

---

## Solution

Add a **validation layer** that checks if a preset has all required fields for the layers it touches. Keep the existing preset structure - no new JSON format.

---

## Files to Create

### 1. `config/preset_validator.py`

```python
"""
Preset Validator - Ensures content presets have all required fields.

Usage:
    python -m config.preset_validator              # Validate all presets
    python -m config.preset_validator carousel_sketch  # Validate one preset

Checks:
    - Required fields present (display_mode, visual_style, etc.)
    - Referenced presets exist (voice_preset -> voice_presets, pacing_preset -> pacing_presets)
    - Layer requirements met based on display_mode routing
"""

from typing import Dict, List, Tuple
from pathlib import Path
import json

# Required fields by layer
LAYER_REQUIREMENTS = {
    "L3": ["prompt_template", "tone", "format"],
    "L4": ["voice_preset"],  # Only if has_audio
    "L5": ["display_mode", "visual_style"],
    "L6": ["display_mode", "pacing_preset"],
    "L7": []  # No required fields
}

# Optional fields that trigger warnings if missing
RECOMMENDED_FIELDS = {
    "L3": ["preferred_model", "output_type"],
    "L5": ["tools.image_gen"],
    "L6": ["tools.animation"]
}


class PresetValidator:
    def __init__(self):
        self.script_presets = self._load_json("config/script_presets.json")
        self.display_modes = self._load_display_modes()

    def validate_preset(self, preset_name: str) -> Dict:
        """Validate a single preset. Returns {valid, errors, warnings}."""
        ...

    def validate_all(self) -> Dict[str, Dict]:
        """Validate all presets."""
        ...

# Singleton
preset_validator = PresetValidator()
```

---

## How It Works

1. **Load preset** from `script_presets.json`
2. **Determine layers** from `display_mode` (via `display_modes.py`)
3. **Check required fields** for each layer the preset touches
4. **Check references** (voice_preset, pacing_preset exist)
5. **Report errors/warnings**

---

## Required Field Definitions

| Layer | Required Fields | Condition |
|-------|----------------|-----------|
| L3 | `prompt_template`, `tone`, `format` | Always |
| L4 | `voice_preset` | Only if `has_audio(display_mode)` |
| L5 | `display_mode`, `visual_style` | Always |
| L6 | `display_mode`, `pacing_preset` | Always |
| L7 | (none) | Always |

---

## CLI Usage

```bash
# Validate all presets
python -m config.preset_validator

# Output:
# OK carousel_illustrated
# OK sketch_insights_carousel
# WARN best_bets_game
#   WARN: L5: Missing recommended field 'tools.image_gen'
# FAIL pokemon_battle_animated
#   ERROR: L6: Missing required field 'pacing_preset'

# Validate single preset
python -m config.preset_validator carousel_illustrated
```

---

## Integration Points

### Optional: Add to Pipeline

Add validation check before L3 runs:

```python
# In L3_ideas.py
from config.preset_validator import PresetValidator

validator = PresetValidator()
result = validator.validate_preset(content_preset)
if not result["valid"]:
    print(f"Preset validation failed:")
    for err in result["errors"]:
        print(f"  {err}")
    sys.exit(1)
```

### Optional: Add to Oracle health check

```bash
python3 oracle/project_oracle.py audit --quick
# Now includes preset validation
```

---

## Verification

1. Run validator on existing presets:
   ```bash
   python -m config.preset_validator
   ```

2. Fix any FAIL results by adding missing fields to `script_presets.json`

3. Test a preset end-to-end:
   ```bash
   python3 app/core/pipeline/layers/_L3/L3_ideas.py playoffs wild_card \
     --matchup "DEN @ BUF" --content-preset carousel_illustrated --no-checkpoint
   ```

---

## Benefits Over Unified Format

- **No migration needed** - existing presets stay as-is
- **No redundancy** - presets can share referenced sub-presets
- **Adjustable** - edit one file, validator confirms it's still valid
- **Incremental** - add validation rules as needed
