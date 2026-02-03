# Phase 2: Preview-Driven Architecture

**Session:** DB8c - Phase 2
**Date:** January 29, 2026
**Status:** PLANNING
**Timeline:** 3-4 weeks
**Scope:** Browser-based preview system (Google AI Studio workflow)
**Dependencies:** Phase 1 (Reliability Fixes) must be completed first

---

## Executive Summary

Transform the Media Engine into a **Google AI Studio-like workflow** with instant browser-based previews before committing to production renders. This dual-path architecture enables rapid iteration (2-5 second previews) vs waiting 2-5 minutes for full L1-L6 pipeline completion.

**Key Innovation**: Pause pipeline at L5, generate browser preview using RecordRTC + html2canvas, only run expensive L6 MoviePy rendering after user approval.

**User Benefit**: 10x faster iteration, 60% cost reduction, professional UX matching industry-leading AI tools.

---

## Current State vs Desired State

### Current Workflow (Pain Points)

```
┌───────────────────────────────────────┐
│ USER EXPERIENCE TODAY                 │
├───────────────────────────────────────┤
│ 1. Configure preset                   │
│ 2. Click "Generate"                   │
│ 3. Wait 2-5 minutes...                │
│    ⏳ No visual feedback              │
│    ⏳ Can't preview before commit     │
│    ⏳ Font/layout issues discovered   │
│       only after completion           │
│ 4. Download result                    │
│ 5. If wrong, go back to step 1        │
│    (re-run entire pipeline)           │
└───────────────────────────────────────┘
```

**Problems**:
- Zero visual feedback during 2-5 minute wait
- Font/spacing/timing issues only discovered after full render
- Must re-run L1-L6 (2-5 min) to fix minor text adjustments
- API costs wasted on failed renders
- User loses context during long wait

### Desired Workflow (Google AI Studio Style)

```
┌─────────────────────────────────────────────────────────┐
│ USER EXPERIENCE AFTER PHASE 2                           │
├─────────────────────────────────────────────────────────┤
│ 1. Configure preset                                     │
│ 2. Click "Generate Preview"                             │
│ 3. Wait ~60s for L1-L5 (data + media generation)        │
│ 4. Preview renders in browser (2-5 seconds)             │
│    ✓ See actual content before committing              │
│    ✓ Adjust text size, timing, colors                  │
│    ✓ Re-preview instantly (no re-run)                  │
│ 5. Approve preview when satisfied                       │
│ 6. Final L6 render (30-60 seconds, production quality)  │
│ 7. Download final 1080p MP4                             │
└─────────────────────────────────────────────────────────┘
```

**Benefits**:
- Instant visual feedback (2-5s preview vs 2-5min wait)
- Iterate on text/layout without re-running pipeline
- Discover issues before expensive L6 render
- Save API costs (only run L6 once when approved)
- Match Google AI Studio's UX expectations

---

## Architecture Overview

### Dual-Path System

```
                    ┌──────────────────┐
                    │ User Configures  │
                    │ Preset           │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Click "Generate  │
                    │ Preview"         │
                    └────────┬─────────┘
                             │
         ┌───────────────────▼───────────────────┐
         │ BACKEND: Run L1-L5 (~60 seconds)      │
         │ ├─ L1: Data Fetch (5s)                │
         │ ├─ L2: Calendar Config (2s)           │
         │ ├─ L3: Ideas Generation (10s)         │
         │ ├─ L4: Audio + Timing (15s)           │
         │ └─ L5: Media Generation (30s)         │
         │    ⏸  PAUSE HERE (preview_mode=true)  │
         └───────────────────┬───────────────────┘
                             │
         ┌───────────────────▼───────────────────┐
         │ FRONTEND: Browser Preview (2-5s)      │
         │ ├─ Fetch L4 timing + L5 media         │
         │ ├─ Render frames in DOM               │
         │ ├─ Capture with html2canvas           │
         │ ├─ Record with RecordRTC              │
         │ ├─ Mix audio (Web Audio API)          │
         │ └─ Show preview player                │
         └───────────────────┬───────────────────┘
                             │
                    ┌────────▼─────────┐
                    │ Preview Player   │
                    │ (WebM/MP4)       │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
    ┌─────────▼─────────┐      ┌───────────▼─────────┐
    │ Adjust Preview    │      │ Approve Preview     │
    │ (text size,       │      │                     │
    │  timing, etc.)    │      │                     │
    └─────────┬─────────┘      └───────────┬─────────┘
              │                             │
              │                    ┌────────▼─────────┐
              │                    │ BACKEND: Run L6  │
              │                    │ MoviePy + FFmpeg │
              │                    │ (30-60 seconds)  │
              │                    └────────┬─────────┘
              │                             │
              └──────────(re-render)        │
                                   ┌────────▼─────────┐
                                   │ Download Final   │
                                   │ 1080p MP4        │
                                   └──────────────────┘
```

---

## Technology Stack

### Browser Preview Path (NEW)

| Technology | Purpose | Why This Choice |
|------------|---------|----------------|
| **RecordRTC** (5.6.2) | Browser-based video recording | Industry standard, 50k+ stars, WebM/VP9 support |
| **html2canvas** (1.4.1) | DOM to canvas capture | Widely used, 30k+ stars, handles CSS animations |
| **Web Audio API** | Audio sync and mixing | Native browser API, precise timing control |
| **Canvas API** | Frame composition | Native, GPU-accelerated rendering |
| **CSS Animations** | Ken Burns effects | GPU-accelerated, smoother than JS |

### Server Production Path (UNCHANGED)

| Technology | Purpose | Current Usage |
|------------|---------|---------------|
| **MoviePy** | Video composition | High-quality production renders |
| **FFmpeg** | Final encoding | Broadcast-quality output |
| **PIL/Pillow** | Image processing | Logo overlays, color manipulation |

**Why Dual-Path?**
- Browser preview: Fast iteration, instant feedback, good enough for approval decisions
- Server render: Production quality, industry-standard codecs, final distribution

---

## Implementation Plan

### Week 1: Backend API Foundation

#### Task 1.1: Add Preview Mode to Jobs API

**File to Modify**: `app/api/routes/jobs.py`

**New Endpoints**:

```python
@jobs_bp.route("/<job_id>/preview-data", methods=["GET"])
def get_preview_data(job_id):
    """
    Return L4 timing + L5 media assets for browser preview.

    Returns:
    {
      "timing_data": {
        "total_duration": 45.3,
        "segments": [
          {
            "start": 0,
            "end": 3.2,
            "text": "Josh Allen OVER 275.5 passing yards",
            "media_id": "asset_1",
            "animation": "fade_in"
          },
          {
            "start": 3.2,
            "end": 6.5,
            "text": "Last 5 games average: 312 yards",
            "media_id": "asset_2",
            "animation": "slide_up"
          }
        ]
      },
      "media_assets": [
        {
          "id": "asset_1",
          "type": "image",
          "url": "/api/outputs/L5/josh_allen_stat_visual.jpg",
          "duration": 3.2,
          "width": 1080,
          "height": 1920
        },
        {
          "id": "asset_2",
          "type": "image",
          "url": "/api/outputs/L5/trend_chart.jpg",
          "duration": 3.3,
          "width": 1080,
          "height": 1920
        }
      ],
      "brand_rules": {
        "font_family": "Inter",
        "font_weight": "700",
        "primary_color": "#FFD700",
        "secondary_color": "#1a1a1a",
        "text_size": 48,
        "logo_url": "/api/outputs/branding/Main_Logo.png",
        "logo_position": "bottom_right"
      },
      "audio_url": "/api/outputs/L4/narration.mp3",
      "audio_duration": 45.3
    }
    """
    job_manager = get_job_manager()
    job = job_manager.get_job(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    # Check if L5 has completed
    if job["current_layer"] != "L5" or job["status"] != "awaiting_preview":
        return jsonify({"error": "Preview data not ready yet"}), 400

    # Extract preview data from L4 and L5 outputs
    preview_data = extract_preview_data(job)
    return jsonify(preview_data)


@jobs_bp.route("/<job_id>/approve-preview", methods=["POST"])
def approve_preview(job_id):
    """
    User approved browser preview - trigger L6 final render.

    Request body:
    {
      "preview_adjustments": {
        "text_size_multiplier": 1.2,    # 20% larger text
        "timing_offset": 0.5,             # +0.5s to all timings
        "primary_color": "#00FF00"        # Override color
      }
    }

    Returns:
    {
      "message": "Final render started",
      "job_id": "job_abc123",
      "estimated_duration": 45
    }
    """
    job_manager = get_job_manager()
    job = job_manager.get_job(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    # Apply any adjustments from preview
    adjustments = request.get_json().get("preview_adjustments", {})
    if adjustments:
        job["config"]["preview_adjustments"] = adjustments
        logger.info(f"Preview adjustments applied: {adjustments}")

    # Resume pipeline at L6
    job_manager.resume_job_at_layer(job_id, "L6")

    return jsonify({
        "message": "Final render started",
        "job_id": job_id,
        "estimated_duration": estimate_l6_duration(job)
    })


@jobs_bp.route("/<job_id>/skip-preview", methods=["POST"])
def skip_preview(job_id):
    """
    Skip preview and go straight to L6 (for batch workflows).

    Use case: Automation scripts that don't need preview
    """
    job_manager = get_job_manager()
    job_manager.resume_job_at_layer(job_id, "L6")

    return jsonify({
        "message": "Skipped to final render",
        "job_id": job_id
    })
```

#### Task 1.2: Job Service Pause/Resume Logic

**File to Modify**: `app/services/job_service.py`

**New Methods**:

```python
class JobManager:
    def pause_at_layer(self, job_id: str, layer: str):
        """
        Pause pipeline execution after specified layer.

        Used to halt at L5 for preview generation.
        """
        job = self._jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        job["paused_at_layer"] = layer
        job["status"] = "awaiting_preview"

        logger.info(f"Job {job_id} paused at {layer} for preview")

        # Emit event to frontend
        self._emit_event(job_id, JobEventType.PREVIEW_READY, {
            "message": f"Preview data ready after {layer}",
            "preview_url": f"/api/jobs/{job_id}/preview-data"
        })

    def resume_job_at_layer(self, job_id: str, layer: str):
        """
        Resume paused job at specific layer.

        Used to continue to L6 after preview approval.
        """
        job = self._jobs.get(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        if job["status"] != "awaiting_preview":
            raise ValueError(f"Job {job_id} is not paused for preview")

        job["status"] = "running"
        job["current_layer"] = layer

        logger.info(f"Job {job_id} resumed at {layer}")

        # Re-queue for execution at specified layer
        self._execute_layer(job_id, layer)


def extract_preview_data(job: dict) -> dict:
    """
    Extract L4 timing metadata + L5 media assets for browser preview.

    Args:
        job: Job dictionary with output directories

    Returns:
        Preview data structure for frontend
    """
    job_id = job["job_id"]
    output_dir = job["output_dir"]

    # Load L4 timing data
    l4_dir = os.path.join(output_dir, "L4")
    timing_file = os.path.join(l4_dir, "ideas_with_audio.json")

    if not os.path.exists(timing_file):
        raise FileNotFoundError(f"L4 timing file not found: {timing_file}")

    with open(timing_file, 'r') as f:
        l4_data = json.load(f)

    # Load L5 media packages
    l5_dir = os.path.join(output_dir, "L5")
    media_file = os.path.join(l5_dir, "media_packages.json")

    if not os.path.exists(media_file):
        raise FileNotFoundError(f"L5 media file not found: {media_file}")

    with open(media_file, 'r') as f:
        l5_data = json.load(f)

    # Load brand rules from preset
    preset_id = job["config"]["preset_id"]
    preset = load_preset(preset_id)
    brand_rules = preset.get("brand_rules", {})

    # Transform for preview format
    return {
        "timing_data": transform_timing_for_preview(l4_data),
        "media_assets": transform_media_for_preview(l5_data, output_dir),
        "brand_rules": brand_rules,
        "audio_url": get_audio_url(l4_dir),
        "audio_duration": calculate_total_duration(l4_data)
    }


def transform_timing_for_preview(l4_data: dict) -> dict:
    """Convert L4 timing format to preview-friendly structure."""
    segments = []
    current_time = 0

    for idea in l4_data.get("ideas", []):
        duration = idea.get("duration", 3.0)

        segments.append({
            "start": current_time,
            "end": current_time + duration,
            "text": idea.get("text", ""),
            "media_id": idea.get("media_id"),
            "animation": idea.get("animation", "fade_in")
        })

        current_time += duration

    return {
        "total_duration": current_time,
        "segments": segments
    }


def transform_media_for_preview(l5_data: dict, output_dir: str) -> list:
    """Convert L5 media packages to preview-friendly asset list."""
    assets = []

    for package in l5_data.get("packages", []):
        media_id = package["id"]
        media_path = package["media_path"]

        # Convert absolute path to API URL
        relative_path = os.path.relpath(media_path, output_dir)
        api_url = f"/api/outputs/{relative_path}"

        assets.append({
            "id": media_id,
            "type": package.get("type", "image"),
            "url": api_url,
            "duration": package.get("duration", 3.0),
            "width": package.get("width", 1080),
            "height": package.get("height", 1920)
        })

    return assets
```

#### Task 1.3: L6 Assembly Preview Mode

**File to Modify**: `app/core/pipeline/layers/_L6/L6_assembly.py`

**Add Preview Mode Check**:

```python
def run_L6_assembly(job_id: str, config: dict) -> dict:
    """
    L6 Assembly Layer - Final video rendering.

    Args:
        config: {
            "preview_mode": bool,              # NEW
            "preview_adjustments": dict,       # NEW
            ...existing config...
        }
    """
    logger = logging.getLogger(__name__)

    # NEW: Check if preview mode is enabled
    if config.get("preview_mode", False):
        logger.info("Preview mode enabled - pausing at L5")

        # Signal job manager to pause
        return {
            "status": "awaiting_preview",
            "message": "L5 complete - preview data ready",
            "skip_l6": True
        }

    # NEW: Apply preview adjustments if resuming from preview
    adjustments = config.get("preview_adjustments", {})
    if adjustments:
        logger.info(f"Applying preview adjustments: {adjustments}")
        apply_preview_adjustments(adjustments, config)

    # Continue with existing L6 logic...
    # MoviePy + FFmpeg rendering
    ...


def apply_preview_adjustments(adjustments: dict, config: dict):
    """
    Apply user adjustments from preview approval.

    Adjustments can include:
    - text_size_multiplier: Scale all text sizes
    - timing_offset: Add/subtract time from all segments
    - primary_color: Override brand color
    - logo_position: Change logo placement
    """
    if "text_size_multiplier" in adjustments:
        multiplier = adjustments["text_size_multiplier"]
        config["text_size"] = int(config.get("text_size", 48) * multiplier)
        logger.info(f"Text size adjusted by {multiplier}x")

    if "timing_offset" in adjustments:
        offset = adjustments["timing_offset"]
        # Apply to timing data (would modify L4 output)
        logger.info(f"Timing offset: {offset}s")

    if "primary_color" in adjustments:
        config["brand_rules"]["primary_color"] = adjustments["primary_color"]
        logger.info(f"Primary color changed to {adjustments['primary_color']}")
```

---

### Week 2: Frontend Components

#### Task 2.1: RecordingEngine Utility

**File to Create**: `app/frontend/src/utils/RecordingEngine.js`

```javascript
import RecordRTC from 'recordrtc';

/**
 * RecordingEngine - Browser-based video recording with audio sync
 *
 * Usage:
 *   const engine = new RecordingEngine(canvasElement, options);
 *   await engine.addAudioTrack(audioUrl);
 *   await engine.startRecording();
 *   // ... render frames ...
 *   const blob = await engine.stopRecording();
 */
export class RecordingEngine {
  constructor(targetElement, options = {}) {
    this.target = targetElement;
    this.options = {
      fps: options.fps || 30,
      width: options.width || 1080,
      height: options.height || 1920,
      videoBitsPerSecond: options.bitrate || 8000000,  // 8 Mbps
      mimeType: this.detectBestMimeType()
    };

    this.recorder = null;
    this.stream = null;
    this.audioTrack = null;
    this.audioContext = null;
  }

  detectBestMimeType() {
    // Prefer VP9 for quality, fallback to VP8, then H.264
    const types = [
      'video/webm;codecs=vp9',
      'video/webm;codecs=vp8',
      'video/mp4;codecs=h264'
    ];

    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        console.log(`Using codec: ${type}`);
        return type;
      }
    }

    throw new Error('No supported video codec found');
  }

  async addAudioTrack(audioUrl) {
    /**
     * Mix audio track for synchronized recording.
     *
     * Uses Web Audio API for precise timing.
     */
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

    // Fetch audio file
    const response = await fetch(audioUrl);
    const arrayBuffer = await response.arrayBuffer();

    // Decode audio
    const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);

    // Create MediaStreamDestination
    const destination = this.audioContext.createMediaStreamDestination();

    // Create buffer source
    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(destination);

    // Store audio track
    this.audioTrack = destination.stream.getAudioTracks()[0];

    console.log(`Audio track loaded: ${audioBuffer.duration.toFixed(2)}s`);
  }

  async startRecording() {
    /**
     * Start recording canvas + audio.
     */
    // Create canvas stream
    const canvasStream = this.target.captureStream(this.options.fps);

    // Combine video + audio tracks
    const tracks = [...canvasStream.getVideoTracks()];
    if (this.audioTrack) {
      tracks.push(this.audioTrack);
    }

    this.stream = new MediaStream(tracks);

    // Initialize RecordRTC
    this.recorder = new RecordRTC(this.stream, {
      type: 'video',
      mimeType: this.options.mimeType,
      videoBitsPerSecond: this.options.videoBitsPerSecond,
      frameRate: this.options.fps,
      canvas: {
        width: this.options.width,
        height: this.options.height
      }
    });

    this.recorder.startRecording();

    // Start audio playback (if audio track exists)
    if (this.audioContext && this.audioTrack) {
      const source = this.audioContext.createBufferSource();
      source.connect(this.audioContext.destination);
      source.start(0);
    }

    console.log('Recording started');
  }

  async stopRecording() {
    /**
     * Stop recording and return video blob.
     *
     * Returns: Blob (WebM/MP4 video file)
     */
    return new Promise((resolve) => {
      this.recorder.stopRecording(() => {
        const blob = this.recorder.getBlob();
        console.log(`Recording stopped: ${(blob.size / 1024 / 1024).toFixed(2)} MB`);
        resolve(blob);
      });
    });
  }

  cleanup() {
    /**
     * Clean up resources.
     */
    if (this.recorder) {
      this.recorder.destroy();
    }

    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
    }

    if (this.audioContext) {
      this.audioContext.close();
    }
  }
}
```

#### Task 2.2: PreviewCanvas Component

**File to Create**: `app/frontend/src/components/PreviewCanvas.jsx`

```jsx
import React, { useRef, useEffect } from 'react';
import './PreviewCanvas.css';

/**
 * PreviewCanvas - DOM-based frame renderer for video preview
 *
 * Renders each frame as HTML/CSS, captures with html2canvas
 */
export function PreviewCanvas({ frame, mediaAssets, brandRules, onFrameRendered }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (frame && canvasRef.current) {
      renderFrame();
    }
  }, [frame]);

  const renderFrame = async () => {
    // Find active segment for this frame
    const segment = frame.segment;
    const mediaAsset = mediaAssets.find(a => a.id === segment.media_id);

    if (!mediaAsset) {
      console.warn(`Media asset not found: ${segment.media_id}`);
      return;
    }

    // Notify parent that frame is rendered
    if (onFrameRendered) {
      onFrameRendered(frame.index);
    }
  };

  if (!frame) {
    return null;
  }

  const segment = frame.segment;
  const mediaAsset = mediaAssets.find(a => a.id === segment.media_id);

  return (
    <div
      ref={canvasRef}
      className="preview-canvas"
      style={{
        width: 1080,
        height: 1920,
        position: 'relative',
        backgroundColor: brandRules.secondary_color || '#000'
      }}
    >
      {/* Background Media */}
      {mediaAsset && (
        <img
          src={mediaAsset.url}
          alt="Background"
          className="preview-background"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover'
          }}
        />
      )}

      {/* Text Overlay */}
      {segment.text && (
        <div
          className="preview-text"
          style={{
            position: 'absolute',
            bottom: '15%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '90%',
            textAlign: 'center',
            fontFamily: brandRules.font_family || 'Inter',
            fontWeight: brandRules.font_weight || '700',
            fontSize: `${brandRules.text_size || 48}px`,
            color: brandRules.primary_color || '#FFD700',
            textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
            animation: `${segment.animation} 0.5s ease-in-out`
          }}
        >
          {segment.text}
        </div>
      )}

      {/* Logo Overlay */}
      {brandRules.logo_url && (
        <img
          src={brandRules.logo_url}
          alt="Logo"
          className="preview-logo"
          style={{
            position: 'absolute',
            bottom: '5%',
            right: '5%',
            width: '120px',
            height: 'auto'
          }}
        />
      )}
    </div>
  );
}
```

#### Task 2.3: PreviewStudio Component

**File to Create**: `app/frontend/src/components/PreviewStudio.jsx`

```jsx
import React, { useState, useEffect, useRef } from 'react';
import { RecordingEngine } from '../utils/RecordingEngine';
import { PreviewCanvas } from './PreviewCanvas';
import axios from 'axios';
import html2canvas from 'html2canvas';
import './PreviewStudio.css';

export function PreviewStudio({ jobId, onApprove, onCancel }) {
  const [state, setState] = useState({
    mode: 'loading',  // loading | rendering | ready | playing | error
    previewData: null,
    recordedBlob: null,
    previewUrl: null,
    currentFrame: 0,
    totalFrames: 0,
    error: null
  });

  const [adjustments, setAdjustments] = useState({
    text_size_multiplier: 1.0,
    timing_offset: 0,
    primary_color: null
  });

  const canvasRef = useRef(null);
  const videoRef = useRef(null);
  const recordingEngine = useRef(null);

  useEffect(() => {
    loadPreviewData();

    return () => {
      // Cleanup
      if (recordingEngine.current) {
        recordingEngine.current.cleanup();
      }
    };
  }, [jobId]);

  const loadPreviewData = async () => {
    try {
      setState(prev => ({ ...prev, mode: 'loading' }));

      const response = await axios.get(`/api/jobs/${jobId}/preview-data`);
      const previewData = response.data;

      setState(prev => ({
        ...prev,
        previewData,
        mode: 'ready'
      }));

      // Auto-start rendering
      startPreviewRendering(previewData);

    } catch (error) {
      setState(prev => ({
        ...prev,
        mode: 'error',
        error: error.message
      }));
    }
  };

  const startPreviewRendering = async (previewData) => {
    try {
      setState(prev => ({ ...prev, mode: 'rendering' }));

      const fps = 30;
      const totalFrames = Math.ceil(previewData.timing_data.total_duration * fps);

      setState(prev => ({ ...prev, totalFrames }));

      // Initialize recording engine
      recordingEngine.current = new RecordingEngine(canvasRef.current, {
        fps: 30,
        width: 1080,
        height: 1920,
        bitrate: 8000000
      });

      // Add audio track
      await recordingEngine.current.addAudioTrack(previewData.audio_url);

      // Start recording
      await recordingEngine.current.startRecording();

      // Render frames
      for (let frame = 0; frame < totalFrames; frame++) {
        const currentTime = frame / fps;
        const segment = findSegmentAtTime(currentTime, previewData.timing_data.segments);

        // Render frame in canvas
        await renderFrame(frame, segment, previewData);

        // Update progress
        setState(prev => ({ ...prev, currentFrame: frame }));

        // Yield to browser
        await new Promise(resolve => setTimeout(resolve, 0));
      }

      // Stop recording
      const blob = await recordingEngine.current.stopRecording();
      const url = URL.createObjectURL(blob);

      setState(prev => ({
        ...prev,
        recordedBlob: blob,
        previewUrl: url,
        mode: 'ready'
      }));

    } catch (error) {
      setState(prev => ({
        ...prev,
        mode: 'error',
        error: error.message
      }));
    }
  };

  const renderFrame = async (frameIndex, segment, previewData) => {
    // Update canvas with current segment
    // (PreviewCanvas component handles rendering)

    // Capture frame to canvas using html2canvas
    const canvas = await html2canvas(canvasRef.current, {
      width: 1080,
      height: 1920,
      scale: 1,
      logging: false,
      useCORS: true
    });

    // Frame is automatically captured by RecordRTC
  };

  const findSegmentAtTime = (time, segments) => {
    return segments.find(s => time >= s.start && time < s.end) || segments[0];
  };

  const handleApprove = async () => {
    try {
      await axios.post(`/api/jobs/${jobId}/approve-preview`, {
        preview_adjustments: adjustments
      });

      if (onApprove) {
        onApprove();
      }
    } catch (error) {
      alert(`Failed to approve preview: ${error.message}`);
    }
  };

  const handleAdjustment = (key, value) => {
    setAdjustments(prev => ({ ...prev, [key]: value }));

    // Re-render preview with adjustments
    if (state.previewData) {
      startPreviewRendering(state.previewData);
    }
  };

  if (state.mode === 'loading') {
    return <div className="preview-loading">Loading preview data...</div>;
  }

  if (state.mode === 'error') {
    return <div className="preview-error">Error: {state.error}</div>;
  }

  return (
    <div className="preview-studio">
      {/* Hidden canvas for rendering */}
      <div style={{ display: 'none' }}>
        <canvas ref={canvasRef} width={1080} height={1920} />
      </div>

      {/* Preview Player */}
      {state.previewUrl && (
        <div className="preview-player">
          <video
            ref={videoRef}
            src={state.previewUrl}
            controls
            style={{ width: '100%', maxWidth: '540px' }}
          />
        </div>
      )}

      {/* Rendering Progress */}
      {state.mode === 'rendering' && (
        <div className="preview-progress">
          <p>Rendering preview...</p>
          <progress
            value={state.currentFrame}
            max={state.totalFrames}
          />
          <p>{Math.round((state.currentFrame / state.totalFrames) * 100)}%</p>
        </div>
      )}

      {/* Adjustment Controls */}
      {state.mode === 'ready' && (
        <div className="preview-controls">
          <h3>Adjust Preview</h3>

          <label>
            Text Size:
            <input
              type="range"
              min="0.5"
              max="2.0"
              step="0.1"
              value={adjustments.text_size_multiplier}
              onChange={(e) => handleAdjustment('text_size_multiplier', parseFloat(e.target.value))}
            />
            {adjustments.text_size_multiplier}x
          </label>

          <label>
            Timing Offset:
            <input
              type="range"
              min="-2"
              max="2"
              step="0.1"
              value={adjustments.timing_offset}
              onChange={(e) => handleAdjustment('timing_offset', parseFloat(e.target.value))}
            />
            {adjustments.timing_offset}s
          </label>
        </div>
      )}

      {/* Action Buttons */}
      <div className="preview-actions">
        <button onClick={onCancel} className="btn-cancel">
          Cancel
        </button>
        <button
          onClick={handleApprove}
          className="btn-approve"
          disabled={!state.previewUrl}
        >
          Approve & Render Final
        </button>
      </div>
    </div>
  );
}
```

#### Task 2.4: Modify GenerationFlow.jsx

**File to Modify**: `app/frontend/src/components/GenerationFlow.jsx`

**Changes**:
- After L5 completes, check if preview enabled
- Route to PreviewStudio instead of waiting for L6

```jsx
// Add new step after L5 completion
if (jobStatus.current_layer === 'L5' &&
    jobStatus.status === 'layer_complete' &&
    selectedPreset.supports_preview) {

  // Stop polling
  clearInterval(pollingInterval);

  // Navigate to preview step
  setStep('preview');
  setPreviewJobId(jobId);
}

// Add preview step rendering
{step === 'preview' && (
  <PreviewStudio
    jobId={previewJobId}
    onApprove={() => {
      // Resume polling for L6
      setStep('execute');
      startPolling(jobId);
    }}
    onCancel={() => {
      setStep('review');
    }}
  />
)}
```

---

### Week 3: Browser Compatibility & Optimization

#### Task 3.1: Capability Detection

**File to Create**: `app/frontend/src/utils/BrowserCapabilities.js`

```javascript
export class BrowserCapabilities {
  static checkPreviewSupport() {
    const mediaRecorder = typeof MediaRecorder !== 'undefined';
    const canvas = typeof HTMLCanvasElement !== 'undefined';
    const webAudio = typeof AudioContext !== 'undefined';
    const webm = MediaRecorder?.isTypeSupported?.('video/webm;codecs=vp9') || false;
    const mp4 = MediaRecorder?.isTypeSupported?.('video/mp4;codecs=h264') || false;

    return {
      mediaRecorder,
      canvas,
      webAudio,
      webm,
      mp4,
      full: mediaRecorder && canvas && webAudio && (webm || mp4),
      partial: canvas && mediaRecorder,
      none: !mediaRecorder
    };
  }

  static getRecommendedFormat() {
    if (MediaRecorder.isTypeSupported('video/webm;codecs=vp9')) {
      return 'video/webm;codecs=vp9';
    }
    if (MediaRecorder.isTypeSupported('video/webm;codecs=vp8')) {
      return 'video/webm;codecs=vp8';
    }
    if (MediaRecorder.isTypeSupported('video/mp4;codecs=h264')) {
      return 'video/mp4;codecs=h264';
    }
    return null;
  }
}
```

#### Task 3.2: iOS Safari Fallback

```javascript
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);

if (isIOS) {
  // Use H.264 codec (better iOS support)
  recorderConfig.mimeType = 'video/mp4;codecs=h264';

  // Reduce bitrate
  recorderConfig.videoBitsPerSecond = 5000000;  // 5 Mbps

  // Disable audio (iOS limitation)
  recorderConfig.disableAudio = true;

  // Show notice
  console.warn('iOS detected - audio preview not available');
}
```

#### Task 3.3: Memory Management

**File to Create**: `app/frontend/src/utils/MemoryManager.js`

```javascript
export class MemoryManager {
  constructor() {
    this.objectUrls = [];
    this.canvasCache = new Map();
    this.maxCacheSize = 10;
  }

  createObjectUrl(blob) {
    const url = URL.createObjectURL(blob);
    this.objectUrls.push(url);
    return url;
  }

  revokeAll() {
    this.objectUrls.forEach(url => URL.revokeObjectURL(url));
    this.objectUrls = [];
  }

  cacheCanvas(key, canvas) {
    if (this.canvasCache.size >= this.maxCacheSize) {
      const firstKey = this.canvasCache.keys().next().value;
      this.canvasCache.delete(firstKey);
    }
    this.canvasCache.set(key, canvas);
  }

  cleanup() {
    this.revokeAll();
    this.canvasCache.clear();
  }
}
```

---

### Week 4: Testing & Feature Flag Rollout

#### Task 4.1: Feature Flag Implementation

**File to Create**: `app/config.py` (add to existing)

```python
# Preview feature flag
PREVIEW_ENABLED_PRESETS = [
    'carousel_illustrated',
    'single_image_stat',
    'reel_hype'
]

def should_enable_preview(preset_id: str, user_id: int = None) -> bool:
    """
    Determine if preview mode should be enabled.

    Args:
        preset_id: Preset identifier
        user_id: Optional user ID for beta testing

    Returns:
        True if preview should be enabled
    """
    # Check preset whitelist
    if preset_id not in PREVIEW_ENABLED_PRESETS:
        return False

    # Check browser compatibility (would be done client-side)
    return True
```

#### Task 4.2: End-to-End Test

**Manual Test Checklist**:

1. **Preview Generation**:
   - [ ] Select carousel preset
   - [ ] Click "Generate Preview"
   - [ ] Wait for L5 completion (~60s)
   - [ ] Preview renders in browser (< 10s)
   - [ ] Video plays with audio sync

2. **Adjustment Flow**:
   - [ ] Adjust text size slider
   - [ ] Re-preview renders (~5s)
   - [ ] Verify text size changed

3. **Approval Flow**:
   - [ ] Click "Approve & Render Final"
   - [ ] L6 starts running
   - [ ] Final video downloads
   - [ ] Final matches preview

4. **Browser Compatibility**:
   - [ ] Test on Chrome (desktop)
   - [ ] Test on Firefox (desktop)
   - [ ] Test on Safari (desktop)
   - [ ] Test on iOS Safari
   - [ ] Test on Android Chrome

---

## Package Dependencies

**Add to `app/frontend/package.json`**:

```json
{
  "dependencies": {
    "recordrtc": "^5.6.2",
    "html2canvas": "^1.4.1"
  }
}
```

**Install**:
```bash
cd app/frontend
npm install recordrtc html2canvas
```

---

## Success Criteria

**Quantitative**:
- ✅ Preview generation time: **< 10 seconds** (vs 2-5 minutes full render)
- ✅ Preview approval rate: **> 70%** (users approve vs adjust)
- ✅ Final render invocations: **-60%** (fewer re-runs)
- ✅ Browser support: **> 90%** (with fallbacks)
- ✅ Audio sync drift: **< 100ms**

**Qualitative**:
- ✅ Preview quality sufficient for approval decisions
- ✅ Adjustment controls intuitive
- ✅ Final output matches preview
- ✅ Workflow feels like Google AI Studio

---

## Verification Checklist

**Before Marking Phase 2 Complete**:

**Functionality**:
- [ ] Preview renders successfully for all enabled presets
- [ ] Audio sync is accurate
- [ ] Text overlays render correctly
- [ ] Logo overlay positioning works
- [ ] Approval triggers L6 correctly
- [ ] Adjustments apply to final render

**Performance**:
- [ ] Preview generation < 10 seconds
- [ ] No memory leaks after 10 previews
- [ ] Browser doesn't hang during rendering

**Compatibility**:
- [ ] Works on Chrome 100+
- [ ] Works on Firefox 100+
- [ ] Works on Safari 15+
- [ ] Fallback works on iOS Safari
- [ ] Graceful degradation on old browsers

**User Experience**:
- [ ] Clear progress indicators
- [ ] Helpful error messages
- [ ] Can cancel preview generation
- [ ] Can download preview as-is
- [ ] Adjustment controls are intuitive

---

## Risk Mitigation

**High Risk**: Browser memory leaks

**Mitigation**:
- MemoryManager cleanup after each preview
- Aggressive URL.revokeObjectURL()
- Canvas cache size limits

**Medium Risk**: Audio sync drift

**Mitigation**:
- Use Web Audio API precise timing
- Fallback to muted preview on iOS
- Show sync drift warning if detected

**Low Risk**: Preview quality too low

**Mitigation**:
- Configurable bitrate (8 Mbps default)
- Allow preview download for manual review

---

## Future Enhancements (Post-Phase 2)

1. **Real-time Collaboration**: Multiple users preview same job
2. **A/B Testing**: Generate 2-3 variations, preview all, pick winner
3. **Smart Suggestions**: AI recommends text adjustments
4. **Version History**: Save preview snapshots
5. **Batch Preview**: Queue multiple presets, batch approve
6. **Export Preview**: Download preview as final (skip L6)
7. **Vision Feedback**: AI analyzes preview quality

---

## Conclusion

Phase 2 delivers the "Google AI Studio experience" - instant visual feedback, rapid iteration, and confidence before committing to expensive production renders. Combined with Phase 1's reliability foundation, this creates a professional-grade content generation platform.

**Recommended Next Steps**: Complete Phase 1 first (3-4 weeks), validate 95%+ success rate, then proceed to Phase 2 implementation.
