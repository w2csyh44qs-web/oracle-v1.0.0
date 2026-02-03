"""
Oracle Bootstrap - Terminal UI Utilities

Provides color output, progress indicators, and formatting for CLI.
Cross-platform support with graceful degradation.

Usage:
    from oracle.bootstrap.terminal import print_step, print_success, print_error

    print_step("Analyzing project", step=1, total=7)
    print_success("Analysis complete!")
    print_error("Failed to detect framework", hint="Check requirements.txt")

Author: Oracle Brain Cell Architecture (P30 Phase 5)
"""

import sys
from typing import Optional


class TerminalColors:
    """ANSI color codes for terminal output."""

    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'

    # Reset
    RESET = '\033[0m'

    @classmethod
    def disable(cls):
        """Disable all colors (for piped output or no-color environments)."""
        cls.RED = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.BLUE = ''
        cls.MAGENTA = ''
        cls.CYAN = ''
        cls.WHITE = ''
        cls.GRAY = ''
        cls.BOLD = ''
        cls.DIM = ''
        cls.UNDERLINE = ''
        cls.RESET = ''


# Auto-detect if we should use colors
def _should_use_colors() -> bool:
    """Check if terminal supports colors."""
    # Check NO_COLOR environment variable
    import os
    if os.environ.get('NO_COLOR'):
        return False

    # Check if output is being piped
    if not sys.stdout.isatty():
        return False

    # Check TERM environment variable
    term = os.environ.get('TERM', '')
    if term == 'dumb':
        return False

    return True


# Initialize colors based on environment
if not _should_use_colors():
    TerminalColors.disable()


def print_header(text: str, char: str = "="):
    """Print a header with surrounding characters."""
    width = 60
    print(f"\n{char * width}")
    print(f"{TerminalColors.BOLD}{text}{TerminalColors.RESET}")
    print(f"{char * width}")


def print_step(text: str, step: int, total: int, emoji: str = "📦"):
    """Print a step with progress indicator."""
    progress = f"[{step}/{total}]"
    print(f"\n{TerminalColors.CYAN}{progress}{TerminalColors.RESET} {emoji} {text}...")


def print_success(text: str, indent: int = 0):
    """Print a success message."""
    prefix = " " * indent
    print(f"{prefix}{TerminalColors.GREEN}✓{TerminalColors.RESET} {text}")


def print_error(text: str, hint: Optional[str] = None):
    """Print an error message with optional hint."""
    print(f"{TerminalColors.RED}✗{TerminalColors.RESET} {text}")
    if hint:
        print(f"{TerminalColors.YELLOW}💡 Hint:{TerminalColors.RESET} {hint}")


def print_warning(text: str):
    """Print a warning message."""
    print(f"{TerminalColors.YELLOW}⚠{TerminalColors.RESET} {text}")


def print_info(text: str, indent: int = 3):
    """Print an info message."""
    prefix = " " * indent
    print(f"{prefix}{TerminalColors.GRAY}•{TerminalColors.RESET} {text}")


def print_section(title: str):
    """Print a section title."""
    print(f"\n{TerminalColors.BOLD}{TerminalColors.BLUE}{title}{TerminalColors.RESET}")


def print_metric(label: str, value: str, emoji: str = ""):
    """Print a metric with label and value."""
    indent = " " * 3
    emoji_str = f"{emoji} " if emoji else ""
    print(f"{indent}{emoji_str}{TerminalColors.BOLD}{label}:{TerminalColors.RESET} {value}")


class ProgressBar:
    """Simple progress bar for terminal output."""

    def __init__(self, total: int, width: int = 40, show_percent: bool = True):
        """
        Initialize progress bar.

        Args:
            total: Total number of items
            width: Width of progress bar in characters
            show_percent: Show percentage alongside bar
        """
        self.total = total
        self.width = width
        self.show_percent = show_percent
        self.current = 0

    def update(self, current: Optional[int] = None, text: str = ""):
        """
        Update progress bar.

        Args:
            current: Current progress (if None, increments by 1)
            text: Optional text to show alongside bar
        """
        if current is not None:
            self.current = current
        else:
            self.current += 1

        # Calculate progress
        progress = min(self.current / self.total, 1.0)
        filled = int(self.width * progress)

        # Build bar
        bar = "█" * filled + "░" * (self.width - filled)

        # Build output
        output = f"\r{bar}"
        if self.show_percent:
            percent = int(progress * 100)
            output += f" {percent}%"
        if text:
            output += f" {text}"

        # Print without newline
        sys.stdout.write(output)
        sys.stdout.flush()

    def finish(self, text: str = "Complete"):
        """Finish progress bar with final text."""
        self.update(self.total, text)
        print()  # New line


class Spinner:
    """Simple spinner for long-running operations."""

    FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    def __init__(self, text: str = "Processing"):
        """
        Initialize spinner.

        Args:
            text: Text to show alongside spinner
        """
        self.text = text
        self.frame = 0
        self.running = False

    def start(self):
        """Start spinner (non-blocking)."""
        self.running = True
        self._update()

    def _update(self):
        """Update spinner frame."""
        if not self.running:
            return

        frame = self.FRAMES[self.frame % len(self.FRAMES)]
        sys.stdout.write(f"\r{TerminalColors.CYAN}{frame}{TerminalColors.RESET} {self.text}")
        sys.stdout.flush()
        self.frame += 1

    def stop(self, final_text: Optional[str] = None):
        """
        Stop spinner.

        Args:
            final_text: Optional final text to replace spinner
        """
        self.running = False
        if final_text:
            sys.stdout.write(f"\r{TerminalColors.GREEN}✓{TerminalColors.RESET} {final_text}\n")
        else:
            sys.stdout.write("\r" + " " * (len(self.text) + 3) + "\r")
        sys.stdout.flush()


def format_file_size(size_bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def format_time(seconds: float) -> str:
    """Format seconds as human-readable time."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds / 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"


def print_table(headers: list, rows: list, indent: int = 0):
    """
    Print a simple table.

    Args:
        headers: List of column headers
        rows: List of row data (list of lists)
        indent: Number of spaces to indent table
    """
    if not rows:
        return

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Print header
    prefix = " " * indent
    header_line = " │ ".join(
        f"{TerminalColors.BOLD}{h:<{w}}{TerminalColors.RESET}"
        for h, w in zip(headers, widths)
    )
    print(f"{prefix}{header_line}")

    # Print separator
    separator = "─┼─".join("─" * w for w in widths)
    print(f"{prefix}{separator}")

    # Print rows
    for row in rows:
        row_line = " │ ".join(f"{str(c):<{w}}" for c, w in zip(row, widths))
        print(f"{prefix}{row_line}")


# Verbose mode state
_verbose = False


def set_verbose(enabled: bool):
    """Enable or disable verbose mode."""
    global _verbose
    _verbose = enabled


def is_verbose() -> bool:
    """Check if verbose mode is enabled."""
    return _verbose


def print_verbose(text: str):
    """Print message only in verbose mode."""
    if _verbose:
        print(f"{TerminalColors.GRAY}[VERBOSE]{TerminalColors.RESET} {text}")
