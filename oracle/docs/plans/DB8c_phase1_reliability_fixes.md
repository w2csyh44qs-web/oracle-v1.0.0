# Phase 1: Pipeline Reliability Overhaul (Audit-Driven)

**Session:** DB8c - Phase 1
**Date:** January 29, 2026
**Status:** PLANNING
**Timeline:** 4 weeks
**Scope:** Fix 87 critical reliability issues discovered in comprehensive code audit

---

## Executive Summary

Comprehensive audit identified **87 critical reliability issues** across L3/L5/L6 pipeline layers that cause "job says complete but output is wrong/missing" silent failures. This plan addresses the **actual issues found**, not theoretical ones, while respecting existing architecture (PipelineContext, orchestrator, adapters).

**Key Finding**: Pipeline uses 3 anti-patterns:
1. **Silent failures** - Functions return empty lists/None without error indication (106 instances)
2. **No validation** - File I/O proceeds without checking results (46 instances)
3. **Print-based debugging** - 242 print() calls instead of structured logging

**Approach**: Fix issues in user priority order (L3 → L5 → L6), add logging first (Week 1 Day 1), implement validation patterns, eliminate silent failures.

---

## Current State: Audit Results

### Issues by Category (87 Total)

| Category | Count | Impact |
|----------|-------|--------|
| Print statements (should be logging) | 242 | No observability in production |
| Silent fallback returns | 106 | "Success" when actually failed |
| Missing file I/O validation | 46 | Corrupt/missing files go undetected |
| Missing return value checks | 42 | Callers don't validate success/failure |
| Bare exception handlers | 29 | Errors swallowed without context |
| API calls without retry logic | 16 | Transient failures become permanent |

### Issues by Layer (User Priority Order)

**L3 - Ideas Generation** (Priority 1):
- `L3_ideas.py`: 22 prints, 18 silent fallbacks, 11 file I/O issues, 4 bare excepts
- `l3_adapter.py`: 2 silent fallbacks, 2 file I/O issues
- **Critical**: Empty ideas list returned for 5 different error conditions (file missing, corrupt JSON, no trends, API failure, matchup mismatch)

**L5 - Media Generation** (Priority 2):
- `L5_media.py`: 126 prints, 58 silent fallbacks, 19 file I/O issues, 12 bare excepts
- `l5_adapter.py`: 2 silent fallbacks, 1 file I/O issue
- **Critical**: AI image generation (Flux, DALL-E, Gemini) returns None on first failure, no retry. Media packages marked "ready_for_assembly" without validating files exist.

**L6 - Video Assembly** (Priority 3):
- `L6_assembly.py`: 94 prints, 24 silent fallbacks, 12 file I/O issues, 10 bare excepts
- `l6_adapter.py`: 2 silent fallbacks, 1 file I/O issue
- **Critical**: Carousel assembly returns None on failure but marked as "assembled" anyway. Logo overlay fails silently. MoviePy rendering has no timeout protection.

### Top 5 Critical Issues (From Audit)

1. **L3 line 863-880 + L5 line 502-565 + L6 line 317-330**: Empty lists returned for all errors
   - User experiences: "All layers complete!" but output directory empty

2. **L5 line 937-1530**: AI image generation no retry/fallback
   - User experiences: Carousel with 2/3 images, looks broken

3. **L5 line 2900-2924**: "ready_for_assembly" set without file validation
   - User experiences: L6 fails with "FileNotFoundError"

4. **L6 line 1794-1879**: Carousel returns None but marked as complete
   - User experiences: Missing slides, wrong aspect ratio

5. **L6 line 584-618**: Audio/background preparation returns None, used as path
   - User experiences: L6 crashes with "NoneType object not subscriptable"

---

## Implementation Plan

### Week 1: Foundation + L3 Fixes

**Day 1: Setup Structured Logging** (CRITICAL - DO FIRST)

**File to Create**: `app/core/utils/logging_config.py`

```python
import logging
import sys
from pathlib import Path
from contextvars import ContextVar
from datetime import datetime

# Context variables for correlation
job_context: ContextVar[str] = ContextVar('job_id', default='no-job')
layer_context: ContextVar[str] = ContextVar('layer', default='no-layer')

class JobContextFilter(logging.Filter):
    """Add job_id and layer to all log records."""
    def filter(self, record):
        record.job_id = job_context.get()
        record.layer = layer_context.get()
        return True

def setup_pipeline_logging(log_level: str = 'INFO'):
    """
    Configure structured logging for pipeline.

    Outputs to:
    - logs/pipeline.log (all messages)
    - logs/errors.log (errors only)
    - Terminal (info and above, with colors)
    """
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)

    # Format with correlation IDs
    log_format = (
        '%(asctime)s | %(job_id)s | %(layer)s | '
        '%(name)s | %(levelname)s | %(message)s'
    )

    # File handler (all logs)
    file_handler = logging.FileHandler('logs/pipeline.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.addFilter(JobContextFilter())

    # Error file handler
    error_handler = logging.FileHandler('logs/errors.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))
    error_handler.addFilter(JobContextFilter())

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter(log_format))
    console_handler.addFilter(JobContextFilter())

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=[file_handler, error_handler, console_handler]
    )

    logging.info("Pipeline logging configured")

class ColoredFormatter(logging.Formatter):
    """Add colors to console output."""
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)

# Context managers for setting correlation IDs
class JobContext:
    """Context manager for setting job_id in logs."""
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.token = None

    def __enter__(self):
        self.token = job_context.set(self.job_id)
        return self

    def __exit__(self, *args):
        job_context.reset(self.token)

class LayerContext:
    """Context manager for setting layer in logs."""
    def __init__(self, layer: str):
        self.layer = layer
        self.token = None

    def __enter__(self):
        self.token = layer_context.set(self.layer)
        return self

    def __exit__(self, *args):
        layer_context.reset(self.token)
```

**Initialize in orchestrator.py**:
```python
from app.core.utils.logging_config import setup_pipeline_logging, JobContext, LayerContext

# At module level (run once)
setup_pipeline_logging()

# In run() method
def run(self, stop_after: Optional[str] = None) -> PipelineContext:
    with JobContext(self.job_id):
        logger.info(f"Starting pipeline for job {self.job_id}")

        for layer in self.layers_to_run:
            with LayerContext(layer):
                logger.info(f"Running {layer}")
                # ... execute layer
```

**Day 2-3: Fix L3_ideas.py Print Statements + Silent Fallbacks**

**Files to Modify**: `app/core/pipeline/layers/_L3/L3_ideas.py`

**Pattern 1: Replace print() with logger**

```python
# BEFORE (22 instances)
print(f"⚠️  Could not load presets: {e}")
print(f"✗ Unexpected error: {e}")

# AFTER
logger = logging.getLogger(__name__)
logger.warning(f"Could not load presets: {e}", exc_info=True)
logger.error(f"Unexpected error in idea generation: {e}", exc_info=True)
```

**Pattern 2: Fix silent fallback returns (18 instances)**

```python
# BEFORE (line 116-118)
def _load_presets(self):
    try:
        with open(SCRIPT_PRESETS_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Could not load: {e}")
        return self._get_fallback_presets()  # Silent fallback

# AFTER
def _load_presets(self):
    try:
        with open(SCRIPT_PRESETS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.info("Presets file not found, using fallback defaults")
        return self._get_fallback_presets()
    except json.JSONDecodeError as e:
        logger.error(f"Presets file corrupted: {e}", exc_info=True)
        raise ValueError(f"Cannot load presets: file corrupted at {SCRIPT_PRESETS_PATH}")
    except Exception as e:
        logger.error(f"Unexpected error loading presets: {e}", exc_info=True)
        raise
```

**Pattern 3: Fix empty list returns (critical)**

```python
# BEFORE (line 863-880)
def load_trends(self):
    try:
        with open(all_trends_file, 'r') as f:
            data = json.load(f)
            return data.get('trends', [])
    except:
        return []  # 5 different error types all return same empty list

# AFTER
def load_trends(self):
    if not os.path.exists(all_trends_file):
        raise FileNotFoundError(
            f"Trends file not found: {all_trends_file}. "
            f"Run web_search_trend_detector.py first."
        )

    try:
        with open(all_trends_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Trends file corrupted: {e}")

    trends = data.get('trends', [])
    if not trends:
        raise ValueError("Trends file exists but contains no trends")

    logger.info(f"Loaded {len(trends)} trends from {all_trends_file}")
    return trends
```

**Day 4-5: Fix L3 File I/O + Return Value Checks**

**Pattern 4: Add post-write validation**

```python
# BEFORE (line 1532-1533)
def save_approved_ideas(self, ideas):
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    return output_file  # Returns even if write failed

# AFTER
def save_approved_ideas(self, ideas):
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    # Validate write succeeded
    if not os.path.exists(output_file):
        raise IOError(f"File write failed: {output_file}")

    file_size = os.path.getsize(output_file)
    if file_size == 0:
        raise IOError(f"File write produced 0 bytes: {output_file}")

    # Validate content is parseable
    try:
        with open(output_file, 'r') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        raise IOError(f"Written file is not valid JSON: {e}")

    logger.info(f"Saved {len(ideas)} approved ideas ({file_size} bytes)")
    return output_file
```

**Pattern 5: Add API retry logic**

```python
# BEFORE (line 309-415)
def fetch_goatedbets_matchup(self, matchup):
    try:
        response = requests.get(endpoint, timeout=30)
        return response.json()
    except:
        print("API failed")
        return None

# AFTER
from app.core.utils.retry_utils import retry_http

@retry_http(max_attempts=3, base_delay=2.0)
def fetch_goatedbets_matchup(self, matchup):
    try:
        response = requests.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as e:
        logger.warning(f"GoatedBets API timeout: {e}")
        raise  # Will be retried by decorator
    except requests.HTTPError as e:
        logger.error(f"GoatedBets API HTTP error: {e.response.status_code}")
        raise
```

**New File to Create**: `app/core/utils/retry_utils.py`

```python
import time
import random
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def retry_http(max_attempts: int = 3, base_delay: float = 2.0):
    """Retry HTTP requests with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                        raise

                    # Exponential backoff with jitter
                    delay = min(base_delay * (2 ** (attempt - 1)), 60.0)
                    delay *= (0.5 + random.random())

                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}), "
                        f"retrying in {delay:.2f}s: {e}"
                    )
                    time.sleep(delay)
        return wrapper
    return decorator
```

---

### Week 2: L5 Media Generation Fixes

**Day 1-2: Fix L5_media.py Print Statements**

**Files to Modify**: `app/core/pipeline/layers/_L5/L5_media.py`

Replace 126 print() calls with logger calls. Use pattern from Week 1.

**Day 3: Fix AI Image Generation - Add Retry + Fallback Chain**

**Critical Fix** (lines 937-1530):

```python
# BEFORE
def _generate_flux(self, prompt):
    try:
        response = fal_client.submit(...)
        return result_url
    except:
        print("Flux failed")
        return None  # First failure, no retry

# AFTER
def _generate_image_with_fallback(self, prompt, idea_id):
    """Generate image with fallback chain: Flux → DALL-E → Pexels stock."""

    # Try Flux (3 attempts)
    for attempt in range(3):
        try:
            logger.info(f"Attempting Flux generation (attempt {attempt + 1}/3)")
            result = self._generate_flux(prompt)
            if result:
                logger.info(f"Flux succeeded on attempt {attempt + 1}")
                return result
        except Exception as e:
            logger.warning(f"Flux attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)  # 1s, 2s, 4s backoff

    # Fallback to DALL-E
    logger.info("Flux exhausted, trying DALL-E")
    try:
        result = self._generate_dalle(prompt)
        if result:
            logger.info("DALL-E succeeded")
            return result
    except Exception as e:
        logger.warning(f"DALL-E failed: {e}")

    # Fallback to Pexels stock
    logger.info("DALL-E failed, trying Pexels stock")
    try:
        search_query = self._extract_search_query(prompt)
        result = self.search_pexels(search_query, limit=1)
        if result:
            logger.info(f"Pexels stock found: {search_query}")
            return result[0]
    except Exception as e:
        logger.warning(f"Pexels failed: {e}")

    # All methods failed
    logger.error(f"All image generation methods failed for idea {idea_id}")
    raise MediaGenerationError(f"Could not generate image for: {prompt}")
```

**Day 4: Fix "ready_for_assembly" Flag Without Validation**

**Critical Fix** (lines 2900-2924):

```python
# BEFORE
media_package['ready_for_assembly'] = True  # Set always

# AFTER
def _validate_media_package(self, package):
    """Validate all required files exist and are valid."""
    errors = []

    # Check background image
    bg_path = package.get('background_path')
    if bg_path:
        if not os.path.exists(bg_path):
            errors.append(f"Background missing: {bg_path}")
        elif os.path.getsize(bg_path) == 0:
            errors.append(f"Background is 0 bytes: {bg_path}")

    # Check carousel slides
    slides = package.get('carousel_slides', [])
    if slides:
        for idx, slide in enumerate(slides):
            slide_path = slide.get('image_path')
            if not slide_path:
                errors.append(f"Slide {idx} missing image_path")
            elif not os.path.exists(slide_path):
                errors.append(f"Slide {idx} image missing: {slide_path}")
            elif os.path.getsize(slide_path) == 0:
                errors.append(f"Slide {idx} image is 0 bytes: {slide_path}")

    # Check audio if present
    audio_path = package.get('audio_path')
    if audio_path:
        if not os.path.exists(audio_path):
            errors.append(f"Audio missing: {audio_path}")
        elif os.path.getsize(audio_path) < 1000:  # Less than 1KB
            errors.append(f"Audio file too small: {audio_path}")

    if errors:
        logger.error(f"Media package validation failed:\n" + "\n".join(errors))
        return False, errors

    return True, []

# Usage
valid, errors = self._validate_media_package(media_package)
if valid:
    media_package['ready_for_assembly'] = True
    logger.info(f"Media package validated: {media_package['idea_id']}")
else:
    media_package['ready_for_assembly'] = False
    media_package['validation_errors'] = errors
    logger.error(f"Media package invalid: {media_package['idea_id']}")
```

**Day 5: Fix L5 File I/O + load_ideas() Empty List Returns**

**Critical Fix** (lines 502-565):

```python
# BEFORE
def load_ideas(self, preset=None, matchup=None):
    try:
        with open(ideas_file, 'r') as f:
            data = json.load(f)
            return data.get('ideas', [])
    except:
        return []  # File missing, corrupt JSON, empty ideas all return same

# AFTER
def load_ideas(self, preset=None, matchup=None):
    """Load ideas with explicit error handling."""

    # Validate file exists
    if not os.path.exists(ideas_file):
        raise FileNotFoundError(
            f"Ideas file not found: {ideas_file}. "
            f"Run L3 ideas generation first."
        )

    # Load and validate JSON
    try:
        with open(ideas_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ideas file corrupted: {e}")

    # Validate structure
    if not isinstance(data, dict):
        raise ValueError(f"Ideas file has invalid structure: expected dict, got {type(data)}")

    ideas = data.get('ideas', [])

    # Validate preset match (if specified)
    loaded_preset = data.get('metadata', {}).get('preset')
    if preset and loaded_preset and loaded_preset != preset:
        raise ValueError(
            f"Preset mismatch: expected '{preset}', file has '{loaded_preset}'. "
            f"Re-run L3 with correct preset."
        )

    # Validate matchup match (if specified)
    cached_matchup = data.get('metadata', {}).get('matchup')
    if matchup and cached_matchup and cached_matchup != matchup:
        raise ValueError(
            f"Matchup mismatch: expected '{matchup}', file has '{cached_matchup}'. "
            f"Re-run L3 for correct matchup."
        )

    # Validate ideas not empty
    if not ideas:
        raise ValueError(
            f"Ideas file exists but contains no ideas. "
            f"Check L3 output or re-run idea generation."
        )

    logger.info(f"Loaded {len(ideas)} ideas (preset: {loaded_preset}, matchup: {cached_matchup})")
    return ideas
```

---

### Week 3: L6 Assembly Fixes + Code Consolidation

**Day 1-2: Fix L6_assembly.py Print Statements + Silent Fallbacks**

**Files to Modify**: `app/core/pipeline/layers/_L6/L6_assembly.py`

Replace 94 print() calls with logger. Fix 24 silent fallback returns using patterns from Weeks 1-2.

**Day 3: Fix Carousel Assembly - Validate Prerequisites**

**Critical Fix** (lines 1794-1879):

```python
# BEFORE
def _assemble_carousel_reels(self, package):
    carousel_slides = package.get('carousel_slides', [])
    if not carousel_slides:
        print("❌ No carousel slides")
        return None  # Fails silently
    # ... assembly continues

# AFTER
def _assemble_carousel_reels(self, package):
    """Assemble carousel with comprehensive validation."""

    # Validate prerequisites
    carousel_slides = package.get('carousel_slides', [])
    if not carousel_slides:
        raise AssemblyError(
            f"Cannot assemble carousel: no slides in package {package['idea_id']}"
        )

    # Validate all slide files exist
    missing_slides = []
    for idx, slide in enumerate(carousel_slides):
        slide_path = slide.get('image_path')
        if not slide_path or not os.path.exists(slide_path):
            missing_slides.append(f"Slide {idx}: {slide_path or 'no path'}")

    if missing_slides:
        raise AssemblyError(
            f"Carousel slides missing:\n" + "\n".join(missing_slides)
        )

    # Validate audio if needed
    audio_path = package.get('audio_path')
    if audio_path and not os.path.exists(audio_path):
        raise AssemblyError(f"Audio file missing: {audio_path}")

    logger.info(f"Assembling carousel: {len(carousel_slides)} slides")

    try:
        # ... assembly logic
        result = self._render_carousel(carousel_slides, audio_path)

        # Validate output
        if not os.path.exists(result):
            raise AssemblyError(f"Carousel render failed: output missing")

        if os.path.getsize(result) < 10000:  # Less than 10KB
            raise AssemblyError(f"Carousel render failed: output too small ({os.path.getsize(result)} bytes)")

        logger.info(f"Carousel assembled: {result} ({os.path.getsize(result)} bytes)")
        return result

    except Exception as e:
        logger.error(f"Carousel assembly failed: {e}", exc_info=True)
        raise AssemblyError(f"Carousel assembly failed: {e}")
```

**Day 4: Fix Logo Overlay + Audio/Background Preparation**

**Fix None returns** (lines 584-618, 1854-1879):

```python
# BEFORE
def _get_audio_file(self, package):
    audio_path = package.get('audio_path')
    if not os.path.exists(audio_path):
        return None, None  # Returns tuple of Nones

# AFTER
def _get_audio_file(self, package):
    """Get audio file with validation."""
    audio_path = package.get('audio_path')

    if not audio_path:
        raise AssemblyError("Package missing audio_path field")

    if not os.path.exists(audio_path):
        raise AssemblyError(f"Audio file not found: {audio_path}")

    # Validate audio is readable
    try:
        clip = AudioFileClip(audio_path)
        duration = clip.duration
        clip.close()
    except Exception as e:
        raise AssemblyError(f"Audio file corrupted: {e}")

    logger.info(f"Audio loaded: {audio_path} ({duration:.2f}s)")
    return audio_path, duration
```

**Day 5: Code Consolidation**

Identify and consolidate duplicate code:

**File**: `app/core/pipeline/utils/validation.py` (NEW)

```python
"""Shared validation utilities for pipeline layers."""
import os
import json
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

def validate_file_exists(file_path: str, file_type: str = "File") -> None:
    """Validate file exists."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_type} not found: {file_path}")

def validate_file_readable(file_path: str, min_size: int = 1) -> None:
    """Validate file is readable and non-empty."""
    validate_file_exists(file_path)

    size = os.path.getsize(file_path)
    if size < min_size:
        raise ValueError(f"File too small ({size} bytes): {file_path}")

def validate_json_file(file_path: str) -> dict:
    """Load and validate JSON file."""
    validate_file_readable(file_path)

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")

def validate_image_files(image_paths: List[str]) -> Tuple[bool, List[str]]:
    """Validate list of image files exist and are readable."""
    errors = []

    for path in image_paths:
        if not path:
            errors.append("Missing image path")
            continue

        if not os.path.exists(path):
            errors.append(f"Image missing: {path}")
            continue

        size = os.path.getsize(path)
        if size < 1000:  # Less than 1KB
            errors.append(f"Image too small ({size} bytes): {path}")

    return len(errors) == 0, errors

def validate_post_write(file_path: str, expected_type: str = "json") -> None:
    """Validate file was written successfully."""
    validate_file_readable(file_path, min_size=10)

    if expected_type == "json":
        # Validate JSON is parseable
        try:
            with open(file_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            raise IOError(f"Written file is not valid JSON: {e}")

    logger.debug(f"Post-write validation passed: {file_path} ({os.path.getsize(file_path)} bytes)")
```

Usage across all layers:
```python
from app.core.pipeline.utils.validation import (
    validate_file_exists,
    validate_json_file,
    validate_image_files,
    validate_post_write
)

# In L3
data = validate_json_file(ideas_file)

# In L5
valid, errors = validate_image_files([slide['path'] for slide in slides])
if not valid:
    raise MediaGenerationError(f"Invalid slides: {errors}")

# In L6
validate_file_exists(audio_path, "Audio file")
```

---

### Week 4: Testing, Documentation, Known Issues

**Day 1-2: Integration Testing**

**File**: `tests/integration/test_pipeline_reliability.py`

```python
import pytest
import json
import os
from pathlib import Path

def test_l3_ideas_generation_with_missing_trends():
    """L3 should fail with clear error if trends file missing."""
    from L3_ideas import IdeaCreation

    # Remove trends file
    trends_file = Path('output/all_trends.json')
    trends_file.unlink(missing_ok=True)

    ideation = IdeaCreation(phase='regular_season', week='week1')

    with pytest.raises(FileNotFoundError, match="Trends file not found"):
        ideation.run()

def test_l5_media_generation_with_empty_ideas():
    """L5 should fail with clear error if ideas list empty."""
    from L5_media import MediaGeneration

    # Create empty ideas file
    ideas_file = Path('output/regular_season/week1/ideas_approved.json')
    ideas_file.parent.mkdir(parents=True, exist_ok=True)
    with open(ideas_file, 'w') as f:
        json.dump({'ideas': [], 'metadata': {}}, f)

    media_gen = MediaGeneration(phase='regular_season', week='week1')

    with pytest.raises(ValueError, match="contains no ideas"):
        media_gen.run()

def test_l6_assembly_with_missing_media_packages():
    """L6 should fail with clear error if media packages missing."""
    from L6_assembly import VideoAssembly

    # Remove media packages file
    packages_file = Path('output/regular_season/week1/media_packages.json')
    packages_file.unlink(missing_ok=True)

    assembly = VideoAssembly(phase='regular_season', week='week1')

    with pytest.raises(FileNotFoundError, match="packages file not found"):
        assembly.run()

def test_l5_ai_image_generation_fallback_chain():
    """L5 should try Flux → DALL-E → Pexels on failures."""
    from L5_media import MediaGeneration

    media_gen = MediaGeneration(phase='regular_season', week='week1')

    # Mock Flux to fail
    def mock_flux_fail(*args, **kwargs):
        raise Exception("Flux API unavailable")

    media_gen._generate_flux = mock_flux_fail

    # Should fallback to DALL-E (or Pexels if DALL-E also fails)
    result = media_gen._generate_image_with_fallback("test prompt", "idea_1")

    # Should succeed via fallback, not return None
    assert result is not None

def test_file_write_validation():
    """Test post-write validation catches corruption."""
    from app.core.pipeline.utils.validation import validate_post_write

    # Write valid JSON
    test_file = Path('test_output.json')
    with open(test_file, 'w') as f:
        json.dump({'test': 'data'}, f)

    validate_post_write(test_file, expected_type='json')  # Should pass

    # Write invalid JSON
    with open(test_file, 'w') as f:
        f.write('{ invalid json')

    with pytest.raises(IOError, match="not valid JSON"):
        validate_post_write(test_file, expected_type='json')

    test_file.unlink()
```

**Day 3: Manual Testing with Test Preset**

Test with existing test preset across full pipeline:

```bash
# Start backend + frontend
python3 -m app.main &  # Backend on 5001
cd app/frontend && npm run dev &  # Frontend on 5173

# Test full pipeline with test preset
# 1. Select test preset in dashboard
# 2. Submit job
# 3. Monitor logs/pipeline.log for:
#    - All print() replaced with logger calls
#    - No silent failures (all errors logged with context)
#    - File validation messages appearing
#    - Retry attempts logged with backoff delays
# 4. Check output directory for completeness
# 5. Verify job_id appears in all log lines
```

**Day 4: Known Issues Documentation**

**File**: `docs/KNOWN_ISSUES.md`

```markdown
# Known Issues & Workarounds

**Last Updated:** February 2026 (Phase 1 Complete)

---

## L3: Ideas Generation

### Issue: Trends file missing or corrupted
**Symptoms:** Job fails at L3 with "Trends file not found" or "Trends file corrupted"
**Root Cause:** Web search trend detector (L1) not run or failed silently
**Fix:** Run `python3 scripts/web_search_trend_detector.py` before L3
**Detection:** Now fails fast with clear error message (previously returned empty list)

### Issue: API timeout on GoatedBets
**Symptoms:** "GoatedBets API timeout" in logs, retrying 3 times
**Root Cause:** Network latency or API overload
**Fix:** Retry logic with exponential backoff (5s, 10s, 30s delays)
**Fallback:** Falls back to BallDontLie API if GoatedBets exhausted

---

## L5: Media Generation

### Issue: Flux AI image generation fails
**Symptoms:** "Flux attempt 1/3 failed" in logs
**Root Cause:** FAL API rate limiting or timeout
**Fix:** Retry 3 times, then fallback to DALL-E, then Pexels stock
**Detection:** All attempts logged with error context

### Issue: Media packages marked "ready_for_assembly" but files missing
**Symptoms:** L6 fails with "FileNotFoundError" on background/slide images
**Root Cause:** L5 previously set ready=True without validating files exist
**Fix:** Added comprehensive file validation before setting ready flag
**Detection:** Validation errors logged with specific missing files

---

## L6: Video Assembly

### Issue: MoviePy TextClip hangs
**Symptoms:** Job gets stuck at "Rendering text overlays"
**Root Cause:** Missing font files
**Fix:** Install fonts: `brew install font-inter font-roboto`
**Alternative:** Set fallback font chain in preset config

### Issue: Carousel assembly fails with "No slides found"
**Symptoms:** Carousel package exists but assembly returns error
**Root Cause:** L5 media package invalid (missing carousel_slides field)
**Fix:** L5 now validates structure before marking ready_for_assembly
**Detection:** Prerequisites validated before assembly starts

### Issue: Logo overlay fails silently
**Symptoms:** Final carousel missing logo branding
**Root Cause:** Logo file path invalid or file not found
**Fix:** Added explicit validation, assembly now fails if logo required but missing
**Detection:** "Logo file not found" error with path logged

---

## General: File I/O

### Issue: Empty/0-byte output files
**Symptoms:** Layer reports "complete" but output file is 0 bytes or missing
**Root Cause:** Disk full, permissions error, or serialization failure
**Fix:** All file writes now have post-write validation
**Detection:** Fails immediately with "File write produced 0 bytes" error

### Issue: Corrupted JSON files
**Symptoms:** Next layer fails with "Invalid JSON" error
**Root Cause:** Process killed mid-write or JSON serialization error
**Fix:** Post-write validation re-parses JSON to confirm validity
**Detection:** Fails at write time, not downstream read time

---

## Logging & Observability

### Issue: Can't debug failures in production
**Symptoms:** Job fails but no error logs captured
**Root Cause:** Print statements instead of structured logging
**Fix:** All 242 print() calls replaced with logger.error/warning/info
**Output:** logs/pipeline.log (all messages), logs/errors.log (errors only)

### Issue: Can't trace failures across layers
**Symptoms:** Error logs don't show which job or layer failed
**Root Cause:** No correlation IDs in logs
**Fix:** All log lines include job_id and layer context
**Format:** `timestamp | job_id | layer | logger | level | message`

---

## API Integrations

### Issue: Transient API failures become permanent
**Symptoms:** Single timeout causes entire job to fail
**Root Cause:** No retry logic on API calls
**Fix:** All external APIs now have retry with exponential backoff
**Behavior:** 3 attempts with 2s, 4s, 8s delays (with jitter)

---

## Testing

### Issue: Silent failures in test suite
**Symptoms:** Tests pass but output is actually broken
**Root Cause:** Tests didn't validate output completeness
**Fix:** Integration tests now check:
  - File existence AND size
  - JSON structure validity
  - Expected field presence
  - Error messages on known failure modes
```

**Day 5: Update Documentation**

Update `docs/ARCHITECTURE.md` with:
- Logging configuration section
- Validation utilities section
- Error handling patterns section
- Inter-layer data contracts section

Update `README.md` with:
- Logging output locations (logs/pipeline.log, logs/errors.log)
- How to read correlation IDs in logs
- How to run integration tests

---

## Files to Modify/Create Summary

### New Files (Create)

```
app/core/utils/
├── logging_config.py              # Structured logging with correlation IDs
├── retry_utils.py                 # Retry decorator with exponential backoff
└── validation.py                  # Shared validation utilities

docs/
└── KNOWN_ISSUES.md                # Known issues + workarounds

tests/integration/
└── test_pipeline_reliability.py  # Integration tests for reliability
```

### Existing Files (Modify)

**Week 1 - L3 Fixes:**
```
app/core/pipeline/layers/_L3/L3_ideas.py       # 22 prints → logger, 18 fallbacks → raise, 11 file I/O validations
app/core/pipeline/adapters/l3_adapter.py        # 2 fallbacks → raise, 2 file I/O validations
app/core/pipeline/orchestrator.py              # Initialize logging with JobContext
```

**Week 2 - L5 Fixes:**
```
app/core/pipeline/layers/_L5/L5_media.py       # 126 prints → logger, 58 fallbacks → raise, 19 file I/O validations, AI retry/fallback
app/core/pipeline/adapters/l5_adapter.py        # 2 fallbacks → raise, 1 file I/O validation
```

**Week 3 - L6 Fixes:**
```
app/core/pipeline/layers/_L6/L6_assembly.py    # 94 prints → logger, 24 fallbacks → raise, 12 file I/O validations
app/core/pipeline/adapters/l6_adapter.py        # 2 fallbacks → raise, 1 file I/O validation
```

**Week 4 - Documentation:**
```
docs/ARCHITECTURE.md                            # Add logging/validation sections
docs/README.md                                  # Add logging output locations
```

---

## Success Criteria

**Quantitative:**
- ✅ Zero print() calls remaining (242 replaced)
- ✅ Zero "return empty list on error" patterns (106 fixed)
- ✅ 100% file writes have post-write validation (46 added)
- ✅ 100% API calls have retry logic (16 added)
- ✅ All adapters return explicit success/failure (6 fixed)

**Qualitative:**
- ✅ Every failed job provides actionable error message with file/line context
- ✅ All errors logged with job_id + layer correlation
- ✅ No silent failures (all errors raise exceptions or log as errors)
- ✅ logs/pipeline.log contains complete execution trace
- ✅ logs/errors.log contains only failures with full context

**User Experience:**
- ✅ "Job failed at L3: Trends file not found. Run web_search_trend_detector.py first."
- ✅ "Job failed at L5: All image generation methods exhausted for idea 'matchup_analysis'"
- ✅ "Job failed at L6: Carousel slides missing - L5 validation should have caught this"

**NOT:**
- ❌ "Job complete!" (but output directory empty)
- ❌ No error indication (silent failure)
- ❌ Generic "Exception occurred" (no context)

---

## Verification Checklist

**Week 1 - L3:**
- [ ] L3_ideas.py has zero print() calls
- [ ] L3_ideas.py raises exceptions on errors (no empty list returns)
- [ ] save_approved_ideas() validates file write succeeded
- [ ] fetch_goatedbets_matchup() retries 3 times on timeout
- [ ] logs/pipeline.log shows job_id and layer context

**Week 2 - L5:**
- [ ] L5_media.py has zero print() calls
- [ ] AI image generation retries 3 times, then fallback chain
- [ ] Media packages validate all files before ready_for_assembly=True
- [ ] load_ideas() raises exception on file missing/corrupt/empty

**Week 3 - L6:**
- [ ] L6_assembly.py has zero print() calls
- [ ] Carousel assembly validates prerequisites before starting
- [ ] Logo overlay fails job if logo required but missing
- [ ] Audio/background preparation raises exception if files missing

**Week 4 - Testing:**
- [ ] Integration tests pass for all error scenarios
- [ ] Manual test with test preset completes successfully
- [ ] logs/pipeline.log readable and contains full execution trace
- [ ] KNOWN_ISSUES.md documents all failure modes with workarounds

---

## Risk Mitigation

**High Risk:** Changes introduce new bugs

**Mitigation:**
- Test each layer individually after modification
- Use test preset for end-to-end validation after each week
- Keep git commits granular (one file per commit)
- Have rollback plan (git revert) if issues arise

**Medium Risk:** Exceptions now raised instead of silent failures, might break existing workflows

**Mitigation:**
- Existing silent failures were already breaking the workflow (producing no output)
- New exceptions provide clear error messages for debugging
- KNOWN_ISSUES.md documents all common failures with fixes

**Low Risk:** Logging overhead affects performance

**Mitigation:**
- Logging is asynchronous, minimal overhead
- File I/O is buffered
- Measure baseline vs after (should be negligible)

---

## Timeline & Milestones

**Week 1 Milestone:** L3 Ideas Generation reliable
- Logging configured across pipeline
- L3 prints → logger, silent failures → exceptions
- Test: Submit job, verify errors logged with context

**Week 2 Milestone:** L5 Media Generation reliable
- AI image generation has retry + fallback
- Media packages validated before assembly
- Test: Submit job with API failures, verify retries + fallback

**Week 3 Milestone:** L6 Assembly reliable
- Carousel assembly validates prerequisites
- All file I/O has pre/post validation
- Test: Submit end-to-end job, verify output completeness

**Week 4 Milestone:** Documentation + testing complete
- Integration tests pass
- KNOWN_ISSUES.md captures all failure modes
- Test: Run full pipeline, verify no silent failures

---

## Next Steps After Phase 1

Once reliability reaches 95%+ success rate:
1. **Phase 2:** Preview Architecture (RecordRTC + html2canvas)
2. **Enhancements:**
   - Layer output caching (avoid re-running L1-L3 for adjustments)
   - WebSocket streaming (replace polling)
   - Prometheus metrics export
   - Health check endpoints

---

**Status:** Ready for implementation
**Dependencies:** None (uses existing architecture)
**Approval Required:** User confirmation before starting Week 1
