# Dashboard Navigation & Preset Visibility Fixes

**Session:** DB8c
**Date:** January 19, 2026
**Status:** COMPLETE

---

## Problems to Solve

1. **Preset not showing after creation** - User created preset from dashboard, can't find it in list
2. **No Home button** - Can't navigate back to media engine from other pages
3. **No icons on nav buttons** - Gallery, Schedules, Admin lack visual indicators
4. **No skip option on Sport Selection** - Must select sport before seeing presets
5. **Missing back buttons** - Some pages lack navigation (GenerationComplete, TruthGallery)

---

## Root Cause Analysis

### 1. Preset Visibility Issue

**Root cause:** The `dev_user` fallback creates invalid user_id references.

In `app/api/routes/presets.py` (lines 67-69):
```python
# Allow anonymous preset creation in development (use 'dev_user' as placeholder)
if not user_id:
    user_id = "dev_user"
```

**Problems:**
- `"dev_user"` is a string, but DB expects integer user_id
- User presets with string user_id won't match when querying by actual Google user_id
- The `preset_service.py` query filters by `user_id=user_id` - type mismatch

**Solution:** Remove `dev_user` fallback. User is always authenticated via Google OAuth.

### 2. Navigation Issues

- No Home button to return to media engine
- Some pages lack back buttons (GenerationComplete, TruthGallery)
- Nav buttons are text-only (no icons)

### 3. No Skip on Sport Selection

SportSelection requires sport selection before proceeding.
User wants job-based (preset-first) workflow for non-matchup content.

---

## Implementation Plan

### Phase 1: Fix Preset Visibility (Backend)

**Files:**
- `app/api/routes/presets.py`

**Changes:**
1. Remove `dev_user` fallback - require authentication
2. Return 401 if user not authenticated for preset creation

```python
@presets_bp.route("", methods=["POST"])
def create_preset():
    """Create a new custom preset."""
    data = request.get_json()
    user_id = get_current_user_id()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Require authentication - no dev_user fallback
    if not user_id:
        return jsonify({"error": "Authentication required to create presets"}), 401

    required = ["name", "output_type"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    try:
        preset = PresetService.create_preset(data, user_id)
        return jsonify({
            "message": "Preset created",
            **preset.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Phase 2: Add Home Button + Icons to Navigation

**Files:**
- `app/frontend/src/App.jsx`
- `app/frontend/src/styles/App.css`

**Changes to UserProfile component:**

```jsx
function UserProfile({ onHome, onScheduler, onGallery, onAdmin }) {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <div className="user-profile">
      <button onClick={onHome} className="nav-btn home-nav-btn">
        <span className="nav-icon">🏠</span>
        <span>Home</span>
      </button>
      <button onClick={onGallery} className="nav-btn gallery-nav-btn">
        <span className="nav-icon">🖼️</span>
        <span>Gallery</span>
      </button>
      <button onClick={onScheduler} className="nav-btn scheduler-nav-btn">
        <span className="nav-icon">📅</span>
        <span>Schedules</span>
      </button>
      {user.role === 'admin' && (
        <button onClick={onAdmin} className="nav-btn admin-nav-btn">
          <span className="nav-icon">⚙️</span>
          <span>Admin</span>
        </button>
      )}
      {user.picture_url && (
        <img src={user.picture_url} alt={user.name} className="user-avatar" />
      )}
      <div className="user-info">
        <span className="user-name">{user.name}</span>
        {user.role === 'admin' && <span className="admin-badge">Admin</span>}
      </div>
      <button onClick={logout} className="logout-btn">
        Logout
      </button>
    </div>
  );
}
```

**Update all UserProfile usages to pass onHome:**
```jsx
<UserProfile
  onHome={() => { resetSelection(); setCurrentPage('generator'); }}
  onScheduler={() => setCurrentPage('scheduler')}
  onGallery={() => setCurrentPage('gallery')}
  onAdmin={() => setCurrentPage('admin')}
/>
```

**CSS additions:**
```css
.nav-btn {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-icon {
  font-size: 1.1rem;
}

.home-nav-btn {
  border-color: #22c55e;
  color: #22c55e;
}

.home-nav-btn:hover {
  background: rgba(34, 197, 94, 0.1);
}
```

### Phase 3: Add Back Buttons to Missing Pages

**Files:**
- `app/frontend/src/components/GenerationFlow.jsx` - Add back button on completion state
- `app/frontend/src/components/TruthGallery.jsx` - Add back button

**GenerationFlow - completion state:**
The completion state already has a "Start New" button which calls `resetSelection()`. This effectively acts as a home button.

**TruthGallery:**
Currently embedded in Admin tabs - the Admin tab navigation handles this. No change needed.

### Phase 4: Add Skip Link to Sport Selection

**Files:**
- `app/frontend/src/components/SportSelection.jsx`
- `app/frontend/src/components/SportSelection.css`

**Add skip link after sport grid:**
```jsx
return (
  <div className="sport-selection">
    <h2 className="section-title">Select a Sport</h2>
    <div className="sport-grid">
      {sports.map((sport) => (
        <button
          key={sport.id}
          className="sport-card"
          onClick={() => handleSelectSport(sport)}
          style={{ borderColor: sport.color }}
        >
          {/* existing card content */}
        </button>
      ))}
    </div>

    {/* Skip link for job-based workflow */}
    <div className="skip-section">
      <span className="skip-text">or</span>
      <button
        className="skip-link"
        onClick={() => setCurrentStep(3)}
      >
        Skip to Presets →
      </button>
      <span className="skip-hint">For non-matchup content (banners, promos, etc.)</span>
    </div>
  </div>
);
```

**CSS:**
```css
.skip-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--bg-tertiary, #2d3748);
}

.skip-text {
  color: var(--text-muted, #718096);
  font-size: 0.9rem;
}

.skip-link {
  background: transparent;
  border: none;
  color: var(--goat-gold, #f59e0b);
  font-size: 0.95rem;
  cursor: pointer;
  text-decoration: underline;
  transition: opacity 0.2s;
}

.skip-link:hover {
  opacity: 0.8;
}

.skip-hint {
  color: var(--text-muted, #718096);
  font-size: 0.8rem;
}
```

---

## Critical Files Summary

| File | Changes |
|------|---------|
| `app/api/routes/presets.py` | Remove dev_user fallback, require auth |
| `app/frontend/src/App.jsx` | Add Home button with icon, add onHome prop, icons on all nav buttons |
| `app/frontend/src/styles/App.css` | Nav icon styling, home button color |
| `app/frontend/src/components/SportSelection.jsx` | Add skip link to presets |
| `app/frontend/src/components/SportSelection.css` | Skip section styling |

---

## Verification Plan

1. **Preset Visibility**
   - Login to dashboard (Google OAuth)
   - Create a new preset in PresetBuilder
   - Navigate to PresetSelection
   - Verify the new preset appears in the list

2. **Home Button**
   - Navigate to Gallery → Click Home → Should return to step 1
   - Navigate to Schedules → Click Home → Should return to step 1
   - Navigate to Admin → Click Home → Should return to step 1
   - Verify icons display on all nav buttons

3. **Skip Link**
   - Load dashboard → See "Skip to Presets" link below sport cards
   - Click skip → Should go directly to PresetSelection (step 3)
   - Select a manual-input preset → Should proceed to GenerationFlow
