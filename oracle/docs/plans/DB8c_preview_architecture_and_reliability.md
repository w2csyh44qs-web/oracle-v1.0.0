# Preview-Driven Architecture & Pipeline Reliability Overhaul

**Session:** DB8c Extended
**Date:** January 29, 2026
**Status:** PLANNING
**Scope:** Major architectural enhancement + critical reliability fixes

---

## Executive Summary

Transform the Media Engine into a **Google AI Studio-like workflow** with instant browser-based previews, while simultaneously fixing 40+ critical reliability issues in the L1-L6 pipeline. This dual-path approach enables rapid iteration (2-5 second previews) before committing to production renders (30-60 seconds).

**Key Innovation**: Pause pipeline at L5, generate browser preview using RecordRTC + html2canvas, only run expensive L6 MoviePy rendering after user approval.

**Timeline**: 6-8 weeks (4 weeks reliability fixes, 3-4 weeks preview architecture)

---

## Current State Analysis

### Problems Identified

#### 1. **UX/Workflow Issues**
- ❌ User waits 2-5 minutes with zero visual feedback until L6 completes
- ❌ Font/layout issues only discovered after full pipeline run
- ❌ Must re-run entire L1-L6 to fix minor text adjustments
- ❌ No way to preview before committing API costs
- ❌ Static mockup in PresetPreview.jsx (not actual content)

#### 2. **Critical Reliability Issues** (From comprehensive audit)
- ❌ **40+ bare exception handlers** that swallow errors silently
- ❌ **No input validation** on API responses (L1) or layer outputs (L3-L5)
- ❌ **No retry logic** for external APIs (GoatedBets, BallDontLie, AI services)
- ❌ **Thread-unsafe global state** in L3 ideas.py (MCP games cache)
- ❌ **FFmpeg subprocess failures** fail silently without logging
- ❌ **MoviePy TextClip hangs** on font loading (no timeout)
- ❌ **Missing error context** - generic "Exception" messages with no traceback
- ❌ **Hardcoded paths** (ImageMagick at /opt/homebrew/bin/convert)
- ❌ **No data validation between layers** (L1→L3, L3→L4, L4→L5, L5→L6)
- ❌ **File system race conditions** (no atomic writes, no locking)

#### 3. **Architecture Gaps**
- No preview generation at any pipeline stage
- No intermediate outputs accessible to frontend
- Polling-based progress (2s intervals) instead of streaming
- No way to apply adjustments without full re-run
- No quality validation on generated outputs

---

## Proposed Architecture: Dual-Path Preview System

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER WORKFLOW (Google AI Studio Style)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Configure Preset (PresetBuilder)                        │
│          ↓                                                  │
│  2. Click "Generate Preview"                                │
│          ↓                                                  │
│  ┌──────────────────────────────────────────┐              │
│  │ BACKEND: Run L1-L5 (Fast Path)           │              │
│  │ • L1: Data (5s)                           │              │
│  │ • L2: Calendar (2s)                       │              │
│  │ • L3: Ideas (10s)                         │              │
│  │ • L4: Audio + Timing (15s)                │              │
│  │ • L5: Media Generation (30s)              │              │
│  │ ⏸  PAUSE HERE (preview_mode=true)        │              │
│  └──────────────┬───────────────────────────┘              │
│                 ↓                                           │
│  ┌──────────────────────────────────────────┐              │
│  │ FRONTEND: Browser Preview (2-5s)         │              │
│  │ • Fetch L4 timing + L5 media             │              │
│  │ • Render frames in DOM (PreviewCanvas)   │              │
│  │ • Capture with html2canvas (1080x1920)   │              │
│  │ • Record with RecordRTC (WebM/VP9)       │              │
│  │ • Mix audio from L4 (Web Audio API)      │              │
│  │ • Show preview in player                 │              │
│  └──────────────┬───────────────────────────┘              │
│                 ↓                                           │
│         ┌───────┴────────┐                                 │
│         │                │                                 │
│    [Adjust] ←──┐    [Approve]                             │
│         │      │         │                                 │
│         ↓      │         ↓                                 │
│    Re-render   │  ┌─────────────────────┐                 │
│    preview ────┘  │ BACKEND: Run L6     │                 │
│    (instant)      │ MoviePy + FFmpeg    │                 │
│                   │ Production quality  │                 │
│                   │ (30-60 seconds)     │                 │
│                   └──────────┬──────────┘                 │
│                              ↓                             │
│                   Download final_1080p.mp4                │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Browser Preview Path**:
- **RecordRTC** (5.6.2) - Browser-based video recording
- **html2canvas** (1.4.1) - DOM to canvas capture
- **Web Audio API** - Audio sync and mixing
- **Canvas API** - Frame composition
- **CSS Animations** - Ken Burns effects

**Server Production Path** (unchanged):
- **MoviePy** - Video composition
- **FFmpeg** - Final encoding
- **PIL/Pillow** - Image processing

---

## Phase 1: Critical Reliability Fixes (MUST DO FIRST)

**Timeline**: 3-4 weeks
**Why First**: Preview system is useless if pipeline fails 30% of the time

### 1.1 Exception Handling Overhaul

**Problem**: 40+ bare `except:` blocks silently fail

**Solution**: Replace all with specific exceptions + structured logging

**Files to Fix** (Priority Order):
```python
# TIER 1 - CRITICAL
app/core/pipeline/layers/_L6/L6_assembly.py          # 7 bare excepts
app/core/pipeline/layers/_L5/L5_media.py             # 8 bare excepts
app/core/pipeline/layers/_L4/L4_audio.py             # 5 bare excepts
app/core/pipeline/layers/_L3/L3_ideas.py             # 3 bare excepts
app/core/pipeline/layers/_L2/L2_calendar.py          # 1 bare except
app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py
app/core/pipeline/layers/_L6/processors/comfyui_processor.py

# TIER 2 - HIGH
app/core/pipeline/layers/_L1/inputs/goatedbets_api.py
app/core/pipeline/layers/_L1/inputs/balldontlie_api.py
app/core/pipeline/layers/_L7/L7_distribution.py      # 5 bare excepts
```

**Implementation Pattern**:
```python
# BEFORE (current)
try:
    result = some_operation()
except:
    pass  # Silent failure!

# AFTER (fixed)
try:
    result = some_operation()
except FileNotFoundError as e:
    logger.error(f"File not found in {operation}: {e}", exc_info=True)
    raise PipelineError(f"Missing required file: {e.filename}")
except subprocess.CalledProcessError as e:
    logger.error(f"Subprocess failed: {e.stderr[:500]}", exc_info=True)
    raise PipelineError(f"FFmpeg encoding failed: {e.stderr[:200]}")
except Exception as e:
    logger.error(f"Unexpected error in {operation}: {e}", exc_info=True)
    raise
```

### 1.2 Input Validation Layer

**Problem**: No validation on API responses or layer outputs

**Solution**: Pydantic schemas for all data contracts

**Files to Create**:
```
app/core/pipeline/schemas/
├── __init__.py
├── l1_schemas.py      # NormalizedMatchup, TeamData, PropData
├── l2_schemas.py      # CalendarConfig, SegmentData
├── l3_schemas.py      # IdeaPackage, ScriptStructure
├── l4_schemas.py      # AudioMetadata, TimingData
├── l5_schemas.py      # MediaPackage, AssetMetadata
└── l6_schemas.py      # AssemblyResult, OutputFile
```

**Example Schema**:
```python
# app/core/pipeline/schemas/l1_schemas.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class PropData(BaseModel):
    player_name: str
    team: str
    stat_type: str
    line: float
    over_odds: Optional[int]
    under_odds: Optional[int]

    @validator('line')
    def validate_line(cls, v):
        if v <= 0:
            raise ValueError('Prop line must be positive')
        return v

class NormalizedMatchup(BaseModel):
    matchup_id: str
    sport: str
    away_team: str
    home_team: str
    game_time: str
    props: List[PropData] = Field(default_factory=list)

    @validator('props')
    def validate_props_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Matchup must have at least one prop')
        return v
```

**Usage in Pipeline**:
```python
# L1 output validation
from app.core.pipeline.schemas.l1_schemas import NormalizedMatchup

def fetch_matchup_data(matchup_id):
    raw_data = api.get_matchup(matchup_id)

    # Validate with Pydantic
    try:
        validated = NormalizedMatchup(**raw_data)
    except ValidationError as e:
        logger.error(f"L1 output validation failed: {e}")
        raise PipelineError(f"Invalid matchup data: {e}")

    return validated
```

### 1.3 Retry Logic with Exponential Backoff

**Problem**: API timeouts fail immediately (no retries)

**Solution**: Implement retry decorator with exponential backoff

**File to Create**: `app/core/utils/retry_utils.py`

```python
import time
import random
from functools import wraps
from typing import Type, Tuple

def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True
):
    """Retry decorator with exponential backoff and jitter."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)

                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay *= (0.5 + random.random())

                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}), "
                        f"retrying in {delay:.2f}s: {e}"
                    )
                    time.sleep(delay)

        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_attempts=3, base_delay=2.0, exceptions=(requests.RequestException,))
def fetch_goatedbets_data(sport, week):
    response = requests.get(f"{API_URL}/{sport}/week/{week}", timeout=30)
    response.raise_for_status()
    return response.json()
```

**Apply to All API Calls**:
- `_L1/inputs/goatedbets_api.py` - 3 API methods
- `_L1/inputs/balldontlie_api.py` - 4 API methods
- `_L1/inputs/ai_models.py` - Gemini/Claude API calls
- `_L5/L5_media.py` - Flux/DALL-E/Gemini calls

### 1.4 Thread-Safe Cache Implementation

**Problem**: Global MCP games cache has no locking

**Solution**: Thread-safe cache with TTL

**File to Create**: `app/core/utils/cache_utils.py`

```python
import threading
from datetime import datetime, timedelta
from typing import Any, Optional

class ThreadSafeCache:
    def __init__(self, ttl_seconds: int = 3600):
        self._cache = {}
        self._lock = threading.RLock()
        self._ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None

            value, timestamp = self._cache[key]

            # Check TTL
            if datetime.now() - timestamp > self._ttl:
                del self._cache[key]
                return None

            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._cache[key] = (value, datetime.now())

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

# Replace global cache in L3_ideas.py
_MCP_GAMES_CACHE = ThreadSafeCache(ttl_seconds=1800)  # 30 min TTL
```

### 1.5 FFmpeg Error Capture & Logging

**Problem**: Subprocess errors swallowed, no diagnostic info

**Solution**: Proper subprocess error handling

**File to Modify**: `app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py`

```python
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_ffmpeg_command(cmd: List[str], timeout: int = 300) -> str:
    """
    Run FFmpeg command with proper error handling.

    Args:
        cmd: FFmpeg command as list
        timeout: Timeout in seconds (default 5min for long encodes)

    Returns:
        Output file path

    Raises:
        FFmpegError: If encoding fails
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True
        )

        if result.returncode != 0:
            # Log full stderr for debugging
            logger.error(
                f"FFmpeg failed with code {result.returncode}\n"
                f"Command: {' '.join(cmd)}\n"
                f"stderr: {result.stderr}"
            )
            raise FFmpegError(
                f"FFmpeg encoding failed: {result.stderr[:500]}"
            )

        # Log success with timing info
        logger.info(f"FFmpeg completed: {cmd[-1]}")
        return cmd[-1]  # Output file path

    except subprocess.TimeoutExpired as e:
        logger.error(f"FFmpeg timeout after {timeout}s: {' '.join(cmd)}")
        raise FFmpegError(f"FFmpeg timed out after {timeout} seconds")
    except FileNotFoundError:
        logger.error("FFmpeg binary not found - check installation")
        raise FFmpegError("FFmpeg not installed or not in PATH")
```

### 1.6 Structured Logging

**Problem**: Print statements instead of proper logging

**Solution**: Python logging with correlation IDs

**File to Create**: `app/core/utils/logging_config.py`

```python
import logging
import uuid
from contextvars import ContextVar

# Store job_id in context for correlation
job_context: ContextVar[str] = ContextVar('job_id', default='no-job')

class JobContextFilter(logging.Filter):
    def filter(self, record):
        record.job_id = job_context.get()
        return True

def setup_pipeline_logging():
    """Configure structured logging for pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(job_id)s | %(name)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler('logs/pipeline.log'),
            logging.StreamHandler()
        ]
    )

    # Add context filter to all handlers
    for handler in logging.root.handlers:
        handler.addFilter(JobContextFilter())

# Usage in pipeline
def run_pipeline(job_id: str, config: dict):
    job_context.set(job_id)  # Set context for all logs
    logger = logging.getLogger(__name__)
    logger.info(f"Starting pipeline for {config['preset_id']}")
    # ... rest of pipeline
```

---

## Phase 2: Preview Architecture Implementation

**Timeline**: 3-4 weeks
**Dependencies**: Phase 1 reliability fixes completed

### 2.1 Backend API Changes

#### A. Modify `app/api/routes/jobs.py`

**New Endpoints**:

```python
@jobs_bp.route("/<job_id>/preview-data", methods=["GET"])
def get_preview_data(job_id):
    """
    Return L4 timing + L5 media for browser preview.

    Response:
    {
      "timing_data": {
        "total_duration": 45.3,
        "segments": [
          {"start": 0, "end": 3.2, "text": "...", "media_id": "asset_1"}
        ]
      },
      "media_assets": [
        {"id": "asset_1", "type": "image", "url": "/api/outputs/...", "duration": 3.2}
      ],
      "brand_rules": {
        "font_family": "Inter",
        "primary_color": "#FFD700",
        "logo_url": "/api/outputs/logo.png"
      },
      "audio_url": "/api/outputs/L4/audio.mp3"
    }
    """

@jobs_bp.route("/<job_id>/approve-preview", methods=["POST"])
def approve_preview(job_id):
    """
    Approve preview and trigger L6 final render.

    Request:
    {
      "preview_adjustments": {
        "text_size_multiplier": 1.2,
        "timing_offset": 0.5
      }
    }
    """

@jobs_bp.route("/<job_id>/skip-preview", methods=["POST"])
def skip_preview(job_id):
    """Skip preview, go straight to L6 (batch mode)."""
```

#### B. Modify `app/services/job_service.py`

**New Methods**:

```python
class JobManager:
    def pause_at_layer(self, job_id: str, layer: str):
        """Pause after specified layer for preview."""
        job = self._jobs[job_id]
        job["paused_at_layer"] = layer
        job["status"] = "awaiting_preview"
        self._emit_event(job_id, JobEventType.PREVIEW_READY, {
            "preview_url": f"/jobs/{job_id}/preview-data"
        })

    def resume_job_at_layer(self, job_id: str, layer: str):
        """Resume from preview approval."""
        job = self._jobs[job_id]
        job["status"] = "running"
        job["current_layer"] = layer
        self._execute_layer(job_id, layer)

def extract_preview_data(job_id: str) -> dict:
    """Extract L4 timing + L5 media for preview."""
    # Implementation in plan
```

#### C. Modify `app/core/pipeline/layers/_L6/L6_assembly.py`

**Add Preview Mode**:

```python
def run_L6_assembly(job_id: str, config: dict) -> dict:
    # Check preview mode flag
    if config.get("preview_mode", False):
        logger.info("Preview mode - pausing at L5")
        return {
            "status": "awaiting_preview",
            "skip_l6": True
        }

    # Apply preview adjustments if resuming
    adjustments = config.get("preview_adjustments", {})
    if adjustments:
        apply_adjustments_to_assembly(adjustments)

    # Continue with MoviePy + FFmpeg rendering
    # ... existing logic ...
```

### 2.2 Frontend Components

#### A. New Component: `PreviewStudio.jsx`

**Location**: `app/frontend/src/components/PreviewStudio.jsx`

**Purpose**: Main preview orchestration

**Key Features**:
- Fetch preview data from `/jobs/:id/preview-data`
- Render frames in hidden canvas
- Capture with html2canvas
- Record with RecordRTC
- Playback controls
- Approve/adjust workflow

**State Structure**:
```javascript
{
  mode: 'idle' | 'loading' | 'rendering' | 'ready' | 'playing',
  mediaAssets: [],
  timingData: {},
  brandRules: {},
  recordedBlob: null,
  previewUrl: null,
  error: null
}
```

#### B. New Component: `PreviewCanvas.jsx`

**Location**: `app/frontend/src/components/PreviewCanvas.jsx`

**Purpose**: DOM-based frame renderer

**Renders**:
- Background media (images/video frames)
- Text overlays with brand styling
- Logo overlays
- CSS animations (Ken Burns)

#### C. New Utility: `RecordingEngine.js`

**Location**: `app/frontend/src/utils/RecordingEngine.js`

**Purpose**: RecordRTC wrapper with audio sync

**Key Methods**:
```javascript
class RecordingEngine {
  async startRecording()
  async stopRecording() -> Blob
  async addAudioTrack(audioUrl)
  cleanup()
}
```

**Configuration**:
```javascript
{
  fps: 30,
  width: 1080,
  height: 1920,
  videoBitsPerSecond: 8000000,  // 8 Mbps
  mimeType: 'video/webm;codecs=vp9'
}
```

#### D. Modified: `GenerationFlow.jsx`

**Changes**:
- After L5 completes, check if preview enabled
- Route to PreviewStudio instead of waiting for L6
- Add "Skip Preview" option

```javascript
if (statusData.current_layer === 'L5' &&
    statusData.status === 'layer_complete' &&
    presetSupportsPreview) {
  setStep('preview');
} else {
  // Continue to L6
}
```

### 2.3 Package Dependencies

**Add to `app/frontend/package.json`**:
```json
{
  "dependencies": {
    "recordrtc": "^5.6.2",
    "html2canvas": "^1.4.1"
  }
}
```

---

## Phase 3: Browser Compatibility & Fallbacks

**Timeline**: 1 week
**Focus**: Cross-browser support, iOS Safari, progressive enhancement

### 3.1 Capability Detection

**File**: `app/frontend/src/utils/BrowserCapabilities.js`

```javascript
export class BrowserCapabilities {
  static checkPreviewSupport() {
    return {
      mediaRecorder: typeof MediaRecorder !== 'undefined',
      canvas: typeof HTMLCanvasElement !== 'undefined',
      webAudio: typeof AudioContext !== 'undefined',
      webm: MediaRecorder.isTypeSupported?.('video/webm;codecs=vp9'),
      full: /* all checks pass */,
      partial: /* some checks pass */,
      none: /* no support */
    };
  }
}
```

### 3.2 iOS Safari Fallback

```javascript
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

if (isIOS) {
  // Use H.264 codec (better iOS support)
  recorderConfig.mimeType = 'video/mp4;codecs=h264';

  // Reduce bitrate
  recorderConfig.videoBitsPerSecond = 5000000;

  // Disable audio (iOS limitation)
  recorderConfig.disableAudio = true;
}
```

### 3.3 Progressive Enhancement

```javascript
useEffect(() => {
  const capabilities = BrowserCapabilities.checkPreviewSupport();

  if (capabilities.none) {
    // Fallback: Skip to L6
    skipToFinalRender();
  } else if (capabilities.partial) {
    // Static preview only
    renderStaticPreview();
  } else {
    // Full preview with recording
    initializePreviewRecording();
  }
}, []);
```

---

## Phase 4: Performance Optimization

**Timeline**: 1 week
**Focus**: Memory management, 60fps rendering, asset preloading

### 4.1 Memory Management

**File**: `app/frontend/src/utils/MemoryManager.js`

```javascript
class MemoryManager {
  constructor() {
    this.objectUrls = [];
    this.canvasCache = new Map();
  }

  createObjectUrl(blob) {
    const url = URL.createObjectURL(blob);
    this.objectUrls.push(url);
    return url;
  }

  cleanup() {
    this.objectUrls.forEach(url => URL.revokeObjectURL(url));
    this.canvasCache.clear();
  }
}
```

### 4.2 Asset Preloading

```javascript
async function preloadAssets(mediaAssets) {
  const promises = mediaAssets
    .filter(a => a.type === 'image')
    .map(asset => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.crossOrigin = 'anonymous';
        img.src = asset.url;
      });
    });

  return Promise.all(promises);
}
```

### 4.3 CSS Optimization for 60fps

```css
.preview-frame {
  /* GPU acceleration */
  transform: translateZ(0);
  will-change: transform, opacity;

  /* Optimize rendering */
  contain: layout style paint;
}

.text-overlay {
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
```

---

## Phase 5: Testing & Rollout

**Timeline**: 1-2 weeks
**Focus**: Feature flag rollout, monitoring, bug fixes

### 5.1 Feature Flag Implementation

```python
# app/config.py
PREVIEW_ENABLED_PRESETS = [
    'carousel_illustrated',
    'single_image_stat',
    'reel_hype'
]

def should_enable_preview(preset_id: str) -> bool:
    return preset_id in PREVIEW_ENABLED_PRESETS
```

### 5.2 Monitoring Metrics

**Track**:
- Preview generation time (target: < 10s)
- Preview approval rate (target: > 70%)
- Final render invocations (expect 60% reduction)
- Browser compatibility issues
- Memory leak incidents

### 5.3 Rollout Plan

**Week 1**: Beta users only (10%)
**Week 2**: Expand to 50% if metrics good
**Week 3**: Full rollout (100%)
**Week 4**: Monitor and fix issues

---

## Additional Recommendations

### 1. WebSocket for Real-Time Updates

**Problem**: Polling every 2 seconds is inefficient

**Solution**: Flask-SocketIO for streaming updates

```python
# app/api/routes/jobs.py
from flask_socketio import emit

@socketio.on('subscribe_job')
def subscribe_to_job(job_id):
    join_room(job_id)

# In job_service.py
def _emit_event(self, job_id, event_type, data):
    socketio.emit('job_update', {
        'type': event_type,
        'data': data
    }, room=job_id)
```

### 2. Layer Output Caching

**Problem**: Re-running L1-L3 for minor adjustments wastes time

**Solution**: Cache layer outputs by hash of inputs

```python
def get_cached_layer_output(layer: str, input_hash: str) -> Optional[dict]:
    cache_file = f"cache/{layer}_{input_hash}.json"
    if os.path.exists(cache_file):
        logger.info(f"Cache hit for {layer}")
        return json.load(open(cache_file))
    return None

def save_layer_output_to_cache(layer: str, input_hash: str, output: dict):
    cache_file = f"cache/{layer}_{input_hash}.json"
    json.dump(output, open(cache_file, 'w'))
```

### 3. Vision Integration Prep

**Future**: Allow users to upload reference images for style matching

**Prep Work**:
- Add image upload to PresetBuilder
- Store reference images with preset
- Pass to L5 vision analysis
- Use for brand consistency validation

### 4. Analytics Integration Hooks

**Future**: Track which presets perform best on social

**Prep Work**:
- Add analytics_id to outputs
- Track downloads, shares, approvals
- Store performance metrics
- Feed back into preset recommendations

---

## Files to Modify/Create

### Phase 1: Reliability Fixes

**Modify**:
- `app/core/pipeline/layers/_L6/L6_assembly.py` - Exception handling
- `app/core/pipeline/layers/_L5/L5_media.py` - Exception handling
- `app/core/pipeline/layers/_L4/L4_audio.py` - Exception handling
- `app/core/pipeline/layers/_L3/L3_ideas.py` - Thread-safe cache
- `app/core/pipeline/layers/_L1/inputs/*.py` - Retry logic
- `app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py` - Error capture

**Create**:
- `app/core/pipeline/schemas/` - Pydantic validation schemas
- `app/core/utils/retry_utils.py` - Retry decorator
- `app/core/utils/cache_utils.py` - Thread-safe cache
- `app/core/utils/logging_config.py` - Structured logging
- `app/core/exceptions.py` - Custom exception types

### Phase 2: Preview Architecture

**Modify**:
- `app/api/routes/jobs.py` - Add preview endpoints
- `app/services/job_service.py` - Pause/resume logic
- `app/core/pipeline/layers/_L6/L6_assembly.py` - Preview mode
- `app/frontend/src/components/GenerationFlow.jsx` - Preview routing
- `app/frontend/package.json` - Add dependencies

**Create**:
- `app/frontend/src/components/PreviewStudio.jsx` - Main preview component
- `app/frontend/src/components/PreviewCanvas.jsx` - Frame renderer
- `app/frontend/src/utils/RecordingEngine.js` - RecordRTC wrapper
- `app/frontend/src/contexts/PreviewContext.jsx` - State management
- `app/frontend/src/utils/BrowserCapabilities.js` - Feature detection
- `app/frontend/src/utils/MemoryManager.js` - Cleanup utilities

---

## Verification Strategy

### Phase 1 Verification (Reliability)

1. **Exception Handling**: Intentionally trigger errors, verify proper logging
2. **Input Validation**: Submit invalid data, verify Pydantic catches it
3. **Retry Logic**: Simulate API timeout, verify exponential backoff
4. **Thread Safety**: Run concurrent jobs, verify no cache corruption
5. **FFmpeg Errors**: Trigger encoding failure, verify error captured

**Success Criteria**:
- No silent failures
- All errors have traceback + context
- Failed jobs provide actionable error messages
- Pipeline success rate > 95%

### Phase 2 Verification (Preview)

1. **Preview Generation**: Generate preview for carousel preset in < 10s
2. **Audio Sync**: Verify audio matches video timing
3. **Browser Compatibility**: Test on Chrome, Firefox, Safari (desktop + mobile)
4. **Approval Flow**: Approve preview → verify L6 runs with adjustments
5. **Skip Flow**: Skip preview → verify goes straight to L6

**Success Criteria**:
- Preview loads in < 10 seconds
- Audio sync drift < 100ms
- Works on 90%+ of browsers (with fallbacks)
- Approval triggers L6 correctly
- Preview quality sufficient for decision-making

### End-to-End Test

1. Select sport + matchup
2. Choose carousel preset
3. Click "Generate Preview"
4. Wait for L5 completion (~60s)
5. Preview renders in browser (~5s)
6. Play preview, verify quality
7. Adjust text size (+20%)
8. Re-render preview (~5s)
9. Approve preview
10. L6 renders final video (~45s)
11. Download 1080p MP4
12. Verify final matches preview

---

## Timeline Summary

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 1: Reliability Fixes** | 3-4 weeks | Pipeline success rate > 95% |
| **Phase 2: Preview Architecture** | 3-4 weeks | Browser-based preview working |
| **Phase 3: Browser Compat** | 1 week | iOS Safari support, fallbacks |
| **Phase 4: Performance** | 1 week | < 10s preview, no memory leaks |
| **Phase 5: Testing & Rollout** | 1-2 weeks | Feature flag rollout, monitoring |
| **TOTAL** | **6-8 weeks** | Production-ready preview system |

**Critical Path**: Phase 1 must complete before Phase 2 begins

---

## Risk Mitigation

### High Risks

1. **RecordRTC compatibility issues on iOS**
   - Mitigation: Fallback to static preview, H.264 codec

2. **Browser memory leaks with large assets**
   - Mitigation: MemoryManager, aggressive cleanup, asset preloading

3. **Audio sync drift in browser recording**
   - Mitigation: Web Audio API precise timing, fallback to muted preview

4. **Phase 1 fixes introduce new bugs**
   - Mitigation: Comprehensive test suite, gradual rollout, rollback plan

### Medium Risks

5. **Preview quality too low for approval decisions**
   - Mitigation: Configurable bitrate, quality presets

6. **L6 adjustments don't match preview**
   - Mitigation: Validate preview adjustments, show diff before final render

---

## Success Metrics

**User Experience**:
- Time to first preview: **< 10 seconds** (vs 2-5 minutes current)
- Preview approval rate: **> 70%** (users approve vs adjust)
- Iteration cycles: **3-5 previews** before final render
- User satisfaction: **+40% improvement** (survey-based)

**System Reliability**:
- Pipeline success rate: **> 95%** (vs ~70% estimated current)
- Error logging coverage: **100%** of exception paths
- API retry success: **> 90%** on transient failures

**Cost Savings**:
- Final render invocations: **-60%** (fewer re-runs)
- API costs: **-40%** (cache + preview approval)

---

## Post-Implementation: Future Enhancements

1. **Real-time Collaboration**: Multiple users preview same job
2. **A/B Testing**: Generate 2-3 variations, preview all, pick winner
3. **Smart Suggestions**: AI recommends text adjustments based on preview
4. **Version History**: Save preview snapshots, rollback to previous
5. **Batch Preview**: Queue multiple presets, preview all, batch approve
6. **Export Preview**: Download preview as-is for quick social posts
7. **Vision Feedback**: AI analyzes preview quality, suggests improvements
8. **Analytics Integration**: Track which previews → approved → high engagement

---

## Conclusion

This dual-path architecture transforms the Media Engine from a "black box" pipeline into an **interactive creative tool** matching Google AI Studio's workflow. By fixing critical reliability issues first, then layering on browser-based previews, we achieve:

- **10x faster iteration** (10s preview vs 2min full render)
- **60% cost reduction** (fewer failed renders)
- **95%+ reliability** (comprehensive error handling)
- **Professional UX** (instant feedback, adjust before commit)

The phased approach ensures stability while delivering incremental value. Start with reliability (Phase 1), then preview (Phase 2), then optimize (Phases 3-4).

**Recommended Start**: Begin Phase 1 reliability fixes immediately. These provide value independent of preview system and create solid foundation for Phase 2.
