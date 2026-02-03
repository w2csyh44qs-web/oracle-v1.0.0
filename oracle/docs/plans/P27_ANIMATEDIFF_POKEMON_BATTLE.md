# P27: AnimateDiff + RIFE Hybrid Pokemon Battle Animation

**Status:** IN PROGRESS - OPTIMIZED FOR M2 MAC
**Created:** January 9, 2026
**Updated:** January 9, 2026
**Context:** Dev (D105)

## Latest Optimizations (VRAM Savings)

| Change | Before | After | VRAM Savings |
|--------|--------|-------|--------------|
| Resolution | 512x384 | 384x288 | ~44% less |
| PixelArt | In ComfyUI pipeline | FFmpeg post-process | ~15-20% less |
| **Total** | ~8-12GB VRAM | ~5-7GB VRAM | ~50% reduction |

**Note:** 384x288 still looks crisp on phone screens - pixel art scales well.

---

## ⚠️ IMPLEMENTATION ISSUE DISCOVERED

The initial implementation attempted but **failed** due to missing components. The generated output was:
- ❌ Completely different characters (not the Jaguar/Buffalo from slides)
- ❌ Garbled/unreadable text
- ❌ No actual motion - just noise/flicker
- ❌ Lost pixel art aesthetic

### Root Cause Analysis

| What We Did (Wrong) | What Should Be Done |
|---------------------|---------------------|
| No IP-Adapter | Must use IP-Adapter to feed slide as "visual prompt" for mascot consistency |
| Basic ControlNet | Must use temporal weighting - blend Canny edges from Start→End |
| No PixelArt Detector | Must apply AFTER RIFE to re-pixelate output |
| img2img approach | Must use Slide A → Slide B bridging with 2 input images |
| Missing CLIP Vision model | Required for IP-Adapter (~2.5GB download) |

### What's Already Installed in ~/ComfyUI

| Component | Status | Used? |
|-----------|--------|-------|
| ComfyUI-AnimateDiff-Evolved | ✅ Installed | ✅ |
| ComfyUI-Frame-Interpolation (RIFE) | ✅ Installed | ✅ |
| ComfyUI_IPAdapter_plus | ✅ Installed | ❌ NOT USED |
| ComfyUI-PixelArt-Detector | ✅ Installed | ❌ NOT USED |
| ControlNet Canny v1.1 | ✅ Installed | ⚠️ Poorly used |
| IP-Adapter SD1.5 model | ✅ Installed | ❌ NOT USED |
| CLIP Vision model | ❌ MISSING | Required for IP-Adapter |
| All-In-One Pixel Model | ✅ Installed | ✅ |
| LCM LoRA SD1.5 | ✅ Installed | ✅ |
| Motion Module v2 | ✅ Installed | ✅ |

---

## Problem Statement

RIFE alone only interpolates pixels between frames - it creates crossfade/morph effects, not actual motion. For Pokemon-style battles, we need:
- **Attack motion**: Jaguar pouncing/striking (slides 1→2→3)
- **Reaction motion**: Buffalo flinching, falling, fainting (slides 3→4)

RIFE can't "understand" that a Jaguar should leap - it just fades one position into another, creating ghosting artifacts.

## Solution: Hybrid Workflow

**AnimateDiff** generates the motion (low FPS) → **RIFE** upsamples to smooth video (high FPS)

### Why This Works on M2 Pro

| Step | Tool | FPS | Time | VRAM |
|------|------|-----|------|------|
| Motion Generation | AnimateDiff + LCM | 8 fps | ~1-2 min | ~8-12 GB |
| Frame Interpolation | RIFE | 8→30 fps (4x) | ~10 sec | ~2 GB |
| **Total** | | 30 fps output | ~2 min | |

Without LCM: AnimateDiff at 30fps would take 10-20 minutes and likely crash.
With LCM: 4 inference steps instead of 30 = 7-8x faster.

---

## Installation Plan

### Step 1: Install ComfyUI (M2 Mac)

```bash
# Clone ComfyUI
cd ~/
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Create venv with Python 3.10+
python3 -m venv venv
source venv/bin/activate

# Install PyTorch with MPS support
pip install torch torchvision torchaudio

# Install ComfyUI requirements
pip install -r requirements.txt

# Launch with M2 optimizations
python main.py --force-fp16 --highvram
```

### Step 2: Install ComfyUI Manager

```bash
cd ~/ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

Then in ComfyUI UI: Manager → Install Custom Nodes

### Step 3: Install AnimateDiff-Evolved

Via ComfyUI Manager, search and install:
- `ComfyUI-AnimateDiff-Evolved`

Download motion modules:
- `mm_sd_v15_v2.ckpt` (recommended for quality)
- `mm_sdxl_v10_beta.safetensors` (if using SDXL)

Place in: `~/ComfyUI/custom_nodes/ComfyUI-AnimateDiff-Evolved/models/`

### Step 4: Install LCM LoRA (Speed Boost)

Download LCM LoRA for faster generation:
- `lcm-lora-sdv1-5.safetensors` from HuggingFace

Place in: `~/ComfyUI/models/loras/`

Settings in workflow:
- Sampler: `lcm`
- Steps: 4-8 (instead of 25-30)
- CFG: 1.5-2.0 (lower for LCM)

### Step 5: Install RIFE VFI Node

Via ComfyUI Manager, search and install:
- `ComfyUI-Frame-Interpolation`

This adds the `RIFE VFI` node for frame interpolation.

### Step 6: Install IP-Adapter (Character Consistency)

Via ComfyUI Manager:
- `ComfyUI_IPAdapter_plus`

Download IP-Adapter models:
- `ip-adapter_sd15.safetensors`
- `ip-adapter-plus_sd15.safetensors` (better quality)

Place in: `~/ComfyUI/models/ipadapter/`

---

## CORRECTED Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SLIDE A → SLIDE B TRANSITION                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐     ┌──────────────┐                              │
│  │ Load Slide A │     │ Load Slide B │                              │
│  │ (e.g. Jaguar)│     │ (e.g. Attack)│                              │
│  └──────┬───────┘     └──────┬───────┘                              │
│         │                    │                                       │
│         ▼                    ▼                                       │
│  ┌──────────────┐     ┌──────────────┐                              │
│  │ Canny Edges  │     │ Canny Edges  │                              │
│  │ (Start)      │     │ (End)        │                              │
│  └──────┬───────┘     └──────┬───────┘                              │
│         │                    │                                       │
│         └────────┬───────────┘                                       │
│                  ▼                                                   │
│         ┌───────────────────┐                                        │
│         │ Temporal Blending │  ← Frame 0: 100% Start                │
│         │ (16 frames)       │  ← Frame 16: 100% End                 │
│         └────────┬──────────┘                                        │
│                  │                                                   │
│  ┌───────────────┼───────────────┐                                  │
│  │               ▼               │                                  │
│  │      ┌───────────────┐        │                                  │
│  │      │ IP-Adapter    │ ← Feed Slide A as "visual prompt"        │
│  │      │ (Consistency) │   to maintain mascot appearance          │
│  │      └───────┬───────┘        │                                  │
│  │              │                │                                  │
│  │              ▼                │                                  │
│  │      ┌───────────────┐        │                                  │
│  │      │ ControlNet    │ ← Use blended Canny to guide motion      │
│  │      │ Apply         │                                          │
│  │      └───────┬───────┘        │                                  │
│  │              │                │                                  │
│  │              ▼                │                                  │
│  │      ┌───────────────┐        │                                  │
│  │      │ AnimateDiff   │ ← LCM LoRA, 6 steps, 8fps               │
│  │      │ KSampler      │   "pixelsprite, 8-bit, pounce"          │
│  │      └───────┬───────┘        │                                  │
│  │              │                │                                  │
│  └──────────────┼────────────────┘                                  │
│                 ▼                                                    │
│         ┌───────────────┐                                           │
│         │ VAE Decode    │                                           │
│         └───────┬───────┘                                           │
│                 ▼                                                    │
│         ┌───────────────┐                                           │
│         │ RIFE VFI 4x   │ ← 16 frames @ 8fps → 64 frames @ 32fps   │
│         └───────┬───────┘                                           │
│                 ▼                                                    │
│         ┌───────────────┐                                           │
│         │ Save Video    │ ← Save from RIFE output (ComfyUI done)   │
│         └───────┬───────┘                                           │
│                 ▼                                                    │
│         ┌───────────────┐                                           │
│         │ FFmpeg Post-  │ ← Re-pixelate via downscale→upscale      │
│         │ Process       │   + color quantization (saves VRAM!)      │
│         └───────────────┘                                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Differences from Failed Implementation

1. **IP-Adapter** - Uses slide image as "visual prompt" → mascot appearance stays consistent
2. **Temporal ControlNet** - Blends Canny edges from Start→End across frames → motion follows structure
3. **PixelArt Detector at END** - Re-pixelates RIFE output → restores 8-bit crispness
4. **Two input images** - Slide A and Slide B guide the transition → not random generation

---

## Pixel Art Preservation

### The Problem
Standard AnimateDiff + diffusion tends to smooth/blur pixel art, losing the retro aesthetic.

### Solutions

1. **Use Pixel Art Checkpoint**
   - Download from Civitai: "Pixel Art XL" or "Retro Anime" checkpoints
   - These are trained on pixel art and maintain the style

2. **ControlNet with Canny Edge**
   - Add ControlNet (Canny) to lock the pixel boundaries
   - Prevents the AI from "inventing" smooth gradients

3. **Low Denoise Strength**
   - Use denoise 0.3-0.5 instead of full 1.0
   - Preserves more of the original pixel structure

4. **Post-Processing: Nearest Neighbor**
   - After generation, resize using NEAREST (not LANCZOS)
   - Optionally run through a "pixelization" filter

---

## ComfyUI Workflow JSON

Save this as `pokemon_battle_workflow.json` in ComfyUI:

```json
{
  "_comment": "Pokemon Battle AnimateDiff + RIFE Workflow",
  "nodes": [
    {"id": 1, "type": "LoadImage", "title": "Slide 1 (Start)"},
    {"id": 2, "type": "LoadImage", "title": "Slide 2 (Attack)"},
    {"id": 3, "type": "IPAdapterEncode", "title": "Lock Character"},
    {"id": 4, "type": "AnimateDiffLoader", "title": "Motion Module"},
    {"id": 5, "type": "AnimateDiffSampler", "title": "Generate Motion"},
    {"id": 6, "type": "RIFE_VFI", "title": "Upsample 4x"},
    {"id": 7, "type": "VideoCombine", "title": "Export MP4"}
  ],
  "_full_workflow": "TODO: Export from ComfyUI after setup"
}
```

---

## Integration with Pipeline

### Option A: ComfyUI as External Service

```python
# In _L6/processors/animatediff_processor.py

class AnimateDiffProcessor:
    """Call ComfyUI API for AnimateDiff generation."""

    def __init__(self, comfyui_url: str = "http://localhost:8188"):
        self.api_url = comfyui_url

    def generate_battle_animation(
        self,
        slides: List[str],
        output_path: str,
        motion_prompts: Dict[str, str]
    ) -> str:
        """Generate battle animation via ComfyUI API."""
        # Load workflow JSON
        # Queue prompt via /prompt endpoint
        # Poll for completion
        # Download result
        pass
```

### Option B: Direct Python Integration

```python
# Requires ComfyUI installed in same venv
from comfy.samplers import KSampler
from comfy_extras.nodes_animatediff import AnimateDiffLoader
# ... complex setup
```

**Recommendation:** Option A (API) is cleaner and doesn't pollute the main venv.

---

## Estimated Performance (M2 Pro 16GB)

| Component | Time | Notes |
|-----------|------|-------|
| AnimateDiff (8fps, 32 frames) | 60-120 sec | With LCM LoRA |
| RIFE 4x upsample | 10-15 sec | Very fast on Neural Engine |
| Video encoding | 5 sec | FFmpeg |
| **Total** | **~2 minutes** | Per battle animation |

Without LCM: 10-20 minutes (not practical)

---

## Files to Modify/Create

| File | Action | Purpose |
|------|--------|---------|
| `_L6/processors/animatediff_processor.py` → `comfyui_processor.py` | RENAME + REWRITE | ComfyUI API with IP-Adapter + ControlNet + PixelArt |
| `_L6/processors/__init__.py` | UPDATE | Export `ComfyUIProcessor` |
| `config/comfyui_workflows/pokemon_battle_correct.json` | CREATE | Corrected workflow template |
| `config/script_presets.json` | UPDATE | Change tool ref to `comfyui` |
| `~/ComfyUI/models/clip_vision/` | DOWNLOAD | CLIP Vision model for IP-Adapter (~2.5GB) |

---

## Execution Steps

### Step 1: Download Missing CLIP Vision Model
```bash
mkdir -p ~/ComfyUI/models/clip_vision
cd ~/ComfyUI/models/clip_vision
curl -L -o "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors" \
  "https://huggingface.co/h94/IP-Adapter/resolve/main/models/image_encoder/model.safetensors"
```

### Step 2: Rename Processor
```bash
cd app/core/pipeline/layers/_L6/processors/
mv animatediff_processor.py comfyui_processor.py
```

### Step 3: Rewrite comfyui_processor.py with Correct Workflow
- Add IP-Adapter nodes
- Add temporal ControlNet blending
- Add PixelArt Detector after RIFE
- Update class name to `ComfyUIProcessor`

### Step 4: Update Launch Flags
```bash
# Add --gpu-only to ComfyUI startup
python main.py --force-fp16 --gpu-only --highvram
```

### Step 5: Test Workflow
```bash
python3 app/core/pipeline/layers/_L6/processors/comfyui_processor.py --test
```

---

## Current State

**Installed (in ~/ComfyUI):**
- [x] ComfyUI with Python 3.11 venv
- [x] AnimateDiff-Evolved custom node
- [x] Frame-Interpolation (RIFE) custom node
- [x] IPAdapter_plus custom node
- [x] PixelArt-Detector custom node
- [x] VideoHelperSuite custom node
- [x] All-In-One Pixel Model checkpoint
- [x] LCM LoRA SD1.5
- [x] Motion Module v2
- [x] ControlNet Canny v1.1
- [x] IP-Adapter SD1.5 model
- [x] RIFE 4.7 model
- [ ] CLIP Vision model (MISSING - REQUIRED)

**Code Created (but needs correction):**
- [x] `animatediff_processor.py` - EXISTS but missing IP-Adapter, PixelArt Detector
- [x] `pokemon_battle_animated` preset in script_presets.json
- [x] Battle audio mixer and audio files

**TODO (P27 Corrected):**
- [ ] Download CLIP Vision model (~2.5GB)
- [ ] Rename `animatediff_processor.py` → `comfyui_processor.py`
- [ ] Rewrite processor with IP-Adapter + ControlNet temporal + PixelArt Detector
- [ ] Update `__init__.py` exports
- [ ] Update preset config tool reference
- [ ] Add `--gpu-only` to launch flags
- [ ] Test with actual slides

---

## References

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [AnimateDiff-Evolved](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved)
- [LCM LoRA](https://huggingface.co/latent-consistency/lcm-lora-sdv1-5)
- [ComfyUI-Frame-Interpolation](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation)
- [IP-Adapter](https://github.com/cubiq/ComfyUI_IPAdapter_plus)
