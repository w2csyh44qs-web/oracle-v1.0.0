# Phase I: PresetBuilder Reorganization + Truth Extension

**Session:** DB7 (continued)
**Date:** January 8, 2026
**Status:** ✅ COMPLETE
**Previous:** Phase G ✅ (truth_prompt_wrapper), Phase H ✅ (Truth Gallery)

---

## COMPACTION RESUME POINT

**Phase I: PresetBuilder UX reorganization with Quick/Advanced modes, Visual/Layout truth dimensions, video config**

---

## Summary

Reorganize PresetBuilder workflow for intuitive content creation:
1. Reference-first approach (assets at top)
2. AI Setup near top (can coordinate with rest of form)
3. Separate Visual and Layout reference systems
4. Quick mode for essential presets, Advanced for full control
5. Video-specific configuration (duration, pacing, voice, platform)
6. Data Source + Aspect Ratio side-by-side in both modes

---

## New Workflow Order

| # | Section | Quick Mode | Advanced Mode |
|---|---------|------------|---------------|
| 1 | Reference Assets (G Drive) | ✅ collapsible | ✅ collapsible |
| 2 | AI-Assisted Setup | ✅ near top | ✅ near top |
| 3 | Basic Info (name, description) | ✅ | ✅ |
| 4 | Visual Style (text) | ✅ | ✅ |
| 5 | Visual Reference (truth) | ❌ | ✅ |
| 6 | Layout Notes (text) | ❌ | ✅ |
| 7 | Layout Reference (truth) | ❌ | ✅ |
| 8 | Output Type (grid) | ✅ | ✅ |
| 9 | Video Config (if video/animation) | ✅ | ✅ |
| 10 | Config (Data Source + Aspect Ratio) | ✅ side-by-side | ✅ side-by-side |
| 11 | Pipeline Layers | ❌ | ✅ |
| 12 | Tool Overrides | ❌ | ✅ collapsible |
| 13 | Submit | ✅ | ✅ |

**Quick Mode includes:** Assets, AI Setup, Basic Info, Visual Style, Output Type, Video Config*, Config (Data Source + Aspect Ratio), Submit
**Advanced Mode adds:** Visual Reference, Layout Notes, Layout Reference, Layers, Tool Overrides

---

## I.1: Quick/Advanced Mode Toggle

**File:** `PresetBuilder.jsx`

**Default:** Remember last choice (localStorage)

```jsx
// Load from localStorage, default to 'quick' for first-time users
const [builderMode, setBuilderMode] = useState(() => {
  return localStorage.getItem('presetBuilderMode') || 'quick';
});

// Persist on change
useEffect(() => {
  localStorage.setItem('presetBuilderMode', builderMode);
}, [builderMode]);

// Top-right toggle
<div className="builder-mode-toggle">
  <button className={builderMode === 'quick' ? 'active' : ''}>Quick</button>
  <button className={builderMode === 'advanced' ? 'active' : ''}>Advanced</button>
</div>

// Conditional sections
{builderMode === 'advanced' && (
  <section>...</section>
)}
```

---

## I.2: Section Reordering

**Current order → New order:**

| Current | New |
|---------|-----|
| AI Setup | 1. Assets (collapsible) |
| Assets | 2. AI Setup (near top) |
| Basic Info + Style + Truth | 3. Basic Info |
| Output Type | 4. Visual Style + Visual Reference |
| Aspect Ratio | 5. Layout Notes + Layout Reference |
| Data Source | 6. Output Type |
| Layers | 7. Video Config (conditional) |
| Tool Overrides | 8. Config (Data Source + Aspect Ratio) |
| Submit | 9. Layers |
|  | 10. Tool Overrides |
|  | 11. Submit |

---

## I.3: Visual/Layout Truth Extension

### Backend Changes

**File:** `app/services/truth_service.py`

Add reference type dimension:
```python
TRUTH_REFERENCE_TYPES = ['visual', 'layout']

# New folder structure:
# Truth/{preset}/visual/yes|no|eh/
# Truth/{preset}/layout/yes|no|eh/

def list_images(self, preset: str, category: str, ref_type: str = 'visual'):
    """List images with reference type support."""

def upload_image(self, preset: str, category: str, file_data, filename, ref_type: str = 'visual'):
    """Upload image with reference type support."""
```

**File:** `app/api/routes/truth.py`

Add `ref_type` parameter to endpoints:
- `GET /truth/sets/<preset>/images?category=yes&ref_type=visual`
- `POST /truth/sets/<preset>/images` (form field: ref_type)

### style_directives.json Schema

**Current:**
```json
{ "cover": "...", "matchup": "...", "bonus": "..." }
```

**New:**
```json
{
  "visual": { "cover": "...", "matchup": "...", "bonus": "..." },
  "layout": { "cover": "...", "matchup": "...", "bonus": "..." }
}
```

### Frontend Changes

**File:** `app/frontend/src/services/api.js`

```javascript
export const getTruthImages = (preset, category = 'yes', refType = 'visual') =>
  api.get(`/truth/sets/${preset}/images`, { params: { category, ref_type: refType } });

export const uploadTruthImage = (preset, file, category = 'yes', refType = 'visual') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('category', category);
  formData.append('ref_type', refType);
  return api.post(...);
};
```

**File:** `TruthGallery.jsx`

Add tabs: Visual References | Layout References

```jsx
const [activeRefType, setActiveRefType] = useState('visual');

<div className="ref-type-tabs">
  <button className={activeRefType === 'visual' ? 'active' : ''}>Visual</button>
  <button className={activeRefType === 'layout' ? 'active' : ''}>Layout</button>
</div>
```

---

## I.4: Layout Notes Field

**File:** `PresetBuilder.jsx`

New form field in formData:
```jsx
const [formData, setFormData] = useState({
  // ...existing
  layout_notes: '',
  visual_truth_set: '',  // renamed from truth_set
  layout_truth_set: '',  // NEW
});
```

Section after Visual Style:
```jsx
{builderMode === 'advanced' && (
  <section className="form-section layout-section">
    <h3>Layout Configuration</h3>
    <div className="form-row">
      <div className="form-group">
        <label>Layout Notes</label>
        <textarea
          value={formData.layout_notes}
          placeholder="Header 20% height, player centered, 10% padding..."
        />
      </div>
      <div className="form-group truth-picker-group">
        <label>Layout Reference</label>
        <TruthPicker type="layout" value={formData.layout_truth_set} />
      </div>
    </div>
  </section>
)}
```

---

## I.5: Video Configuration (Conditional)

**File:** `PresetBuilder.jsx`

New constants:
```jsx
const PACING_PRESETS = [
  { value: 'slow', label: 'Slow (Cinematic)' },
  { value: 'medium', label: 'Medium (Standard)' },
  { value: 'fast', label: 'Fast (Dynamic)' },
];

const PLATFORMS = [
  { value: 'tiktok', label: 'TikTok (9:16)' },
  { value: 'instagram_reels', label: 'Instagram Reels (9:16)' },
  { value: 'youtube_shorts', label: 'YouTube Shorts (9:16)' },
  { value: 'twitter', label: 'Twitter/X (16:9)' },
];

const VOICE_PRESETS = [
  { value: '', label: 'Default' },
  { value: 'energetic_male', label: 'Energetic Male' },
  { value: 'sports_announcer', label: 'Sports Announcer' },
];
```

Conditional section:
```jsx
{['video', 'animation'].includes(formData.output_type) && (
  <section className="video-config-section">
    <h3>Video Settings</h3>
    <div className="form-row">
      <FormGroup label="Duration (sec)" type="number" />
      <FormGroup label="Pacing" type="select" options={PACING_PRESETS} />
    </div>
    <div className="form-row">
      <FormGroup label="Platform" type="select" options={PLATFORMS} />
      {formData.layers.includes('L4') && (
        <FormGroup label="Voice Preset" type="select" options={VOICE_PRESETS} />
      )}
    </div>
    {/* L4 suggestion if not selected */}
    {!formData.layers.includes('L4') && (
      <div className="layer-suggestion">
        Video content typically includes audio.
        <button onClick={() => handleLayerToggle('L4')}>Add L4 (Audio)</button>
      </div>
    )}
  </section>
)}
```

---

## I.6: Data Source + Aspect Ratio Side-by-Side

**File:** `PresetBuilder.jsx`

Move after Layers section, combine into one row:
```jsx
<section className="form-section config-section">
  <h3>Configuration</h3>
  <div className="form-row">
    <div className="form-group">
      <label>Data Source</label>
      <select>...</select>
    </div>
    <div className="form-group">
      <label>Aspect Ratio</label>
      <select>...</select>
    </div>
  </div>
</section>
```

---

## I.7: AI Setup Coordination

Keep AI-Assisted Setup near top (after Assets, before Basic Info).

AI can read and suggest values for fields below it. When user clicks "Generate with AI":
1. AI analyzes selected assets
2. AI suggests name, description, visual style based on assets
3. AI recommends output type based on content
4. User can accept/modify suggestions

```jsx
{/* AI Setup - near top to inform the rest of the form */}
{hasAIProviders && (
  <section className="ai-assist-section">
    <div className="ai-assist-header" onClick={() => setAiExpanded(!aiExpanded)}>
      <h3>AI-Assisted Setup</h3>
      <span className="expand-icon">{aiExpanded ? '−' : '+'}</span>
    </div>
    {aiExpanded && (
      <div className="ai-assist-content">
        <p>Let AI analyze your assets and suggest preset configuration.</p>
        {formData.assets.length > 0 && (
          <div className="ai-asset-preview">
            Analyzing {formData.assets.length} reference asset(s)...
          </div>
        )}
        {/* AI generation controls */}
      </div>
    )}
  </section>
)}
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `PresetBuilder.jsx` | Reorder sections, add mode toggle, video config, layout notes, dual truth pickers |
| `PresetBuilder.css` | Mode toggle, video config, layout section, side-by-side styling |
| `TruthGallery.jsx` | Add Visual/Layout tabs |
| `TruthGallery.css` | Tab styling |
| `api.js` | Add `ref_type` param to truth functions |
| `truth_service.py` | Add reference type folder structure |
| `truth.py` | Add `ref_type` to route params |
| `truth_prompt_wrapper.py` | Update to load both visual and layout directives |

---

## Implementation Order (Backend First)

### Phase I.D: Truth Extension (High Risk - Backend) ← START HERE
1. Update truth_service.py for ref_type dimension
2. Update truth.py routes with ref_type param
3. Update api.js functions with ref_type
4. Add Visual/Layout tabs to TruthGallery
5. Update style_directives.json schema
6. Test full truth workflow end-to-end

### Phase I.A: Quick/Advanced Mode (Low Risk)
1. Add mode state with localStorage persistence
2. Add mode toggle UI
3. Add CSS for toggle
4. Wrap sections with conditional rendering
5. Test mode switching persists

### Phase I.B: Section Reordering (Medium Risk)
1. Reorder JSX sections per new workflow
2. Keep AI Setup near top (after Assets)
3. Combine Data Source + Aspect Ratio side-by-side
4. Add layout notes field
5. Add dual truth pickers (visual + layout)
6. Test form submission

### Phase I.C: Video Configuration (Medium Risk)
1. Add video constants (PACING_PRESETS, PLATFORMS, VOICE_PRESETS)
2. Add conditional video section
3. Add L4 suggestion logic
4. Test with video/animation output types

---

## CSS Additions

```css
/* Mode Toggle */
.builder-mode-toggle { display: flex; gap: 0; justify-content: flex-end; margin-bottom: 20px; }
.mode-btn { padding: 10px 24px; background: var(--bg-tertiary); border: 2px solid var(--bg-tertiary); }
.mode-btn.active { background: var(--goat-purple); border-color: var(--goat-purple); color: white; }

/* Layout Section */
.layout-section { background: linear-gradient(135deg, #1e3a3a 0%, #1a2744 100%); border-left: 4px solid #0d9488; }

/* Video Config */
.video-config-section { background: linear-gradient(135deg, #3a1e5a 0%, #1a1744 100%); border-left: 4px solid #9333ea; }
.layer-suggestion { padding: 12px; background: rgba(245, 158, 11, 0.1); border: 1px dashed var(--goat-gold); }

/* Reference Type Tabs */
.ref-type-tabs { display: flex; border-bottom: 2px solid var(--bg-tertiary); margin-bottom: 20px; }
.ref-tab.active::after { content: ''; position: absolute; bottom: -2px; left: 0; right: 0; height: 2px; background: var(--goat-gold); }
```

---

## Verification Checklist

- [ ] Quick mode shows only essential fields
- [ ] Advanced mode shows all fields
- [ ] Mode toggle persists during session
- [ ] Visual Reference picker works
- [ ] Layout Notes saves to form
- [ ] Layout Reference picker works
- [ ] Video config shows for video/animation types
- [ ] L4 suggestion appears when L4 not selected
- [ ] Data Source + Aspect Ratio side-by-side
- [ ] AI Setup near top analyzes assets
- [ ] TruthGallery has Visual/Layout tabs
- [ ] Backend ref_type parameter works
- [ ] style_directives.json has nested structure
