#!/usr/bin/env python3
"""
GOATED Trend Detection
Main script with source toggle system

ARCHIVED: December 17, 2025 (Session D30)
REASON: Functionality merged into content_pipeline.py (L0 entry point)
        and web_search_trend_detector.py (sources sub-menu).
PRESERVE: Multi-source orchestration pattern (TREND_SOURCES dict) for
        future reference when implementing additional trend sources.
"""

import os
import json
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TrendDetection:
    """Main trend detection orchestrator with source toggles"""

    # Available trend sources
    TREND_SOURCES = {
        'websearch_trends': {
            'name': 'Web Search (Tavily)',
            'active': True,  # Default active
            'script': 'web_search_trend_detector.py',
            'description': 'Searches Reddit, Twitter, betting forums'
        },
        'reddit_trends': {
            'name': 'Reddit Direct',
            'active': False,
            'script': None,  # Placeholder - covered by websearch
            'description': 'Direct Reddit API scraping (covered by web search)'
        },
        'covers_trends': {
            'name': 'Covers.com Forum',
            'active': False,
            'script': None,  # Placeholder
            'description': 'Betting forum discussions (covered by web search)'
        },
        'action_network_trends': {
            'name': 'Action Network',
            'active': False,
            'script': None,  # Future: professional betting insights
            'description': 'Sharp money tracking (future integration)'
        },
        'youtube_shorts_trends': {
            'name': 'YouTube Shorts',
            'active': False,
            'script': None,  # Future: video content trends
            'description': 'Trending short-form video content (future)'
        },
        'instagram_trends': {
            'name': 'Instagram',
            'active': False,
            'script': None,  # Future: Instagram scraping
            'description': 'Instagram betting content (future)'
        },
        'x_trends': {
            'name': 'X/Twitter Direct',
            'active': False,
            'script': None,  # Placeholder - covered by websearch
            'description': 'Direct Twitter API (covered by web search)'
        },
        'tiktok_trends': {
            'name': 'TikTok',
            'active': False,
            'script': None,  # Future: TikTok API
            'description': 'Viral TikTok betting content (future)'
        },
        'discord_trends': {
            'name': 'Discord Communities',
            'active': False,
            'script': None,  # Future: Discord scraping
            'description': 'Real-time betting discussions (future)'
        }
    }

    def __init__(self):
        """Initialize trend detection"""
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)

    def display_sources(self):
        """Display available trend sources with toggle status"""
        print("\n" + "="*80)
        print("TREND SOURCES")
        print("="*80)

        for i, (slug, source) in enumerate(self.TREND_SOURCES.items(), 1):
            status = "🟢 ACTIVE" if source['active'] else "🔴 INACTIVE"
            available = "✓" if source['script'] else "⚠ (future)"
            print(f"{i}. {status} {available} - {source['name']}")
            print(f"   {source['description']}")

        print("\n" + "="*80)

        # Show summary
        active_count = len([s for s in self.TREND_SOURCES.values() if s['active']])
        available_count = len([s for s in self.TREND_SOURCES.values() if s['script']])

        print(f"Active: {active_count} | Available: {available_count} | Total: {len(self.TREND_SOURCES)}")
        print("="*80)

    def toggle_source(self):
        """Toggle a source on/off"""
        print("\n" + "="*80)
        print("TOGGLE TREND SOURCE")
        print("="*80)

        source_list = list(self.TREND_SOURCES.items())

        for i, (slug, source) in enumerate(source_list, 1):
            status = "✓" if source['active'] else "✗"
            print(f"{i}. [{status}] {source['name']}")

        choice = input("\nEnter number to toggle (or 'done'): ").strip()

        if choice.lower() in ['done', 'd', '']:
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(source_list):
                slug = source_list[idx][0]
                source = self.TREND_SOURCES[slug]

                # Check if source is available
                if not source['script']:
                    print(f"⚠️  {source['name']} is not yet implemented (future)")
                    return

                # Toggle
                source['active'] = not source['active']
                status = "ACTIVE" if source['active'] else "INACTIVE"
                print(f"✓ {source['name']} is now {status}")
            else:
                print("❌ Invalid number")
        except ValueError:
            print("❌ Invalid input")

    def run_active_sources(self):
        """Run all active trend detection sources"""
        print("\n" + "="*80)
        print("RUNNING ACTIVE SOURCES")
        print("="*80)

        active_sources = {
            slug: source for slug, source in self.TREND_SOURCES.items()
            if source['active'] and source['script']
        }

        if not active_sources:
            print("❌ No active sources selected!")
            return False

        print(f"Running {len(active_sources)} active source(s)...\n")

        # Run each active source
        for slug, source in active_sources.items():
            print(f"\n{'='*80}")
            print(f"Running: {source['name']}")
            print(f"{'='*80}")

            if slug == 'websearch_trends':
                # Run web search
                os.system(f"python3 scripts/{source['script']}")

        print("\n" + "="*80)
        print("✅ All active sources completed!")
        print("="*80)

        return True

    def combine_trends(self):
        """Combine all approved trends from active sources into all_trends.json"""
        print("\n" + "="*80)
        print("COMBINING APPROVED TRENDS")
        print("="*80)

        combined = {
            'generated_at': datetime.now().isoformat(),
            'sources': {}
        }

        # Load trends from each active source
        active_sources = [
            slug for slug, source in self.TREND_SOURCES.items()
            if source['active'] and source['script']
        ]

        for slug in active_sources:
            # Try approved file first, fallback to base file
            approved_file = f"{self.output_dir}/{slug.replace('_trends', '_trends_approved')}.json"
            base_file = f"{self.output_dir}/{slug}.json"

            loaded = False

            # Try approved file first
            try:
                with open(approved_file, 'r') as f:
                    data = json.load(f)
                    combined['sources'][slug] = data
                    print(f"✓ Loaded {len(data.get('all_trends', []))} approved trends from {slug}")
                    loaded = True
            except FileNotFoundError:
                pass

            # Fallback to base file if no approved file
            if not loaded:
                try:
                    with open(base_file, 'r') as f:
                        data = json.load(f)
                        combined['sources'][slug] = data
                        print(f"⚠️  No approved file found, using {len(data.get('all_trends', []))} trends from {slug}")
                except FileNotFoundError:
                    print(f"⚠️  {slug} not found, skipping")
                    continue

        # Save combined file (overwrites previous)
        output_file = f"{self.output_dir}/all_trends.json"
        with open(output_file, 'w') as f:
            json.dump(combined, f, indent=2)

        total_trends = sum([
            len(source_data.get('all_trends', []))
            for source_data in combined['sources'].values()
        ])

        print(f"\n💾 Combined trends saved to: {output_file}")
        print(f"   Total trends: {total_trends} from {len(combined['sources'])} source(s)")
        print(f"   Note: Using approved trends where available")
        print("="*80)

    def run(self):
        """Main workflow"""
        print("🚀 GOATED TREND DETECTION LAYER\n")

        # Display sources
        self.display_sources()

        # Configuration loop
        while True:
            print("\nOPTIONS:")
            print("  [v]iew - View source status")
            print("  [t]oggle - Toggle sources on/off")
            print("  [r]un - Run active sources and combine trends")
            print("  [x]exit - Exit")
            print()

            choice = input("Choose action: ").strip().lower()

            if choice in ['v', 'view']:
                self.display_sources()
            elif choice in ['t', 'toggle']:
                self.toggle_source()
            elif choice in ['r', 'run']:
                # Run active sources
                success = self.run_active_sources()
                if success:
                    # Combine into all_trends.json
                    self.combine_trends()

                    print("\n✅ Trend detection complete!")
                    print("\nNext: Configure calendar & segments")
                    print("    python scripts/calendar_config.py regular_season week1")
                break
            elif choice in ['x', 'exit']:
                print("\n⚠️  Exiting...")
                exit(0)
            else:
                print("❌ Invalid choice")


if __name__ == "__main__":
    detector = TrendDetection()
    detector.run()
