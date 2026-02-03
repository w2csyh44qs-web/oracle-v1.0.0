#!/usr/bin/env python3
"""
Oracle Simple Status - Generate HTML status page
Run this to get a quick visual overview without a full dashboard.

Usage:
    python3 oracle/scripts/simple_status.py
    open oracle/reports/status.html
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from oracle.maintenance.microglia import run_audit
from oracle.memory.hippocampus import Hippocampus


def generate_status_html():
    """Generate simple HTML status page."""

    # Get health data
    print("Gathering health data...")
    audit_result = run_audit(quick=True)
    health_score = audit_result.health_score
    issues = audit_result.issues

    # Get memory stats
    print("Gathering memory stats...")
    hippo = Hippocampus()
    stats = hippo.get_stats()

    # Get recent patterns
    recent_patterns = hippo.detect_patterns(days_back=7)

    # Build HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle Status - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 18px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .card h2 {{
            font-size: 20px;
            margin-bottom: 16px;
            color: #333;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }}
        .metric:last-child {{
            border-bottom: none;
        }}
        .metric-label {{
            color: #666;
            font-size: 14px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .health-score {{
            font-size: 64px;
            font-weight: bold;
            text-align: center;
            margin: 20px 0;
            color: {'#22c55e' if health_score >= 80 else '#f59e0b' if health_score >= 60 else '#ef4444'};
        }}
        .issues {{
            list-style: none;
        }}
        .issues li {{
            padding: 8px 12px;
            margin: 8px 0;
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            border-radius: 4px;
            font-size: 14px;
        }}
        .pattern {{
            padding: 12px;
            margin: 8px 0;
            background: #f3f4f6;
            border-radius: 8px;
            font-size: 14px;
        }}
        .pattern-type {{
            display: inline-block;
            padding: 4px 8px;
            background: #667eea;
            color: white;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
            font-size: 14px;
        }}
        .refresh-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            padding: 16px 24px;
            background: white;
            border: none;
            border-radius: 50px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
        }}
        .refresh-btn:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Oracle Status</h1>
            <p>Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>

        <div class="grid">
            <!-- Health Card -->
            <div class="card">
                <h2>🏥 System Health</h2>
                <div class="health-score">{health_score:.0f}</div>
                <p style="text-align: center; color: #666;">Health Score</p>
            </div>

            <!-- Memory Card -->
            <div class="card">
                <h2>🧠 Memory Stats</h2>
                <div class="metric">
                    <span class="metric-label">Total Observations</span>
                    <span class="metric-value">{stats.total_observations}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Patterns Detected</span>
                    <span class="metric-value">{stats.total_patterns}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Database Size</span>
                    <span class="metric-value">{stats.db_size_mb:.1f} MB</span>
                </div>
            </div>

            <!-- Context Card -->
            <div class="card">
                <h2>📝 Context Activity</h2>
                <div class="metric">
                    <span class="metric-label">Oracle Context</span>
                    <span class="metric-value">{stats.observations_by_context.get('Oracle', 0) if stats.observations_by_context else 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Dev Context</span>
                    <span class="metric-value">{stats.observations_by_context.get('Dev', 0) if stats.observations_by_context else 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Dashboard Context</span>
                    <span class="metric-value">{stats.observations_by_context.get('Dashboard', 0) if stats.observations_by_context else 0}</span>
                </div>
            </div>
        </div>

        <!-- Issues Card -->
        <div class="card" style="margin-bottom: 20px;">
            <h2>⚠️ Active Issues ({len(issues)})</h2>
            {f'<ul class="issues">' + ''.join([f'<li>{issue}</li>' for issue in issues[:5]]) + '</ul>' if issues else '<p style="color: #22c55e; text-align: center; padding: 20px;">✓ No issues detected</p>'}
        </div>

        <!-- Patterns Card -->
        <div class="card">
            <h2>🔍 Recent Patterns (Last 7 Days)</h2>
            {generate_patterns_html(recent_patterns[:5])}
        </div>

        <div class="footer">
            <p>Oracle v1.0 - Brain Cell Architecture</p>
            <p>Session O105 - AutomationScript Project</p>
        </div>

        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
    </div>
</body>
</html>
    """

    # Write to file
    output_path = Path(__file__).parent.parent.parent / "oracle" / "reports" / "status.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)

    print(f"✅ Status page generated: {output_path}")
    print(f"   Open with: open {output_path}")

    return output_path


def generate_patterns_html(patterns):
    """Generate HTML for pattern list."""
    if not patterns:
        return '<p style="color: #666; text-align: center; padding: 20px;">No patterns detected</p>'

    html_parts = []
    for pattern in patterns:
        pattern_type = pattern.pattern_type.replace('_', ' ').title()
        description = pattern.description if pattern.description else 'No description'
        confidence = pattern.confidence

        html_parts.append(f"""
        <div class="pattern">
            <span class="pattern-type">{pattern_type}</span>
            <p>{description}</p>
            <small style="color: #666;">Confidence: {confidence:.0%} | Count: {pattern.occurrence_count}</small>
        </div>
        """)

    return ''.join(html_parts)


if __name__ == "__main__":
    generate_status_html()
