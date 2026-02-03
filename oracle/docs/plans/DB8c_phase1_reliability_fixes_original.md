# Phase 1: Pipeline Reliability Overhaul

**Session:** DB8c - Phase 1
**Date:** January 29, 2026
**Status:** PLANNING
**Timeline:** 3-4 weeks
**Scope:** Critical reliability fixes to achieve 95%+ pipeline success rate

---

## Executive Summary

Fix 40+ critical reliability issues discovered in comprehensive pipeline audit (L1-L6). This phase establishes a solid foundation by implementing proper exception handling, input validation, retry logic, thread safety, and structured logging. **Must complete before Phase 2 (Preview Architecture).**

**Why This Matters**: Preview system is useless if pipeline fails 30% of the time. Google AI Studio's reliability comes from comprehensive error handling - we need the same foundation.

---

## Current State: Reliability Issues Audit

### Critical Issues Discovered

#### 1. **40+ Bare Exception Handlers**
Silent failures without logging - impossible to debug

**Files Affected**:
- `_L6/L6_assembly.py` - 7 bare excepts
- `_L5/L5_media.py` - 8 bare excepts
- `_L4/L4_audio.py` - 5 bare excepts
- `_L3/L3_ideas.py` - 3 bare excepts
- `_L2/L2_calendar.py` - 1 bare except
- `_L6/processors/ffmpeg_processor.py` - Multiple bare excepts
- `_L6/processors/comfyui_processor.py` - Multiple bare excepts
- `_L7/L7_distribution.py` - 5 bare excepts
- `_L1/inputs/*.py` - Multiple bare excepts

#### 2. **No Input Validation**
API responses and layer outputs used without validation

**Problems**:
- L1 assumes API response structure exists
- L3 assumes ideas JSON has required fields
- L5 assumes image files exist and are valid
- No schema validation anywhere

#### 3. **No Retry Logic**
API timeouts fail immediately

**Problems**:
- GoatedBets API: 30s timeout, no retry
- BallDontLie API: 10s timeout, no retry
- AI services (Gemini, Claude, Flux): 60s timeout, no retry
- Single failure = entire pipeline fails

#### 4. **Thread-Unsafe Global State**
Concurrent access can corrupt data

**Problems**:
- L3 ideas.py: `_MCP_GAMES_CACHE` has no locking
- Multiple jobs could modify cache simultaneously
- Race conditions in file writes

#### 5. **FFmpeg Subprocess Failures**
Silent failures, no diagnostic info

**Problems**:
- Errors swallowed with `except: pass`
- No stderr logging
- 60s hard timeout kills long encodes
- Partial files left behind

#### 6. **MoviePy TextClip Hangs**
No timeout on font loading

**Problems**:
- Can hang indefinitely on missing fonts
- No fallback chain validation
- Hardcoded paths: `/opt/homebrew/bin/convert`

#### 7. **Missing Error Context**
Generic "Exception" messages

**Problems**:
- No traceback information
- No correlation IDs for request tracking
- Can't distinguish network vs validation vs system errors

#### 8. **No Data Validation Between Layers**
Fragile assumptions about data structure

**Problems**:
- L1→L3: Assumes props exist
- L3→L4: Assumes ideas_approved.json valid
- L4→L5: Assumes audio files valid
- L5→L6: Assumes all media files exist

---

## Implementation Plan

### Task 1: Exception Handling Overhaul (Week 1)

**Goal**: Replace all bare exception handlers with specific exceptions + logging

**Files to Fix** (Priority Order):

**TIER 1 - CRITICAL** (Week 1, Days 1-3):
```
app/core/pipeline/layers/_L6/L6_assembly.py          # 7 bare excepts
app/core/pipeline/layers/_L5/L5_media.py             # 8 bare excepts
app/core/pipeline/layers/_L4/L4_audio.py             # 5 bare excepts
app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py
app/core/pipeline/layers/_L6/processors/comfyui_processor.py
```

**TIER 2 - HIGH** (Week 1, Days 4-5):
```
app/core/pipeline/layers/_L3/L3_ideas.py             # 3 bare excepts
app/core/pipeline/layers/_L2/L2_calendar.py          # 1 bare except
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
except requests.RequestException as e:
    logger.error(f"API request failed: {e}", exc_info=True)
    raise PipelineError(f"External API error: {e}")
except Exception as e:
    logger.error(f"Unexpected error in {operation}: {e}", exc_info=True)
    raise
```

**New File to Create**: `app/core/exceptions.py`

```python
"""Custom exception types for pipeline."""

class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass

class ValidationError(PipelineError):
    """Data validation failed."""
    pass

class APIError(PipelineError):
    """External API request failed."""
    pass

class FFmpegError(PipelineError):
    """FFmpeg encoding failed."""
    pass

class MediaGenerationError(PipelineError):
    """Media generation (L5) failed."""
    pass

class AudioGenerationError(PipelineError):
    """Audio generation (L4) failed."""
    pass
```

---

### Task 2: Input Validation Layer (Week 1-2)

**Goal**: Add Pydantic schemas for all data contracts between layers

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

**Example Schema**: `app/core/pipeline/schemas/l1_schemas.py`

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class PropData(BaseModel):
    """Player prop data from API."""
    player_name: str
    team: str
    stat_type: str
    line: float
    over_odds: Optional[int] = None
    under_odds: Optional[int] = None

    @validator('line')
    def validate_line(cls, v):
        if v <= 0:
            raise ValueError('Prop line must be positive')
        return v

class TeamData(BaseModel):
    """Team information."""
    name: str
    abbreviation: str
    city: Optional[str] = None
    conference: Optional[str] = None
    division: Optional[str] = None

class NormalizedMatchup(BaseModel):
    """Standardized matchup data from L1."""
    matchup_id: str
    sport: str
    away_team: str
    home_team: str
    game_time: str
    props: List[PropData] = Field(default_factory=list)
    vegas_spread: Optional[float] = None
    over_under: Optional[float] = None

    @validator('props')
    def validate_props_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Matchup must have at least one prop')
        return v

    @validator('sport')
    def validate_sport(cls, v):
        allowed_sports = ['nfl', 'nba', 'mlb', 'nhl', 'ncaaf', 'ncaab']
        if v.lower() not in allowed_sports:
            raise ValueError(f'Sport must be one of {allowed_sports}')
        return v.lower()
```

**Usage Pattern in Pipeline**:

```python
# L1 output validation
from app.core.pipeline.schemas.l1_schemas import NormalizedMatchup
from pydantic import ValidationError

def fetch_matchup_data(matchup_id: str) -> NormalizedMatchup:
    """Fetch and validate matchup data."""
    raw_data = api.get_matchup(matchup_id)

    # Validate with Pydantic
    try:
        validated = NormalizedMatchup(**raw_data)
    except ValidationError as e:
        logger.error(f"L1 output validation failed: {e}")
        raise PipelineError(f"Invalid matchup data from API: {e}")

    logger.info(f"Validated matchup {matchup_id}: {validated.matchup_id}")
    return validated
```

**Apply Validation at Layer Boundaries**:
- L1 output → Validate before passing to L3
- L3 output → Validate ideas JSON structure
- L4 output → Validate audio metadata + timing
- L5 output → Validate media packages exist

---

### Task 3: Retry Logic with Exponential Backoff (Week 2)

**Goal**: Implement robust retry mechanism for all external API calls

**File to Create**: `app/core/utils/retry_utils.py`

```python
import time
import random
import logging
from functools import wraps
from typing import Type, Tuple, Callable

logger = logging.getLogger(__name__)

def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True,
    on_retry: Callable = None
):
    """
    Retry decorator with exponential backoff and jitter.

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds (doubles each retry)
        max_delay: Maximum delay between retries
        exceptions: Tuple of exception types to catch
        jitter: Add randomness to delay (prevent thundering herd)
        on_retry: Optional callback(attempt, exception) on each retry

    Example:
        @retry_with_backoff(max_attempts=3, base_delay=2.0)
        def fetch_data():
            return requests.get(url, timeout=30)
    """
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
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
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

                    # Optional retry callback
                    if on_retry:
                        on_retry(attempt, e)

                    time.sleep(delay)

        return wrapper
    return decorator

# Specialized retry for HTTP requests
def retry_http(max_attempts: int = 3, base_delay: float = 2.0):
    """Retry specifically for HTTP requests (timeouts, 5xx errors)."""
    import requests

    return retry_with_backoff(
        max_attempts=max_attempts,
        base_delay=base_delay,
        exceptions=(
            requests.Timeout,
            requests.ConnectionError,
            requests.HTTPError
        )
    )

# Usage examples
@retry_http(max_attempts=3, base_delay=2.0)
def fetch_goatedbets_data(sport: str, week: int):
    """Fetch data with automatic retry on failure."""
    response = requests.get(
        f"{API_URL}/{sport}/week/{week}",
        timeout=30
    )
    response.raise_for_status()  # Raises HTTPError for 4xx/5xx
    return response.json()
```

**Apply to All API Calls**:

**L1 Data Sources**:
- `_L1/inputs/goatedbets_api.py` - 3 methods: `get_matchups()`, `get_props()`, `get_odds()`
- `_L1/inputs/balldontlie_api.py` - 4 methods: `get_nfl_games()`, `get_nba_games()`, `get_player_stats()`, `get_team_info()`
- `_L1/inputs/ai_models.py` - Gemini/Claude API calls

**L5 Media Generation**:
- `_L5/L5_media.py` - Flux API, DALL-E API, Gemini Vision API

**Example Application**:
```python
# Before
def get_matchups(sport, week):
    response = requests.get(url, timeout=30)
    return response.json()

# After
@retry_http(max_attempts=3, base_delay=2.0)
def get_matchups(sport, week):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

---

### Task 4: Thread-Safe Cache Implementation (Week 2)

**Goal**: Fix global state race conditions with thread-safe cache

**File to Create**: `app/core/utils/cache_utils.py`

```python
import threading
from datetime import datetime, timedelta
from typing import Any, Optional, Dict

class ThreadSafeCache:
    """Thread-safe cache with TTL support."""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize thread-safe cache.

        Args:
            ttl_seconds: Time-to-live for cache entries (default 1 hour)
        """
        self._cache: Dict[str, tuple] = {}
        self._lock = threading.RLock()  # Reentrant lock
        self._ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
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
        """Set value in cache with current timestamp."""
        with self._lock:
            self._cache[key] = (value, datetime.now())

    def delete(self, key: str) -> bool:
        """Delete key from cache. Returns True if key existed."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        """Return number of items in cache."""
        with self._lock:
            return len(self._cache)

    def get_or_set(self, key: str, factory: callable) -> Any:
        """
        Get value from cache or compute with factory function.

        Args:
            key: Cache key
            factory: Function to call if key not in cache

        Returns:
            Cached or newly computed value
        """
        value = self.get(key)
        if value is not None:
            return value

        # Compute new value
        value = factory()
        self.set(key, value)
        return value
```

**Apply to L3 Ideas Cache**:

**File to Modify**: `app/core/pipeline/layers/_L3/L3_ideas.py`

```python
# BEFORE (current - unsafe)
_MCP_GAMES_CACHE = []

def get_mcp_games():
    global _MCP_GAMES_CACHE
    if not _MCP_GAMES_CACHE:
        _MCP_GAMES_CACHE = fetch_from_mcp()
    return _MCP_GAMES_CACHE

# AFTER (thread-safe)
from app.core.utils.cache_utils import ThreadSafeCache

_MCP_GAMES_CACHE = ThreadSafeCache(ttl_seconds=1800)  # 30 min TTL

def get_mcp_games():
    """Fetch MCP games with thread-safe caching."""
    return _MCP_GAMES_CACHE.get_or_set(
        key='mcp_games',
        factory=lambda: fetch_from_mcp()
    )
```

---

### Task 5: FFmpeg Error Capture & Logging (Week 2-3)

**Goal**: Proper subprocess error handling with full diagnostic info

**File to Modify**: `app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py`

```python
import subprocess
import logging
from typing import List
from app.core.exceptions import FFmpegError

logger = logging.getLogger(__name__)

def run_ffmpeg_command(
    cmd: List[str],
    timeout: int = 300,
    description: str = "FFmpeg operation"
) -> str:
    """
    Run FFmpeg command with proper error handling.

    Args:
        cmd: FFmpeg command as list
        timeout: Timeout in seconds (default 5min for long encodes)
        description: Human-readable description for logging

    Returns:
        Output file path

    Raises:
        FFmpegError: If encoding fails
    """
    logger.info(f"Starting {description}: {' '.join(cmd[:5])}...")

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
                f"{description} failed with code {result.returncode}\n"
                f"Command: {' '.join(cmd)}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
            raise FFmpegError(
                f"{description} failed: {result.stderr[:500]}"
            )

        # Log success
        logger.info(f"{description} completed: {cmd[-1]}")
        return cmd[-1]  # Output file path

    except subprocess.TimeoutExpired as e:
        logger.error(
            f"{description} timeout after {timeout}s\n"
            f"Command: {' '.join(cmd)}"
        )
        raise FFmpegError(
            f"{description} timed out after {timeout} seconds. "
            f"Try increasing timeout or reducing video duration."
        )

    except FileNotFoundError:
        logger.error("FFmpeg binary not found - check installation")
        raise FFmpegError(
            "FFmpeg not installed or not in PATH. "
            "Install via: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
        )

def validate_ffmpeg_installation():
    """Validate FFmpeg is installed and accessible."""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            logger.info(f"FFmpeg validated: {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        logger.error("FFmpeg validation failed")
        return False

# Call on module import to fail fast
if not validate_ffmpeg_installation():
    raise FFmpegError("FFmpeg not available - L6 assembly will fail")
```

**Apply Pattern to All Subprocess Calls**:
- Carousel reel generation
- Video padding/scaling
- Meme mashup assembly
- ComfyUI server calls

---

### Task 6: Structured Logging (Week 3)

**Goal**: Replace print statements with structured logging + correlation IDs

**File to Create**: `app/core/utils/logging_config.py`

```python
import logging
import sys
from contextvars import ContextVar
from typing import Optional

# Context variables for correlation
job_context: ContextVar[Optional[str]] = ContextVar('job_id', default=None)
layer_context: ContextVar[Optional[str]] = ContextVar('layer', default=None)

class JobContextFilter(logging.Filter):
    """Add job_id and layer to all log records."""

    def filter(self, record):
        record.job_id = job_context.get() or 'no-job'
        record.layer = layer_context.get() or 'no-layer'
        return True

def setup_pipeline_logging(log_level: str = 'INFO'):
    """
    Configure structured logging for pipeline.

    Format: timestamp | job_id | layer | logger | level | message
    """
    # Create logs directory if not exists
    import os
    os.makedirs('logs', exist_ok=True)

    # Configure format
    log_format = (
        '%(asctime)s | %(job_id)s | %(layer)s | '
        '%(name)s | %(levelname)s | %(message)s'
    )

    # File handler (all logs)
    file_handler = logging.FileHandler('logs/pipeline.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.addFilter(JobContextFilter())

    # Console handler (info and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.addFilter(JobContextFilter())

    # Error file handler (errors only)
    error_handler = logging.FileHandler('logs/errors.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(log_format))
    error_handler.addFilter(JobContextFilter())

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=[file_handler, console_handler, error_handler]
    )

    logging.info("Pipeline logging configured")

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

# Usage in pipeline
def run_pipeline(job_id: str, config: dict):
    """Run pipeline with correlation IDs."""
    with JobContext(job_id):
        logger = logging.getLogger(__name__)
        logger.info(f"Starting pipeline for preset {config['preset_id']}")

        # L1
        with LayerContext('L1'):
            logger.info("Running L1 data fetch")
            run_L1(config)

        # L2
        with LayerContext('L2'):
            logger.info("Running L2 calendar")
            run_L2(config)

        # ... etc
```

**Apply to All Layers**:
- Replace all `print()` statements with `logger.info()`
- Replace all `print(f"Error: {e}")` with `logger.error()`
- Use context managers for job/layer correlation

---

### Task 7: Data Validation Between Layers (Week 3)

**Goal**: Validate data contracts at every layer boundary

**Implementation Pattern**:

```python
# L1 → L3 validation
def run_L3_ideas(config: dict):
    """L3: Generate ideas from L1 matchup data."""
    from app.core.pipeline.schemas.l1_schemas import NormalizedMatchup
    from app.core.pipeline.schemas.l3_schemas import IdeaPackage

    # Load L1 output
    l1_file = os.path.join(config['output_dir'], 'L1', 'matchups.json')
    with open(l1_file, 'r') as f:
        l1_data = json.load(f)

    # Validate L1 output
    try:
        matchup = NormalizedMatchup(**l1_data)
    except ValidationError as e:
        logger.error(f"L1 output validation failed: {e}")
        raise PipelineError(f"Invalid L1 data structure: {e}")

    # Generate ideas
    ideas = generate_ideas(matchup)

    # Validate L3 output before saving
    try:
        validated_ideas = [IdeaPackage(**idea) for idea in ideas]
    except ValidationError as e:
        logger.error(f"L3 output validation failed: {e}")
        raise PipelineError(f"Invalid idea structure: {e}")

    # Save validated output
    save_ideas(validated_ideas)
```

**Checkpoints to Add**:
- L1→L3: Validate `NormalizedMatchup` before ideas generation
- L3→L4: Validate `IdeaPackage` before audio generation
- L4→L5: Validate `TimingData` and audio files exist
- L5→L6: Validate `MediaPackage` and all files exist

---

## Files to Modify/Create Summary

### New Files (Create)

```
app/core/exceptions.py                    # Custom exception types
app/core/utils/retry_utils.py             # Retry decorator
app/core/utils/cache_utils.py             # Thread-safe cache
app/core/utils/logging_config.py          # Structured logging

app/core/pipeline/schemas/
├── __init__.py
├── l1_schemas.py                         # L1 data validation
├── l2_schemas.py                         # L2 calendar validation
├── l3_schemas.py                         # L3 ideas validation
├── l4_schemas.py                         # L4 audio validation
├── l5_schemas.py                         # L5 media validation
└── l6_schemas.py                         # L6 assembly validation
```

### Existing Files (Modify)

**TIER 1 - Critical** (Week 1):
```
app/core/pipeline/layers/_L6/L6_assembly.py
app/core/pipeline/layers/_L5/L5_media.py
app/core/pipeline/layers/_L4/L4_audio.py
app/core/pipeline/layers/_L6/processors/ffmpeg_processor.py
app/core/pipeline/layers/_L6/processors/comfyui_processor.py
```

**TIER 2 - High** (Week 2):
```
app/core/pipeline/layers/_L3/L3_ideas.py
app/core/pipeline/layers/_L2/L2_calendar.py
app/core/pipeline/layers/_L1/inputs/goatedbets_api.py
app/core/pipeline/layers/_L1/inputs/balldontlie_api.py
app/core/pipeline/layers/_L1/inputs/ai_models.py
app/core/pipeline/layers/_L7/L7_distribution.py
```

**TIER 3 - Apply patterns** (Week 3):
```
All remaining _L1/inputs/*.py files
All _L6/processors/*.py files
```

---

## Testing Strategy

### Unit Tests (Create)

**File**: `tests/test_retry_utils.py`
```python
import pytest
from app.core.utils.retry_utils import retry_with_backoff

def test_retry_succeeds_on_second_attempt():
    attempts = []

    @retry_with_backoff(max_attempts=3, base_delay=0.1)
    def flaky_function():
        attempts.append(1)
        if len(attempts) < 2:
            raise ValueError("Temporary failure")
        return "success"

    result = flaky_function()
    assert result == "success"
    assert len(attempts) == 2

def test_retry_exhausts_attempts():
    @retry_with_backoff(max_attempts=3, base_delay=0.1)
    def always_fails():
        raise ValueError("Permanent failure")

    with pytest.raises(ValueError):
        always_fails()
```

**File**: `tests/test_cache_utils.py`
```python
import pytest
from app.core.utils.cache_utils import ThreadSafeCache
import time

def test_cache_get_set():
    cache = ThreadSafeCache(ttl_seconds=10)
    cache.set('key1', 'value1')
    assert cache.get('key1') == 'value1'

def test_cache_ttl_expiration():
    cache = ThreadSafeCache(ttl_seconds=1)
    cache.set('key1', 'value1')
    time.sleep(1.1)
    assert cache.get('key1') is None

def test_cache_get_or_set():
    cache = ThreadSafeCache()
    result = cache.get_or_set('key1', lambda: 'computed_value')
    assert result == 'computed_value'

    # Should not recompute
    result2 = cache.get_or_set('key1', lambda: 'new_value')
    assert result2 == 'computed_value'
```

### Integration Tests

**File**: `tests/integration/test_l1_validation.py`
```python
import pytest
from app.core.pipeline.schemas.l1_schemas import NormalizedMatchup
from pydantic import ValidationError

def test_valid_matchup():
    data = {
        'matchup_id': 'nfl_2025_w18_buf_mia',
        'sport': 'nfl',
        'away_team': 'Buffalo Bills',
        'home_team': 'Miami Dolphins',
        'game_time': '2025-01-05T13:00:00',
        'props': [
            {
                'player_name': 'Josh Allen',
                'team': 'BUF',
                'stat_type': 'passing_yards',
                'line': 275.5,
                'over_odds': -110,
                'under_odds': -110
            }
        ]
    }

    matchup = NormalizedMatchup(**data)
    assert matchup.matchup_id == 'nfl_2025_w18_buf_mia'
    assert len(matchup.props) == 1

def test_invalid_matchup_missing_props():
    data = {
        'matchup_id': 'nfl_2025_w18_buf_mia',
        'sport': 'nfl',
        'away_team': 'Buffalo Bills',
        'home_team': 'Miami Dolphins',
        'game_time': '2025-01-05T13:00:00',
        'props': []  # Empty props should fail
    }

    with pytest.raises(ValidationError):
        NormalizedMatchup(**data)
```

### Manual Testing Checklist

**Week 3-4: End-to-End Validation**

1. **Trigger known error conditions**:
   - [ ] Missing API key → verify proper error message
   - [ ] Invalid matchup ID → verify validation error
   - [ ] FFmpeg not installed → verify clear error message
   - [ ] Network timeout → verify retry logic works
   - [ ] Concurrent jobs → verify no cache corruption

2. **Verify logging**:
   - [ ] Check `logs/pipeline.log` has correlation IDs
   - [ ] Check `logs/errors.log` has full tracebacks
   - [ ] Verify job_id appears in all log lines

3. **Performance testing**:
   - [ ] Run 10 concurrent jobs → verify no deadlocks
   - [ ] Verify retry delays use exponential backoff
   - [ ] Check cache hit rate for MCP games

---

## Success Criteria

**Quantitative Metrics**:
- ✅ Pipeline success rate: **> 95%** (vs ~70% estimated current)
- ✅ Error logging coverage: **100%** of exception paths have proper handlers
- ✅ API retry success: **> 90%** on transient failures
- ✅ Zero bare exception handlers remaining
- ✅ All layer boundaries have Pydantic validation

**Qualitative Goals**:
- ✅ Every failed job provides actionable error message
- ✅ All errors have correlation IDs for debugging
- ✅ No silent failures
- ✅ Thread-safe cache for concurrent jobs
- ✅ FFmpeg errors captured with full diagnostics

---

## Timeline & Milestones

**Week 1**:
- Day 1-3: Fix Tier 1 files (L6, L5, L4, FFmpeg processor)
- Day 4-5: Fix Tier 2 files (L3, L2, L1 inputs)

**Week 2**:
- Day 1-2: Create Pydantic schemas for all layers
- Day 3-4: Implement retry logic, apply to all API calls
- Day 5: Implement thread-safe cache

**Week 3**:
- Day 1-2: Implement structured logging
- Day 3-4: Add validation at layer boundaries
- Day 5: Integration testing

**Week 4**:
- Day 1-3: Manual testing, bug fixes
- Day 4-5: Documentation, final validation

---

## Risk Mitigation

**High Risk**: Changes introduce new bugs

**Mitigation**:
- Test each file individually after modification
- Keep git commits granular (one file per commit)
- Have rollback plan for each change
- Run full pipeline test after each major change

**Medium Risk**: Pydantic validation too strict

**Mitigation**:
- Start with permissive schemas, tighten gradually
- Use `Optional[]` liberally at first
- Add validation incrementally based on real failures

**Low Risk**: Performance degradation from logging

**Mitigation**:
- Use lazy string formatting: `logger.info(f"...")` only evaluates if level enabled
- File I/O is buffered, minimal overhead
- Measure before/after with `time` profiling

---

## Dependencies

**Python Packages** (add to `requirements.txt`):
```
pydantic>=2.0.0        # Data validation
```

**System Requirements**:
- Python 3.9+
- FFmpeg installed
- ImageMagick installed

---

## Next Steps After Phase 1

Once this phase completes with 95%+ success rate:
1. **Proceed to Phase 2**: Preview Architecture
2. Consider additional enhancements:
   - WebSocket streaming (replace polling)
   - Layer output caching
   - Prometheus metrics export
   - Health check endpoints

---

## Verification Checklist

Before marking Phase 1 complete:

**Code Quality**:
- [ ] Zero bare `except:` blocks remain
- [ ] All API calls use retry decorator
- [ ] All layer outputs validated with Pydantic
- [ ] All subprocess calls capture stderr
- [ ] All files use structured logging

**Testing**:
- [ ] Unit tests pass for retry/cache utils
- [ ] Integration tests pass for validation
- [ ] Manual end-to-end test passes
- [ ] 10 concurrent jobs run without errors

**Documentation**:
- [ ] Error messages are clear and actionable
- [ ] Logs include correlation IDs
- [ ] README updated with new dependencies
- [ ] Migration guide for any breaking changes

**Performance**:
- [ ] Pipeline success rate > 95%
- [ ] No performance regression vs baseline
- [ ] Cache hit rate > 80% for MCP games
- [ ] Retry success rate > 90%

---

## Appendix: Exception Handling Checklist

Use this checklist when fixing each file:

**For each bare `except:` block**:
1. [ ] Identify what specific exceptions can occur
2. [ ] Replace with specific exception types
3. [ ] Add logger.error() with exc_info=True
4. [ ] Raise custom PipelineError with context
5. [ ] Test the error path manually

**For each API call**:
1. [ ] Add @retry_http decorator
2. [ ] Add proper timeout
3. [ ] Call response.raise_for_status()
4. [ ] Validate response structure

**For each file write operation**:
1. [ ] Check parent directory exists
2. [ ] Use atomic writes (write to temp, then rename)
3. [ ] Validate data before writing
4. [ ] Log file path after successful write

**For each subprocess call**:
1. [ ] Set appropriate timeout
2. [ ] Capture stdout and stderr
3. [ ] Check returncode
4. [ ] Log full command on failure
5. [ ] Raise specific exception (FFmpegError, etc.)
