#!/usr/bin/env python3
"""
Memory Analytics Dashboard

CLI dashboard for memory analytics with rich terminal UI.
Shows per-agent memory usage, growth trends, pattern detection results,
and actionable insights.

Usage:
    python -m memory dashboard --agent <id> --days 7
    python -m memory dashboard --all --days 30
    python -m memory export --format json --output report.json
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from .models import MemoryEntry, MemoryType
from .store import MemoryStore


class MemoryDashboard:
    """Analytics dashboard for agent memory data."""
    
    def __init__(self, store: Optional[MemoryStore] = None):
        """Initialize dashboard with memory store."""
        self.store = store or MemoryStore()
    
    def collect_stats(self, agent_id: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
        """
        Collect comprehensive memory statistics.
        
        Args:
            agent_id: Specific agent to analyze (None for all)
            days: Number of days to analyze
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            'agents': {},
            'total_memories': 0,
            'total_size_bytes': 0,
            'memory_types': defaultdict(int),
            'top_tags': defaultdict(int),
            'age_distribution': defaultdict(int),
            'growth_data': defaultdict(lambda: defaultdict(int)),
            'pattern_results': None
        }
        
        # Determine which agents to analyze
        if agent_id:
            agent_dirs = [self.store.base_path / agent_id]
        else:
            agent_dirs = [d for d in self.store.base_path.iterdir() if d.is_dir()]
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        for agent_dir in agent_dirs:
            if not agent_dir.exists():
                continue
            
            agent_name = agent_dir.name
            agent_stats = {
                'total': 0,
                'size_bytes': 0,
                'types': defaultdict(int),
                'tags': defaultdict(int),
                'oldest': None,
                'newest': None,
                'daily_counts': defaultdict(int)
            }
            
            # Process all JSONL files
            for jsonl_file in agent_dir.glob("*.jsonl"):
                # Skip archived files
                if 'archive' in str(jsonl_file):
                    continue
                
                file_size = jsonl_file.stat().st_size
                agent_stats['size_bytes'] += file_size
                
                file_date = jsonl_file.stem
                if file_date < cutoff_str:
                    continue
                
                with open(jsonl_file, 'r') as f:
                    for line in f:
                        try:
                            entry = MemoryEntry.from_json(line.strip())
                            agent_stats['total'] += 1
                            agent_stats['types'][entry.type.value] += 1
                            
                            # Track dates
                            entry_date = entry.timestamp[:10]
                            agent_stats['daily_counts'][entry_date] += 1
                            
                            if agent_stats['oldest'] is None or entry.timestamp < agent_stats['oldest']:
                                agent_stats['oldest'] = entry.timestamp
                            if agent_stats['newest'] is None or entry.timestamp > agent_stats['newest']:
                                agent_stats['newest'] = entry.timestamp
                            
                            # Collect tags
                            for tag in entry.tags:
                                agent_stats['tags'][tag] += 1
                                stats['top_tags'][tag] += 1
                            
                            # Age bucket
                            age_days = (datetime.utcnow() - datetime.fromisoformat(entry.timestamp.replace('Z', ''))).days
                            age_bucket = self._get_age_bucket(age_days)
                            stats['age_distribution'][age_bucket] += 1
                            
                            # Growth data
                            stats['growth_data'][agent_name][entry_date] += 1
                            
                        except (json.JSONDecodeError, ValueError):
                            continue
            
            # Aggregate to global stats
            stats['agents'][agent_name] = agent_stats
            stats['total_memories'] += agent_stats['total']
            stats['total_size_bytes'] += agent_stats['size_bytes']
            
            for mem_type, count in agent_stats['types'].items():
                stats['memory_types'][mem_type] += count
        
        return stats
    
    def _get_age_bucket(self, days: int) -> str:
        """Convert days to age bucket."""
        if days < 1:
            return '0-1 days'
        elif days < 7:
            return '1-7 days'
        elif days < 30:
            return '7-30 days'
        elif days < 90:
            return '30-90 days'
        else:
            return '90+ days'
    
    def compute_growth_rate(self, stats: Dict, days: int = 7) -> Dict[str, float]:
        """Compute memory growth rate per agent."""
        rates = {}
        
        for agent_name, growth_data in stats['growth_data'].items():
            if not growth_data:
                rates[agent_name] = 0.0
                continue
            
            total = sum(growth_data.values())
            rates[agent_name] = round(total / days, 2) if days > 0 else 0.0
        
        return rates
    
    def get_pattern_results(self) -> Optional[Dict]:
        """Get pattern detection results if available."""
        try:
            # Import pattern detector
            sys.path.insert(0, str(Path(__file__).parent.parent / 'improvement'))
            from improvement.pattern_detector import PatternDetector
            
            detector = PatternDetector()
            results = detector.detect()
            return results
        except Exception:
            return None
    
    def render_rich(self, stats: Dict, days: int, show_patterns: bool = True) -> str:
        """Render dashboard using rich terminal UI."""
        try:
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            from rich import box
            
            console = Console()
            output = []
            
            # Title
            output.append(Panel(
                f"[bold cyan]Memory Analytics Dashboard[/bold cyan]\n"
                f"Period: Last {days} days | Total: {stats['total_memories']} memories | "
                f"Size: {self._format_bytes(stats['total_size_bytes'])}",
                box=box.ROUNDED
            ))
            
            # Per-agent table
            agent_table = Table(title="Agent Memory Usage", box=box.SIMPLE)
            agent_table.add_column("Agent", style="cyan")
            agent_table.add_column("Memories", justify="right")
            agent_table.add_column("Size", justify="right")
            agent_table.add_column("Oldest", style="dim")
            agent_table.add_column("Newest", style="green")
            
            for agent_name, agent_stats in sorted(stats['agents'].items()):
                if agent_stats['total'] == 0:
                    continue
                agent_table.add_row(
                    agent_name,
                    str(agent_stats['total']),
                    self._format_bytes(agent_stats['size_bytes']),
                    (agent_stats['oldest'] or 'N/A')[:10],
                    (agent_stats['newest'] or 'N/A')[:10]
                )
            
            output.append(agent_table)
            
            # Growth rates
            rates = self.compute_growth_rate(stats, days)
            if rates:
                growth_table = Table(title="Growth Rate (memories/day)", box=box.SIMPLE)
                growth_table.add_column("Agent", style="cyan")
                growth_table.add_column("Rate", justify="right")
                growth_table.add_column("Trend", style="yellow")
                
                for agent_name, rate in sorted(rates.items(), key=lambda x: -x[1]):
                    trend = "↑" if rate > 1 else "→" if rate > 0 else "↓"
                    growth_table.add_row(agent_name, f"{rate:.2f}", trend)
                
                output.append(growth_table)
            
            # Memory types breakdown
            if stats['memory_types']:
                type_table = Table(title="Memory Types", box=box.SIMPLE)
                type_table.add_column("Type", style="magenta")
                type_table.add_column("Count", justify="right")
                type_table.add_column("Percentage", justify="right")
                
                total = sum(stats['memory_types'].values())
                for mem_type, count in sorted(stats['memory_types'].items(), key=lambda x: -x[1]):
                    pct = (count / total * 100) if total > 0 else 0
                    type_table.add_row(mem_type, str(count), f"{pct:.1f}%")
                
                output.append(type_table)
            
            # Top tags
            if stats['top_tags']:
                tag_table = Table(title="Top Tags", box=box.SIMPLE)
                tag_table.add_column("Tag", style="yellow")
                tag_table.add_column("Count", justify="right")
                
                for tag, count in sorted(stats['top_tags'].items(), key=lambda x: -x[1])[:10]:
                    tag_table.add_row(tag, str(count))
                
                output.append(tag_table)
            
            # Age distribution histogram
            age_table = Table(title="Memory Age Distribution", box=box.SIMPLE)
            age_table.add_column("Age Bucket", style="blue")
            age_table.add_column("Count", justify="right")
            age_table.add_column("Histogram")
            
            total_age = sum(stats['age_distribution'].values())
            max_count = max(stats['age_distribution'].values()) if stats['age_distribution'] else 1
            
            for bucket in ['0-1 days', '1-7 days', '7-30 days', '30-90 days', '90+ days']:
                count = stats['age_distribution'].get(bucket, 0)
                bar = '█' * int(count / max_count * 20) if max_count > 0 else ''
                age_table.add_row(bucket, str(count), bar)
            
            output.append(age_table)
            
            # Pattern detection results
            if show_patterns:
                patterns = self.get_pattern_results()
                if patterns and patterns.get('promotion_candidates'):
                    pattern_table = Table(title="Pattern Detection Results", box=box.SIMPLE)
                    pattern_table.add_column("Priority", style="red")
                    pattern_table.add_column("Pattern")
                    pattern_table.add_column("Frequency", justify="right")
                    pattern_table.add_column("Agents", justify="right")
                    
                    for candidate in patterns['promotion_candidates'][:5]:
                        priority_style = "red" if candidate['priority'] == 'HIGH' else "yellow" if candidate['priority'] == 'MEDIUM' else "dim"
                        pattern_table.add_row(
                            f"[{priority_style}]{candidate['priority']}[/{priority_style}]",
                            candidate['pattern'][:30],
                            str(candidate['frequency']),
                            str(candidate['num_agents'])
                        )
                    
                    output.append(pattern_table)
            
            # Render all
            rendered = []
            for item in output:
                with console.capture() as capture:
                    console.print(item)
                rendered.append(capture.get())
            
            return '\n'.join(rendered)
            
        except ImportError:
            # Fallback to simple text output
            return self.render_simple(stats, days, show_patterns)
    
    def render_simple(self, stats: Dict, days: int, show_patterns: bool = True) -> str:
        """Render dashboard as simple text (fallback without rich)."""
        lines = []
        
        lines.append("=" * 60)
        lines.append("MEMORY ANALYTICS DASHBOARD")
        lines.append(f"Period: Last {days} days")
        lines.append(f"Total memories: {stats['total_memories']}")
        lines.append(f"Total size: {self._format_bytes(stats['total_size_bytes'])}")
        lines.append("=" * 60)
        
        # Per-agent stats
        lines.append("\n--- Agent Memory Usage ---")
        for agent_name, agent_stats in sorted(stats['agents'].items()):
            if agent_stats['total'] == 0:
                continue
            lines.append(f"{agent_name}: {agent_stats['total']} memories, {self._format_bytes(agent_stats['size_bytes'])}")
        
        # Growth rates
        rates = self.compute_growth_rate(stats, days)
        if rates:
            lines.append("\n--- Growth Rate (memories/day) ---")
            for agent_name, rate in sorted(rates.items(), key=lambda x: -x[1]):
                lines.append(f"{agent_name}: {rate:.2f}")
        
        # Memory types
        if stats['memory_types']:
            lines.append("\n--- Memory Types ---")
            total = sum(stats['memory_types'].values())
            for mem_type, count in sorted(stats['memory_types'].items(), key=lambda x: -x[1]):
                pct = (count / total * 100) if total > 0 else 0
                lines.append(f"{mem_type}: {count} ({pct:.1f}%)")
        
        # Top tags
        if stats['top_tags']:
            lines.append("\n--- Top Tags ---")
            for tag, count in sorted(stats['top_tags'].items(), key=lambda x: -x[1])[:10]:
                lines.append(f"{tag}: {count}")
        
        # Age distribution
        lines.append("\n--- Memory Age Distribution ---")
        total_age = sum(stats['age_distribution'].values())
        max_count = max(stats['age_distribution'].values()) if stats['age_distribution'] else 1
        
        for bucket in ['0-1 days', '1-7 days', '7-30 days', '30-90 days', '90+ days']:
            count = stats['age_distribution'].get(bucket, 0)
            bar = '█' * int(count / max_count * 20) if max_count > 0 else ''
            lines.append(f"{bucket}: {count} {bar}")
        
        return '\n'.join(lines)
    
    def _format_bytes(self, size: int) -> str:
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if abs(size) < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def export(self, stats: Dict, format: str = 'json', output_path: Optional[str] = None) -> str:
        """
        Export analytics data to JSON or CSV.
        
        Args:
            stats: Statistics dictionary
            format: 'json' or 'csv'
            output_path: Optional file path to write
            
        Returns:
            Exported data as string
        """
        if format == 'json':
            # Convert defaultdicts to regular dicts
            export_data = {
                'generated_at': datetime.utcnow().isoformat() + 'Z',
                'total_memories': stats['total_memories'],
                'total_size_bytes': stats['total_size_bytes'],
                'agents': {
                    name: {
                        'total': data['total'],
                        'size_bytes': data['size_bytes'],
                        'types': dict(data['types']),
                        'tags': dict(data['tags']),
                        'oldest': data['oldest'],
                        'newest': data['newest']
                    }
                    for name, data in stats['agents'].items()
                },
                'memory_types': dict(stats['memory_types']),
                'top_tags': dict(stats['top_tags']),
                'age_distribution': dict(stats['age_distribution']),
                'growth_rates': self.compute_growth_rate(stats)
            }
            
            result = json.dumps(export_data, indent=2)
            
        elif format == 'csv':
            lines = ['agent,memories,size_bytes,type,tag,count']
            
            for agent_name, agent_stats in stats['agents'].items():
                for mem_type, count in agent_stats['types'].items():
                    lines.append(f"{agent_name},{agent_stats['total']},{agent_stats['size_bytes']},{mem_type},,{count}")
                
                for tag, count in agent_stats['tags'].items():
                    lines.append(f"{agent_name},{agent_stats['total']},{agent_stats['size_bytes']},,{tag},{count}")
            
            result = '\n'.join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_path:
            Path(output_path).write_text(result)
        
        return result


def main():
    """CLI entry point for dashboard."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Memory Analytics Dashboard',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Dashboard command
    dash_parser = subparsers.add_parser('dashboard', help='Show memory analytics dashboard')
    dash_parser.add_argument('--agent', help='Filter by specific agent ID')
    dash_parser.add_argument('--all', action='store_true', help='Show all agents')
    dash_parser.add_argument('--days', type=int, default=7, help='Days to analyze (default: 7)')
    dash_parser.add_argument('--no-patterns', action='store_true', help='Skip pattern detection')
    dash_parser.add_argument('--simple', action='store_true', help='Simple text output (no rich UI)')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export analytics data')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                              help='Export format (default: json)')
    export_parser.add_argument('--output', '-o', help='Output file path')
    export_parser.add_argument('--agent', help='Filter by specific agent ID')
    export_parser.add_argument('--days', type=int, default=7, help='Days to analyze (default: 7)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    dashboard = MemoryDashboard()
    
    if args.command == 'dashboard':
        stats = dashboard.collect_stats(agent_id=args.agent, days=args.days)
        
        if args.simple:
            output = dashboard.render_simple(stats, args.days, show_patterns=not args.no_patterns)
        else:
            output = dashboard.render_rich(stats, args.days, show_patterns=not args.no_patterns)
        
        print(output)
    
    elif args.command == 'export':
        stats = dashboard.collect_stats(agent_id=args.agent, days=args.days)
        result = dashboard.export(stats, format=args.format, output_path=args.output)
        
        if not args.output:
            print(result)
        else:
            print(f"Exported to: {args.output}")


if __name__ == '__main__':
    main()
