# Phase E: PresetBuilder Enhancements

**Session:** DB5
**Date:** January 8, 2026
**Status:** Phase A ✅, Phase B ✅, Phase C ✅, Phase D ✅, Phase E Planning

---

## Overview

Enhance PresetBuilder to be the primary preset creation interface with:
1. Tool selection dropdowns (not just layers)
2. Clarified aspect ratio fields
3. G Drive asset integration
4. Remove redundant audio checkbox
5. Add "Animation" output type
6. Preset Reference in both Admin and PresetSelection

---

## E.1: Tool Selection UI

### Goal
Allow users to override default tools for each layer when creating presets.

### Implementation

**File:** `app/frontend/src/components/PresetBuilder.jsx`

Add collapsible "Tool Overrides" section after Layers section:

```jsx
// New state
const [toolCategories, setToolCategories] = useState({});
const [showToolOverrides, setShowToolOverrides] = useState(false);

// Fetch tools on mount (reuse existing admin endpoint, no auth needed for read)
useEffect(() => {
  loadToolCategories();
}, []);

// Map layers to categories
const LAYER_TO_CATEGORY = {
  'L1': 'data_source',
  'L3': 'llm_query',
  'L4': 'tts',
  'L5': 'image_gen',
  'L6': 'animation',
};
```

**UI Design:**
```
┌─ Tool Overrides (Optional) ──────────────────┐
│ Override default tools for specific layers   │
│                                              │
│ L1 Data:  [Default ▼] or [goatedbets_api ▼] │
│ L3 LLM:   [Default ▼] or [perplexity ▼]     │
│ L5 Image: [Default ▼] or [nano_banana ▼]    │
│ L6 Anim:  [Default ▼] or [ken_burns ▼]      │
│                                              │
│ (Only shows categories for selected layers)  │
└──────────────────────────────────────────────┘
```

### Backend Changes

**File:** `app/api/routes/presets.py`

Add public endpoint for tool categories (no admin auth):
```python
@presets_bp.route("/tools/categories", methods=["GET"])
def get_tool_categories_public():
    """Get tool categories for preset builder (public, read-only)"""
    # Return categories with tools list, no sync status
```

### Files to Modify
| File | Changes |
|------|---------|
| `PresetBuilder.jsx` | Add tool override section, fetch categories |
| `PresetBuilder.css` | Style tool override dropdowns |
| `api.js` | Add `getToolCategoriesPublic()` |
| `presets.py` | Add public `/tools/categories` endpoint |

---

## E.2: Clarify Aspect Ratio Fields

### Current State
- `aspect_ratio` = "Working Ratio" (confusing name)
- `final_aspect_ratio` = "Final Output Ratio" (not used in pipeline)

### Clarification
- **aspect_ratio**: The target final aspect ratio for the preset output
- **final_aspect_ratio**: Optional post-processing crop (separate concern)

### Implementation

**File:** `app/frontend/src/components/PresetBuilder.jsx`

**Option A: Same section, clarified labels**
```jsx
<section className="form-section">
  <h3>Aspect Ratio</h3>
  <div className="form-row">
    <div className="form-group">
      <label htmlFor="aspect_ratio">
        Target Ratio
        <span className="field-tooltip" title="The final aspect ratio for your output">ⓘ</span>
      </label>
      <select ...>
    </div>
  </div>

  {/* Collapsible advanced option */}
  <details className="advanced-crop">
    <summary>Post-Processing Crop (Optional)</summary>
    <div className="form-group">
      <label htmlFor="final_aspect_ratio">
        Crop To
        <span className="field-tooltip" title="Optionally crop to a different ratio after generation">ⓘ</span>
      </label>
      <select ...>
    </div>
  </details>
</section>
```

**Option B: Separate sections** (if cleaner)
- Main "Aspect Ratio" section with single dropdown
- "Advanced" section at bottom with post-processing crop option

Going with **Option A** - keeps related settings together but hides complexity.

---

## E.3: G Drive Asset Integration

### Goal
- Configure G Drive folder for assets
- Browse/select assets when creating presets
- Drag-drop UI uploads to G Drive (not server)

### Architecture

```
User's G Drive
└── GoatedBets/
    └── Assets/
        ├── backgrounds/
        ├── logos/
        ├── overlays/
        └── audio/
```

### Backend Implementation

**New File:** `app/services/gdrive_service.py`
```python
class GDriveService:
    def __init__(self, credentials_path: str, folder_id: str):
        """Initialize with service account credentials"""

    def list_assets(self, subfolder: str = None) -> List[Dict]:
        """List files in assets folder"""

    def upload_file(self, file_data: bytes, filename: str, subfolder: str) -> str:
        """Upload file to G Drive, return file ID"""

    def get_download_url(self, file_id: str) -> str:
        """Get temporary download URL for asset"""
```

**New File:** `app/api/routes/assets.py`
```python
@assets_bp.route("/list", methods=["GET"])
def list_assets():
    """List available assets from G Drive"""

@assets_bp.route("/upload", methods=["POST"])
def upload_asset():
    """Upload file to G Drive assets folder"""
```

### Frontend Implementation

**New File:** `app/frontend/src/components/AssetPicker.jsx`
```jsx
function AssetPicker({ onSelect, allowedTypes, subfolder }) {
  // Grid of assets from G Drive
  // Click to select
  // Drag-drop zone to upload new
}
```

**Integrate into PresetBuilder:**
```jsx
<section className="form-section">
  <h3>Assets (Optional)</h3>
  <AssetPicker
    onSelect={(assets) => handleChange('assets', assets)}
    allowedTypes={['image', 'video', 'audio']}
  />
</section>
```

### Configuration

**File:** `config/settings.py` or `.env`
```
GDRIVE_CREDENTIALS_PATH=config/gdrive_service_account.json
GDRIVE_ASSETS_FOLDER_ID=1abc123...
```

### Files to Create/Modify
| File | Action |
|------|--------|
| `app/services/gdrive_service.py` | CREATE - G Drive API wrapper |
| `app/api/routes/assets.py` | CREATE - Asset endpoints |
| `app/api/routes/__init__.py` | MODIFY - Register assets blueprint |
| `app/frontend/src/components/AssetPicker.jsx` | CREATE - Asset browser UI |
| `app/frontend/src/components/AssetPicker.css` | CREATE - Styling |
| `PresetBuilder.jsx` | MODIFY - Add AssetPicker section |
| `api.js` | MODIFY - Add asset API calls |

---

## E.4: Remove Audio Checkbox

### Current State
Lines 592-605 in PresetBuilder.jsx have a separate "Include TTS Audio" checkbox that just toggles L4.

### Change
Remove the checkbox section entirely. Users can click L4 directly in the layers grid.

**File:** `app/frontend/src/components/PresetBuilder.jsx`

Delete:
```jsx
{/* Audio Toggle */}
<section className="form-section">
  <h3>Audio</h3>
  <label className="toggle-label">
    <input
      type="checkbox"
      checked={formData.include_audio}
      onChange={handleAudioToggle}
    />
    <span className="toggle-text">
      Include TTS Audio (adds L4 layer)
    </span>
  </label>
</section>
```

Also remove:
- `include_audio` from formData state
- `handleAudioToggle` function
- References to `include_audio` in AI generation handler

---

## E.5: Add "Animation" Output Type + Reorder

### Current Output Types
```jsx
const OUTPUT_TYPES = [
  { value: 'carousel', label: 'Carousel', icon: '📱' },
  { value: 'single_image', label: 'Single Image', icon: '🖼️' },
  { value: 'infographic', label: 'Infographic', icon: '📊' },
  { value: 'video', label: 'Video', icon: '🎥' },
];
```

### New Order + Animation Type
Reordered by complexity (static → motion):
```jsx
const OUTPUT_TYPES = [
  { value: 'single_image', label: 'Single Image', icon: '🖼️' },
  { value: 'infographic', label: 'Infographic', icon: '📊' },
  { value: 'carousel', label: 'Carousel', icon: '📱' },
  { value: 'animation', label: 'Animation', icon: '✨' },  // NEW
  { value: 'video', label: 'Video', icon: '🎥' },
];
```

### Layer Recommendations
Update `getLayerRecommendation()`:
```jsx
} else if (output_type === 'animation') {
  recommended = ['L1', 'L3', 'L5', 'L6', 'L7'];  // Similar to video but focuses on motion
}
```

### Grid Layout Fix
Currently 4 columns for 4 types. With 5 types:
```css
.output-type-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);  /* Changed from 4 */
  gap: 15px;
}

@media (max-width: 800px) {
  .output-type-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 500px) {
  .output-type-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## E.6: Expandable Preset Cards + Admin Reference Fix

### Goal
- PresetSelection: Expandable cards to show tool details (no separate tab)
- Admin Reference: Convert to card layout (no horizontal scroll)

### PresetSelection: Expandable Cards

**File:** `app/frontend/src/components/PresetSelection.jsx`

Add expand/collapse functionality to existing preset cards:
```jsx
const [expandedPreset, setExpandedPreset] = useState(null);

const handleExpand = (presetId) => {
  setExpandedPreset(expandedPreset === presetId ? null : presetId);
};

// In PresetCard render:
<div className={`preset-card ${expanded ? 'expanded' : ''}`}>
  {/* Existing content: name, type, layers, ratio */}

  <button
    className="expand-btn"
    onClick={() => handleExpand(preset.preset_id)}
  >
    {expanded ? '▲ Less' : '▼ Details'}
  </button>

  {expanded && (
    <div className="preset-details">
      <h5>Tools Used</h5>
      <div className="tool-list">
        {preset.tools?.data_source && (
          <div className="tool-item">
            <span className="tool-cat">Data:</span>
            <span className="tool-name">{preset.tools.data_source}</span>
          </div>
        )}
        {preset.tools?.llm_query && (
          <div className="tool-item">
            <span className="tool-cat">LLM:</span>
            <span className="tool-name">{preset.tools.llm_query}</span>
          </div>
        )}
        {/* etc for tts, image_gen, animation */}
      </div>

      {preset.visual_style && (
        <div className="visual-style">
          <strong>Style:</strong> {preset.visual_style}
        </div>
      )}
    </div>
  )}

  {/* Existing buttons: Select, Customize */}
</div>
```

**CSS Animation:**
```css
.preset-card {
  transition: all 0.3s ease;
}

.preset-card.expanded {
  grid-column: span 2;  /* Expand to double width on desktop */
}

.preset-details {
  animation: slideDown 0.2s ease;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  margin-top: 1rem;
}

@keyframes slideDown {
  from { opacity: 0; max-height: 0; }
  to { opacity: 1; max-height: 200px; }
}
```

### Admin Reference: Card Layout

**File:** `app/frontend/src/components/AdminPresetsReference.jsx`

Convert from table to responsive card grid (no horizontal scroll):
```jsx
<div className="admin-preset-grid">
  {presets.map(preset => (
    <div className="admin-preset-card" key={preset.preset_id}>
      <div className="card-header">
        <h4>{preset.name}</h4>
        <span className="output-badge">{preset.output_type}</span>
      </div>

      <p className="card-desc">{preset.description}</p>

      <div className="card-layers">
        {preset.layers?.map(l => (
          <span className="layer-badge" key={l}>{l}</span>
        ))}
      </div>

      <div className="card-tools">
        <div className="tool-row">
          <span>Data:</span>
          <strong>{preset.tools?.data_source || 'default'}</strong>
        </div>
        <div className="tool-row">
          <span>LLM:</span>
          <strong>{preset.tools?.llm_query || 'default'}</strong>
        </div>
        <div className="tool-row">
          <span>Image:</span>
          <strong>{preset.tools?.image_gen || 'default'}</strong>
        </div>
        {/* Only show if has L4/L6 */}
      </div>

      <div className="card-actions">
        <button onClick={() => handleEdit(preset)}>Edit</button>
        <button onClick={() => handleDelete(preset)}>Delete</button>
      </div>
    </div>
  ))}
</div>
```

### Files to Modify
| File | Action |
|------|--------|
| `PresetSelection.jsx` | MODIFY - Add expandable card logic |
| `PresetSelection.css` | MODIFY - Expanded card styles, animation |
| `AdminPresetsReference.jsx` | MODIFY - Convert table → card grid |
| `AdminPresetsReference.css` | MODIFY - Responsive card styles |

---

## Implementation Order

1. **E.4** - Remove audio checkbox (quick cleanup)
2. **E.5** - Add animation output type (small addition)
3. **E.2** - Clarify aspect ratio labels (small UX fix)
4. **E.1** - Tool selection UI (medium - depends on existing admin endpoint)
5. **E.6** - Preset Reference tabs (medium - UI refactor)
6. **E.3** - G Drive integration (largest - new service + UI)

---

## Verification Checklist

### E.1 Tool Selection
- [ ] Tool dropdowns appear for selected layers only
- [ ] "Default" option uses tool_config.json setting
- [ ] Selected tools saved in preset's `tools` object

### E.2 Aspect Ratio
- [ ] Labels are clear (Generation Ratio, Output Crop)
- [ ] Tooltips explain purpose

### E.3 G Drive Assets
- [ ] Assets list from configured folder
- [ ] Drag-drop uploads to G Drive
- [ ] Selected assets saved with preset

### E.4 Audio Checkbox
- [ ] Checkbox section removed
- [ ] L4 still selectable in layers grid
- [ ] No regression in preset creation

### E.5 Animation Type
- [ ] Fifth output type appears
- [ ] Grid layout doesn't break
- [ ] Layer recommendations work

### E.6 Expandable Cards + Admin Reference
- [ ] Clicking "Details" on preset card expands it
- [ ] Expanded card shows tools used
- [ ] Can still Select/Customize from expanded state
- [ ] Admin Reference uses card grid (no table)
- [ ] No horizontal scroll in either view
- [ ] Admin cards have Edit/Delete buttons
