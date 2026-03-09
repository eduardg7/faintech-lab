#!/usr/bin/env python3
"""
Self-Improvement Pattern Detector

Reads ERRORS.md and LEARNINGS.md from all agents, clusters similar entries,
and outputs promotion candidates for system-wide rule extraction.

Usage:
    python pattern_detector.py --threshold 3 --output promotion_candidates.json
"""

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple


class PatternDetector:
    """Detects recurring patterns in agent learning and error logs."""
    
    def __init__(self, agents_dir: str = "~/.openclaw/agents", threshold: int = 3):
        self.agents_dir = Path(agents_dir).expanduser()
        self.threshold = threshold
        self.patterns: Dict[str, Dict] = defaultdict(lambda: {
            'count': 0,
            'agents': set(),
            'entries': [],
            'suggested_rule': ''
        })
    
    def extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from text."""
        # Remove markdown headers and special chars
        text = re.sub(r'#+\s+', '', text)
        text = re.sub(r'[*_`]', '', text)
        text = text.lower()
        
        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'been', 'be',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
            'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
            'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
            'into', 'over', 'after', 'before', 'between', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'as', 'if', 'then', 'because', 'while', 'during'
        }
        
        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', text)
        keywords = {w for w in words if w not in stop_words}
        
        return keywords
    
    def categorize_entry(self, content: str) -> str:
        """Categorize entry type based on content."""
        content_lower = content.lower()
        
        if 'error' in content_lower or 'exception' in content_lower or 'fail' in content_lower:
            return 'error'
        elif 'correction' in content_lower or 'actually' in content_lower or 'wrong' in content_lower:
            return 'correction'
        elif 'pattern' in content_lower or 'recurring' in content_lower:
            return 'recurring_pattern'
        elif 'security' in content_lower or 'auth' in content_lower or 'permission' in content_lower:
            return 'security'
        elif 'performance' in content_lower or 'slow' in content_lower or 'timeout' in content_lower:
            return 'performance'
        elif 'test' in content_lower or 'coverage' in content_lower:
            return 'testing'
        elif 'git' in content_lower or 'branch' in content_lower or 'merge' in content_lower:
            return 'git_workflow'
        elif 'pr' in content_lower or 'review' in content_lower:
            return 'code_review'
        else:
            return 'general'
    
    def suggest_rule(self, pattern_key: str, category: str, count: int) -> str:
        """Generate a suggested rule for a pattern."""
        templates = {
            'error': f"When encountering {pattern_key}, check logs and escalate after 2 failed attempts",
            'correction': f"Before implementing {pattern_key}, verify approach with documentation or team",
            'recurring_pattern': f"Automate {pattern_key} detection and create checklist for future instances",
            'security': f"Always validate {pattern_key} before processing - security-critical pattern",
            'performance': f"Monitor {pattern_key} metrics and alert when threshold exceeded",
            'testing': f"Add test coverage for {pattern_key} scenarios before marking done",
            'git_workflow': f"Follow {pattern_key} git protocol: branch, commit, PR, verify before merge",
            'code_review': f"During review, check for {pattern_key} issues using standard checklist",
            'general': f"Create standard operating procedure for {pattern_key} occurrences"
        }
        
        return templates.get(category, templates['general'])
    
    def compute_similarity(self, keywords1: Set[str], keywords2: Set[str]) -> float:
        """Compute Jaccard similarity between two keyword sets."""
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = len(keywords1 & keywords2)
        union = len(keywords1 | keywords2)
        
        return intersection / union if union > 0 else 0.0
    
    def parse_entry(self, content: str, agent_id: str, file_type: str) -> List[Dict]:
        """Parse markdown entry into structured format."""
        entries = []
        
        # Split by markdown headers (##)
        sections = re.split(r'\n##\s+', content)
        
        for section in sections[1:]:  # Skip first section (file header)
            lines = section.strip().split('\n')
            if not lines:
                continue
            
            title = lines[0].strip()
            body = '\n'.join(lines[1:]).strip()
            
            if not title or not body:
                continue
            
            # Extract metadata
            entry = {
                'title': title,
                'content': body,
                'agent_id': agent_id,
                'file_type': file_type,
                'keywords': self.extract_keywords(title + ' ' + body),
                'category': self.categorize_entry(title + ' ' + body)
            }
            
            entries.append(entry)
        
        return entries
    
    def scan_agent_files(self) -> List[Dict]:
        """Scan all agent .learnings directories for ERRORS.md and LEARNINGS.md."""
        all_entries = []
        
        if not self.agents_dir.exists():
            print(f"Warning: Agents directory not found: {self.agents_dir}")
            return all_entries
        
        for agent_dir in self.agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            
            agent_id = agent_dir.name
            learnings_dir = agent_dir / ".learnings"
            
            if not learnings_dir.exists():
                continue
            
            # Read ERRORS.md
            errors_file = learnings_dir / "ERRORS.md"
            if errors_file.exists():
                content = errors_file.read_text()
                entries = self.parse_entry(content, agent_id, "ERRORS")
                all_entries.extend(entries)
            
            # Read LEARNINGS.md
            learnings_file = learnings_dir / "LEARNINGS.md"
            if learnings_file.exists():
                content = learnings_file.read_text()
                entries = self.parse_entry(content, agent_id, "LEARNINGS")
                all_entries.extend(entries)
        
        return all_entries
    
    def cluster_patterns(self, entries: List[Dict]) -> None:
        """Cluster entries by similarity and track patterns."""
        # Group by category first
        by_category = defaultdict(list)
        for entry in entries:
            by_category[entry['category']].append(entry)
        
        # Within each category, cluster by keyword similarity
        for category, category_entries in by_category.items():
            for i, entry1 in enumerate(category_entries):
                # Create pattern key from top keywords
                top_keywords = sorted(entry1['keywords'])[:5]
                pattern_key = '_'.join(top_keywords[:3]) if top_keywords else 'unknown'
                
                # Find similar entries
                similar_found = False
                for existing_key in list(self.patterns.keys()):
                    # Check if this is the same pattern (high similarity)
                    existing_keywords = set(existing_key.split('_'))
                    similarity = self.compute_similarity(entry1['keywords'], existing_keywords)
                    
                    if similarity > 0.5:  # 50% similarity threshold
                        self.patterns[existing_key]['count'] += 1
                        self.patterns[existing_key]['agents'].add(entry1['agent_id'])
                        self.patterns[existing_key]['entries'].append({
                            'title': entry1['title'],
                            'agent_id': entry1['agent_id'],
                            'file_type': entry1['file_type']
                        })
                        similar_found = True
                        break
                
                if not similar_found:
                    # Create new pattern
                    self.patterns[pattern_key]['count'] = 1
                    self.patterns[pattern_key]['agents'].add(entry1['agent_id'])
                    self.patterns[pattern_key]['entries'].append({
                        'title': entry1['title'],
                        'agent_id': entry1['agent_id'],
                        'file_type': entry1['file_type']
                    })
                    self.patterns[pattern_key]['suggested_rule'] = self.suggest_rule(
                        pattern_key, category, 1
                    )
    
    def detect(self) -> Dict:
        """Main detection pipeline."""
        print(f"Scanning agent learnings in: {self.agents_dir}")
        
        # Step 1: Scan files
        entries = self.scan_agent_files()
        print(f"Found {len(entries)} entries across all agents")
        
        # Step 2: Cluster patterns
        self.cluster_patterns(entries)
        print(f"Identified {len(self.patterns)} unique patterns")
        
        # Step 3: Filter promotion candidates
        promotion_candidates = []
        
        for pattern_key, pattern_data in self.patterns.items():
            frequency = pattern_data['count']
            affected_agents = len(pattern_data['agents'])
            
            # Flag as HIGH priority if: 3+ occurrences across 2+ agents
            if frequency >= self.threshold and affected_agents >= 2:
                priority = 'HIGH'
            elif frequency >= self.threshold:
                priority = 'MEDIUM'
            elif frequency >= 2:
                priority = 'LOW'
            else:
                continue  # Skip single occurrences
            
            candidate = {
                'pattern': pattern_key,
                'frequency': frequency,
                'affected_agents': sorted(list(pattern_data['agents'])),
                'num_agents': affected_agents,
                'suggested_rule': pattern_data['suggested_rule'],
                'priority': priority,
                'sample_entries': pattern_data['entries'][:3],  # First 3 examples
                'detected_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            promotion_candidates.append(candidate)
        
        # Sort by priority (HIGH first) then frequency
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        promotion_candidates.sort(
            key=lambda x: (priority_order[x['priority']], -x['frequency'])
        )
        
        return {
            'metadata': {
                'scan_timestamp': datetime.utcnow().isoformat() + 'Z',
                'agents_directory': str(self.agents_dir),
                'total_entries_scanned': len(entries),
                'total_patterns_found': len(self.patterns),
                'promotion_threshold': self.threshold,
                'total_promotion_candidates': len(promotion_candidates)
            },
            'promotion_candidates': promotion_candidates
        }


def main():
    parser = argparse.ArgumentParser(
        description='Detect recurring patterns in agent learning logs'
    )
    parser.add_argument(
        '--agents-dir',
        default='~/.openclaw/agents',
        help='Directory containing agent folders (default: ~/.openclaw/agents)'
    )
    parser.add_argument(
        '--threshold',
        type=int,
        default=3,
        help='Minimum frequency threshold for promotion candidates (default: 3)'
    )
    parser.add_argument(
        '--output',
        default='promotion_candidates.json',
        help='Output file path (default: promotion_candidates.json)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print verbose output'
    )
    
    args = parser.parse_args()
    
    detector = PatternDetector(
        agents_dir=args.agents_dir,
        threshold=args.threshold
    )
    
    results = detector.detect()
    
    # Write output
    output_path = Path(args.output)
    with output_path.open('w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results written to: {output_path}")
    print(f"  Total entries scanned: {results['metadata']['total_entries_scanned']}")
    print(f"  Total patterns found: {results['metadata']['total_patterns_found']}")
    print(f"  Promotion candidates: {results['metadata']['total_promotion_candidates']}")
    
    if args.verbose and results['promotion_candidates']:
        print("\n=== Promotion Candidates ===")
        for candidate in results['promotion_candidates']:
            print(f"\n[{candidate['priority']}] {candidate['pattern']}")
            print(f"  Frequency: {candidate['frequency']}")
            print(f"  Agents: {', '.join(candidate['affected_agents'])}")
            print(f"  Suggested Rule: {candidate['suggested_rule']}")


if __name__ == '__main__':
    main()
