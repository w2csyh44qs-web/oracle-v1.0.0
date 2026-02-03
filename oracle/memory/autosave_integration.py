"""
Autosave Integration - Memory-Powered Context Updates

Integrates Hippocampus memory and ContextUpdater with Oracle's autosave workflow.
Provides simple functions to generate and apply context updates during sessions.

Usage:
    # At end of Oracle session (before autosave)
    from oracle.memory.autosave_integration import suggest_context_updates

    suggest_context_updates(session_id="O105", context="Oracle", days_back=1)

Author: Oracle Brain Cell Architecture (P30 Phase 3)
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from oracle.memory import Hippocampus, ContextUpdater


def suggest_context_updates(
    session_id: str = "unknown",
    context: str = "Oracle",
    days_back: int = 1,
    auto_apply_threshold: float = 0.8,
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Generate and optionally apply context updates for current session.

    This is designed to be called at the end of an Oracle session,
    before running autosave. It analyzes recent observations and
    generates markdown updates for context files.

    Args:
        session_id: Current session ID (e.g., "O105")
        context: Current context (Oracle, Dev, Dashboard, etc.)
        days_back: Days to analyze (default: 1 for current session)
        auto_apply_threshold: Confidence threshold for auto-apply (default: 0.8)
        dry_run: If True, preview changes without applying

    Returns:
        Dict with counts: applied, queued, failed
    """
    print(f"\n🧠 Memory-Powered Context Updates for {session_id}")
    print("=" * 60)

    # Initialize components
    hippo = Hippocampus()
    updater = ContextUpdater(hippocampus=hippo)

    # Get session stats
    stats = hippo.get_stats()
    print(f"\n📊 Memory Stats:")
    print(f"   Total Observations: {stats.total_observations}")
    print(f"   By Context: {stats.observations_by_context}")
    print(f"   Database Size: {stats.db_size_mb} MB")

    # Analyze and generate updates
    print(f"\n🔍 Analyzing last {days_back} days...")
    updates = updater.analyze_and_generate(days_back=days_back, context=context)

    if not updates:
        print("   No updates generated.")
        return {"applied": 0, "queued": 0, "failed": 0}

    print(f"   Generated {len(updates)} proposed updates")

    # Count by confidence
    high_conf = [u for u in updates if u.confidence >= auto_apply_threshold]
    medium_conf = [u for u in updates if 0.5 <= u.confidence < auto_apply_threshold]
    low_conf = [u for u in updates if u.confidence < 0.5]

    print(f"\n📈 Confidence Breakdown:")
    print(f"   High (≥{auto_apply_threshold}): {len(high_conf)} updates")
    print(f"   Medium (0.5-{auto_apply_threshold}): {len(medium_conf)} updates")
    print(f"   Low (<0.5): {len(low_conf)} updates")

    # Preview high-confidence updates
    if high_conf:
        print(f"\n✨ High-Confidence Updates (will auto-apply):")
        for update in high_conf[:5]:  # Show first 5
            print(f"   • [{update.confidence:.2f}] {update.section}: {update.reason[:60]}...")

    # Apply updates
    if dry_run:
        print(f"\n🔍 DRY RUN MODE - No changes will be made")

    print(f"\n⚙️  Applying updates (threshold: {auto_apply_threshold})...")
    results = updater.apply_updates(
        auto_apply_threshold=auto_apply_threshold,
        dry_run=dry_run
    )

    print(f"\n📊 Results:")
    print(f"   ✅ Applied: {results['applied']}")
    print(f"   📋 Queued for review: {results['queued']}")
    print(f"   ❌ Failed: {results['failed']}")

    if results['applied'] > 0 and not dry_run:
        print(f"\n💾 Context files updated successfully!")
        print(f"   Review changes in oracle/docs/context/")

    if results['queued'] > 0:
        print(f"\n📝 Queued updates require review:")
        print(f"   Run: python3 oracle/memory/context_updater.py preview")
        print(f"   Apply: python3 oracle/memory/context_updater.py apply 0.5")

    return results


def review_pending_updates(min_confidence: float = 0.0) -> None:
    """
    Review pending context updates that weren't auto-applied.

    Args:
        min_confidence: Minimum confidence threshold to display
    """
    updater = ContextUpdater()
    preview = updater.preview_updates(min_confidence=min_confidence)
    print(preview)


def apply_pending_updates(threshold: float = 0.5, dry_run: bool = False) -> Dict[str, int]:
    """
    Apply pending context updates with specified confidence threshold.

    Args:
        threshold: Confidence threshold (0.0-1.0)
        dry_run: If True, preview without applying

    Returns:
        Dict with counts: applied, queued, failed
    """
    updater = ContextUpdater()
    return updater.apply_updates(auto_apply_threshold=threshold, dry_run=dry_run)


def clear_pending_updates() -> None:
    """Clear all pending context updates."""
    updater = ContextUpdater()
    updater.pending_updates = []
    updater._save_pending_updates()
    print("✅ Cleared all pending updates")


def main():
    """CLI interface for autosave integration."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python autosave_integration.py [suggest|review|apply|clear]")
        print()
        print("Commands:")
        print("  suggest [session_id] [context] [days] - Generate and apply updates for session")
        print("  review [min_conf]                      - Review pending updates")
        print("  apply [threshold] [--dry-run]          - Apply pending updates")
        print("  clear                                  - Clear all pending updates")
        print()
        print("Examples:")
        print("  python autosave_integration.py suggest O105 Oracle 1")
        print("  python autosave_integration.py review 0.5")
        print("  python autosave_integration.py apply 0.5 --dry-run")
        return

    command = sys.argv[1]

    if command == "suggest":
        session_id = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        context = sys.argv[3] if len(sys.argv) > 3 else "Oracle"
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        dry_run = "--dry-run" in sys.argv

        suggest_context_updates(
            session_id=session_id,
            context=context,
            days_back=days,
            dry_run=dry_run
        )

    elif command == "review":
        min_conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
        review_pending_updates(min_confidence=min_conf)

    elif command == "apply":
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
        dry_run = "--dry-run" in sys.argv
        apply_pending_updates(threshold=threshold, dry_run=dry_run)

    elif command == "clear":
        clear_pending_updates()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
