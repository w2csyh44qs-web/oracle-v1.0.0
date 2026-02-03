# UX Rules Reference - V2 Dashboard-First

**Last Updated:** January 7, 2026
**Purpose:** Consistent UX patterns for the V2 dashboard (primary) and CLI (automation/scripting).

---

## Core Principles

### V2 Dashboard-First Philosophy

1. **Dashboard is Primary** - Web UI for daily content generation
2. **CLI for Automation** - Scripts for batch processing, cron jobs, development
3. **Real-Time Feedback** - SSE progress updates during generation
4. **Guided Flow** - Step-by-step wizard for content creation

### Hierarchy of Interfaces

| Priority | Interface | Use Case |
|----------|-----------|----------|
| 1 | Web Dashboard | Daily content generation, preset browsing, output gallery |
| 2 | CLI Scripts | Batch processing, scheduled automation, development |
| 3 | API Direct | Third-party integrations, custom tooling |

---

## Dashboard UX Patterns

### Primary User Flow

```
Sport Selection → Matchup Selection → Preset Selection → Generation → Output
     (1)               (2)                 (3)              (4)        (5)
```

### Step Navigation

| Element | Implementation |
|---------|----------------|
| **Progress Indicator** | Purple dots, current step highlighted |
| **Back Button** | Always available, returns to previous step |
| **Reset** | Logo click returns to step 1 |
| **Step Labels** | Visible but not clickable (must go sequential) |

### Card Selection Pattern

```css
/* Unselected */
.card { border: 1px solid var(--border-default); }

/* Hover */
.card:hover { border-color: var(--success); background: rgba(34, 197, 94, 0.1); }

/* Selected */
.card.selected { border-color: var(--success); background: rgba(34, 197, 94, 0.15); }
```

**Interaction Rules:**
- Single-click to select
- Click selected card to deselect
- Visual feedback on hover
- Green for selection states

### Button Hierarchy

| Type | Styling | Use Case |
|------|---------|----------|
| **Primary** | Gold background, dark text | Main CTAs: Generate, Create, Save |
| **Secondary** | Purple outline/text | Clone, Customize, Edit |
| **Tertiary** | Text-only with hover | Cancel, Back, Skip |
| **Success** | Green background | Download, Confirm |
| **Danger** | Red background | Delete, Remove |

### Loading States

| State | UI Element |
|-------|------------|
| **Button Loading** | Spinner icon, disabled state, "Generating..." text |
| **Page Loading** | Full-page skeleton or spinner |
| **Inline Loading** | Small spinner next to element |
| **Progress** | Purple progress bar with percentage |

### Toast/Alert Patterns

| Type | Color | Duration |
|------|-------|----------|
| Success | Green | 3s auto-dismiss |
| Error | Red | Manual dismiss required |
| Warning | Gold | 5s auto-dismiss |
| Info | Purple | 3s auto-dismiss |

---

## Generation Flow UX

### SSE Progress Display

```
Generating content...

[=====================----] 68%

Layers:
  L1 Data      ✓ Complete
  L3 Ideas     ✓ Complete
  L5 Media     ⟳ In Progress (3/6 slides)
  L6 Assembly  ○ Pending
  L7 Output    ○ Pending
```

**Progress Rules:**
- Show overall percentage
- List layer status with icons
- Update in real-time via SSE
- Show sub-progress where applicable (slide count)

### Error During Generation

- Don't clear progress - show which step failed
- Offer retry option
- Show error message in context
- Log full error to job details

### Generation Complete

- Auto-navigate to output preview
- Show success toast
- Display generated files with thumbnails
- Offer download individual or batch

---

## Preset Builder UX

### Form Layout

```
┌────────────────────────────────┬──────────────────────────┐
│        Form Inputs             │    Live Preview Panel    │
│  - Output Type                 │                          │
│  - Layer Selection             │    [Preview updates      │
│  - Aspect Ratio                │     as you change        │
│  - Sport                       │     form values]         │
│  - ...                         │                          │
└────────────────────────────────┴──────────────────────────┘
```

### Layer Selection

- Checkboxes with layer descriptions
- L1 always required (locked checked)
- "Apply Recommended" button populates common configs
- Visual layer flow diagram

### Clone/Customize Flow

1. User clicks "Clone" on preset card
2. Modal opens with preset values pre-filled
3. User modifies desired fields
4. Options: "Cancel", "Use Original", "Clone & Use"
5. Cloned preset saved to DB with user ownership

---

## Scheduler UX

### Schedule List

| Column | Content |
|--------|---------|
| Sport | Badge with sport icon |
| Preset | Preset name |
| Schedule | Human-readable cron ("Every Sunday 8am") |
| Next Run | Timestamp or "Paused" |
| Actions | Toggle, Edit, Delete, Run Now |

### Cron Input

- Quick preset buttons: "NFL Sunday", "NBA Daily", "Weekly"
- Manual cron input with validation
- Live preview of next 3 run times
- Error state for invalid cron

---

## Auth UX

### Login Flow

1. Landing shows LoginPage with Google button
2. Click → redirect to Google OAuth
3. Google auth → callback with token
4. Token stored → fetch user info
5. Redirect to dashboard

### Authenticated State

- User avatar in header
- Name displayed
- Admin badge if applicable
- Logout dropdown

### Session Expiry

- Silent token refresh where possible
- Graceful redirect to login on 401
- Preserve intended destination for post-login redirect

---

## Output Gallery UX

### Gallery Grid

- Thumbnails with hover preview
- Filter by: Job, Preset, Sport, Date
- Sort by: Date created, Size, Type
- Batch select for download/delete

### Preview Modal

- Large image/video preview
- Metadata sidebar (job, preset, created date)
- Download button (individual file)
- Navigation arrows for multiple outputs
- Escape to close

---

## Responsive Design

### Breakpoints

| Size | Width | Layout |
|------|-------|--------|
| Mobile | <768px | Single column, stacked |
| Tablet | 768-1024px | 2-column where applicable |
| Desktop | >1024px | Full 3-column layout |

### Mobile Considerations

- Hamburger menu for navigation
- Touch-friendly button sizes (min 44px)
- Stacked cards instead of grid
- Bottom sheet for filters instead of sidebar

---

## CLI UX Patterns (Automation)

### Retained for V2 CLI Scripts

The following patterns apply to `scripts/L0_pipeline.py` and batch automation:

**Checkpoint Pattern:**
```python
print("\n" + "="*80)
print("CHECKPOINT: [Purpose]")
print("="*80)
print("\nOptions:")
print("  [c] Continue")
print("  [v] View details")
print("  [q] Quit")

while True:
    choice = input("\nChoice: ").strip().lower()
    if choice == 'c': break
```

**Menu Design:**
- Single-letter shortcuts: `[c]`, `[v]`, `[q]`
- No "Press Enter to continue"
- Return to menu after sub-actions
- One-handed navigation support

**Layer Transitions:**
```python
print("\n" + "="*80)
print("LAYER X COMPLETE")
print("="*80)
```

### L6 Processor CLI

```bash
# PIL Processor
python3 scripts/_L5/pil_processor.py logo image.jpg --position top-left

# FFmpeg Processor
python3 scripts/_L5/ffmpeg_processor.py kenburns image.jpg --zoom in -d 5
```

---

## Accessibility

### Keyboard Navigation

- Tab through focusable elements
- Enter/Space to activate
- Escape to close modals
- Arrow keys for option lists

### Screen Reader

- Proper heading hierarchy
- Alt text on images
- ARIA labels on interactive elements
- Status announcements for async updates

### Color Contrast

- Text: minimum 4.5:1 ratio
- UI elements: minimum 3:1 ratio
- `--goat-purple-text` (#c4b5fd) for readable purple on dark

---

## Quick Reference

### Color Meanings

| Color | Meaning |
|-------|---------|
| Gold | Primary action, important |
| Purple | UI element, step indicator |
| Green | Selection, success, positive |
| Red | Error, danger, delete |

### Icon Meanings

| Icon | Meaning |
|------|---------|
| ✓ | Complete, success |
| ⟳ | In progress, loading |
| ○ | Pending, not started |
| ✗ | Failed, error |

### State Transitions

```
pending → in_progress → completed
               ↓
            failed
```

---

*This document defines UX patterns for the V2 Media Engine. Dashboard is primary, CLI is for automation.*
