# Phase H: Dashboard Truth Gallery

**Session:** DB7
**Date:** January 8, 2026
**Status:** In Progress
**Previous:** Phase A-G Complete

---

## Overview

Implement a Truth Gallery system for managing visual style references with:
1. Separate Truth Gallery page for full management (upload, organize, AI extract, save)
2. PresetBuilder integration with quick truth picker
3. Per-preset truth reference linking
4. G Drive storage (primary) + local fallback
5. AI-assisted style extraction via Claude Vision

---

## Background

The `truth_prompt_wrapper.py` was restored in Phase G with static style directives derived from analyzing TB @ CAR carousel artwork. Phase H makes this dynamic by:
- Allowing users to upload/manage reference images
- Using Claude Vision to analyze approved images
- Storing extracted style directives per-preset
- Loading directives dynamically at generation time

---

## Architecture

```
Truth Gallery Page          PresetBuilder
─────────────────          ──────────────
[Full truth management]    [Quick picker]
├── Upload images           ├── Truth Reference: [carousel_sketch ▼]
├── Organize yes/no/eh      ├── [Preview thumbs]
├── Enter notes             └── [Edit in Gallery →]
├── AI extract
└── Save directives
         │
         └──→ GoatedBets/Truth/{preset}/style_directives.json
                      │
                      └──→ Used by prompt_builders.py at generation time
```

---

## Storage Architecture

**G Drive (Primary - shared):**
```
GoatedBets/
├── Assets/
├── Outputs/
└── Truth/                    ← NEW folder
    ├── carousel_sketch/
    │   ├── yes/
    │   ├── no/
    │   ├── eh/
    │   └── style_directives.json
    ├── dark_incentives/
    └── ...
```

**Local (Personal - backup):**
```
content/truth/                ← Existing folder
├── carousel_illustrated/     (maps to carousel_sketch)
└── ...
```

**Lookup Priority:**
1. G Drive Truth/{preset}/ (shared, authoritative)
2. Local content/truth/{preset}/ (personal fallback)
3. Hardcoded defaults in truth_prompt_wrapper.py

---

## H.1: Backend Service

**New File:** `app/services/truth_service.py`

```python
class TruthService:
    """Manages truth references via G Drive (primary) + local fallback."""

    def __init__(self, gdrive_service: GDriveService):
        self.gdrive = gdrive_service
        self.local_base = "content/truth"

    def list_truth_sets(self) -> List[Dict]:
        """List all truth sets from G Drive + local.
        Returns: [{ id, name, source, yes_count, has_directives }]
        """

    def list_images(self, preset: str, category: str) -> List[Dict]:
        """List images from G Drive Truth/{preset}/{category}/
        Falls back to local if G Drive unavailable.
        Returns: [{ id, name, url, source }]
        """

    def upload_image(self, preset: str, category: str, file) -> Dict:
        """Upload to G Drive Truth/{preset}/{category}/"""

    def move_image(self, preset: str, image_id: str, from_cat: str, to_cat: str) -> bool:
        """Move image between categories (e.g., eh -> yes)"""

    def delete_image(self, preset: str, category: str, image_id: str) -> bool:
        """Delete image from G Drive"""

    def extract_style_with_vision(self, preset: str, user_notes: str) -> Dict:
        """Download 'yes' images from G Drive, analyze with Claude Vision.
        Combines AI analysis with user notes.
        Returns: { cover: str, matchup: str, bonus: str }
        """

    def save_style_directives(self, preset: str, directives: Dict) -> bool:
        """Save to G Drive Truth/{preset}/style_directives.json"""

    def get_style_directives(self, preset: str) -> Dict:
        """Load directives: G Drive first, local fallback, hardcoded defaults."""

    def create_truth_set(self, preset: str) -> bool:
        """Create new truth set folder structure in G Drive"""
```

---

## H.2: API Routes

**New File:** `app/api/routes/truth.py`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/truth/sets` | List all truth sets |
| POST | `/truth/sets` | Create new truth set |
| GET | `/truth/sets/<preset>` | Get truth set details |
| DELETE | `/truth/sets/<preset>` | Delete truth set |
| GET | `/truth/sets/<preset>/images` | List images (query: category) |
| POST | `/truth/sets/<preset>/images` | Upload image |
| PUT | `/truth/sets/<preset>/images/<id>/move` | Move image to category |
| DELETE | `/truth/sets/<preset>/images/<id>` | Delete image |
| GET | `/truth/sets/<preset>/directives` | Get style directives |
| PUT | `/truth/sets/<preset>/directives` | Save directives |
| POST | `/truth/sets/<preset>/extract` | AI extract (body: user_notes) |

---

## H.3: Truth Gallery Page

**New File:** `app/frontend/src/components/TruthGallery.jsx`

Full-page component for managing truth references:

```
┌─────────────────────────────────────────────────────────────┐
│ Truth Gallery - Style Reference Management                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Preset: [carousel_sketch ▼]    [+ Create New Truth Set]    │
│                                                             │
│ ┌─── YES (Approved) ──────────────────────────────────────┐ │
│ │ [img] [img] [img]                    [+ Upload]         │ │
│ │  ☑      ☑                                               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─── NO (Avoid) ──────────────────────────────────────────┐ │
│ │ [img] [img]                          [+ Upload]         │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─── EH (Borderline) ─────────────────────────────────────┐ │
│ │ [img]                                [+ Upload]         │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ═══════════════════════════════════════════════════════════ │
│                                                             │
│ Style Extraction                                            │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Your Notes (what you like about the YES images):        │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ The ink splatters should have visible drips running │ │ │
│ │ │ down. Player poses should be dynamic, not static... │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ [Analyze with Claude Vision]                           │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─── Extracted Style Directives ──────────────────────────┐ │
│ │ COVER:                                                  │ │
│ │ - INK SPLATTER CLOUD with VISIBLE DRIPS behind player  │ │
│ │ - Small ink droplets scattered around edges            │ │
│ │                                                         │ │
│ │ MATCHUP:                                                │ │
│ │ - Column helmets: SUBTLE wash (30% intensity)          │ │
│ │ - Winner section: DRAMATIC paint explosion (100%)      │ │
│ │                                                         │ │
│ │ [Edit]  [Save]  [Re-extract]                           │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Drag-drop image upload to any category
- Click image to view full size in modal
- Drag image between categories to reclassify
- Select multiple images for bulk operations
- Real-time sync status indicator for G Drive

---

## H.4: PresetBuilder Truth Picker

**Modify:** `app/frontend/src/components/PresetBuilder.jsx`

Add truth reference section below visual style:

```jsx
{/* Truth Reference Section */}
<section className="form-section">
  <h3>Style Reference</h3>
  <p className="section-hint">
    Link this preset to approved reference images for consistent style
  </p>

  <div className="truth-picker">
    <select
      value={formData.truth_set}
      onChange={(e) => handleChange('truth_set', e.target.value)}
    >
      <option value="">None (use default style)</option>
      {truthSets.map(set => (
        <option key={set.id} value={set.id}>{set.name}</option>
      ))}
    </select>

    {formData.truth_set && (
      <div className="truth-preview">
        <div className="truth-thumbs">
          {truthThumbs.map(img => (
            <img key={img.id} src={img.url} alt="Reference" />
          ))}
        </div>
        <Link to={`/truth/${formData.truth_set}`}>
          Edit in Gallery
        </Link>
      </div>
    )}
  </div>
</section>
```

---

## H.5: Dynamic Style Loading

**Modify:** `app/core/pipeline/layers/_L3/processors/truth_prompt_wrapper.py`

```python
import os
import json
from typing import Dict, Optional

# Default styles (fallback) - existing constants
DEFAULT_STYLES = {
    "carousel_sketch": {
        "cover": TRUTH_STYLE_COVER,
        "matchup": TRUTH_STYLE_MATCHUP,
        "bonus": TRUTH_STYLE_BONUS
    }
}

def load_style_directives(preset: str) -> Dict[str, str]:
    """Load style directives, preferring saved over defaults.

    Priority:
    1. G Drive Truth/{preset}/style_directives.json (via local sync)
    2. Local content/truth/{preset}/style_directives.json
    3. Hardcoded defaults
    """
    # Check local truth folder (synced from G Drive or local backup)
    local_paths = [
        f"content/truth/{preset}/style_directives.json",
        f"content/truth/{preset.replace('_', '-')}/style_directives.json",
    ]

    for style_file in local_paths:
        if os.path.exists(style_file):
            try:
                with open(style_file) as f:
                    saved = json.load(f)
                    return {
                        "cover": saved.get("cover", ""),
                        "matchup": saved.get("matchup", ""),
                        "bonus": saved.get("bonus", "")
                    }
            except (json.JSONDecodeError, IOError):
                pass

    # Fall back to hardcoded defaults
    return DEFAULT_STYLES.get(preset, DEFAULT_STYLES.get("carousel_sketch", {}))


def wrap_carousel_prompts(prompts: Dict[str, str], preset: str = "carousel_sketch") -> Dict[str, str]:
    """Wrap prompts with style directives from truth set."""
    styles = load_style_directives(preset)

    if not styles:
        return prompts

    return {
        'cover': wrap_cover_prompt(prompts.get('cover', ''), styles.get('cover', TRUTH_STYLE_COVER)),
        'matchup': wrap_matchup_prompt(prompts.get('matchup', ''), styles.get('matchup', TRUTH_STYLE_MATCHUP)),
        'bonus': wrap_bonus_prompt(prompts.get('bonus', ''), styles.get('bonus', TRUTH_STYLE_BONUS))
    }
```

---

## H.6: GDrive Service Extension

**Modify:** `app/services/gdrive_service.py`

Add Truth folder methods:

```python
class GDriveService:
    # ... existing methods ...

    def get_truth_folder_id(self) -> Optional[str]:
        """Get or create Truth folder under GoatedBets root"""

    def list_truth_sets(self) -> List[Dict]:
        """List all folders in GoatedBets/Truth/"""

    def create_truth_set(self, preset: str) -> str:
        """Create Truth/{preset}/ with yes/no/eh subfolders"""

    def list_truth_images(self, preset: str, category: str) -> List[Dict]:
        """List images in Truth/{preset}/{category}/"""

    def upload_truth_image(self, preset: str, category: str, file_data: bytes, filename: str) -> Dict:
        """Upload image to Truth/{preset}/{category}/"""

    def move_truth_image(self, preset: str, image_id: str, to_category: str) -> bool:
        """Move image to different category folder"""

    def get_truth_directives(self, preset: str) -> Optional[Dict]:
        """Read style_directives.json from Truth/{preset}/"""

    def save_truth_directives(self, preset: str, directives: Dict) -> bool:
        """Write style_directives.json to Truth/{preset}/"""
```

---

## Files to Create/Modify

| File | Action | Priority |
|------|--------|----------|
| `app/services/truth_service.py` | CREATE | H.1 |
| `app/services/gdrive_service.py` | MODIFY | H.1 |
| `app/api/routes/truth.py` | CREATE | H.2 |
| `app/api/routes/__init__.py` | MODIFY | H.2 |
| `app/frontend/src/components/TruthGallery.jsx` | CREATE | H.3 |
| `app/frontend/src/components/TruthGallery.css` | CREATE | H.3 |
| `app/frontend/src/App.jsx` | MODIFY | H.3 |
| `app/frontend/src/utils/api.js` | MODIFY | H.3 |
| `app/frontend/src/components/PresetBuilder.jsx` | MODIFY | H.4 |
| `app/frontend/src/components/PresetBuilder.css` | MODIFY | H.4 |
| `app/core/pipeline/layers/_L3/processors/truth_prompt_wrapper.py` | MODIFY | H.5 |

---

## Implementation Order

1. **H.1** - Backend truth service + GDrive extension
2. **H.2** - Truth API routes
3. **H.3** - Truth Gallery page (full UI)
4. **H.4** - PresetBuilder truth picker
5. **H.5** - Dynamic style loading in prompt wrapper

---

## G Drive Setup (Manual)

Create folder structure in G Drive:
```
GoatedBets/
└── Truth/
    └── carousel_sketch/
        ├── yes/
        ├── no/
        └── eh/
```

The service will auto-create subfolders as needed.

---

## Claude Vision Integration

For style extraction, the service will:
1. Download all images from `yes/` folder
2. Send to Claude Vision API with prompt:
   ```
   Analyze these reference images for a sports betting carousel.
   Focus on:
   - Ink splatter/watercolor effects (intensity, placement, drip patterns)
   - Player rendering style (brushwork, line weight, sketch quality)
   - Color application (saturation, bleeding, texture)
   - Visual hierarchy between elements

   User notes: {user_notes}

   Output style directives for: COVER, MATCHUP, BONUS sections
   ```
3. Parse response into structured directives
4. Allow user to edit before saving

---

## Verification Checklist

### H.1 Backend Service
- [ ] TruthService initializes with GDriveService
- [ ] list_truth_sets returns G Drive + local sets
- [ ] upload/delete/move operations work
- [ ] extract_style_with_vision calls Claude API

### H.2 API Routes
- [ ] All endpoints return proper JSON
- [ ] Error handling for missing presets
- [ ] File upload works with multipart form

### H.3 Truth Gallery Page
- [ ] Loads truth sets on mount
- [ ] Displays images in correct categories
- [ ] Upload works (drag-drop + click)
- [ ] AI extraction shows loading state
- [ ] Directives editable and saveable

### H.4 PresetBuilder Integration
- [ ] Truth picker dropdown populated
- [ ] Thumbnail previews load
- [ ] Link to gallery works

### H.5 Dynamic Loading
- [ ] Reads from local style_directives.json
- [ ] Falls back to hardcoded defaults
- [ ] Prompts include loaded directives
