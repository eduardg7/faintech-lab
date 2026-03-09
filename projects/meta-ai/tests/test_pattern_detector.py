#!/usr/bin/env python3
"""
Tests for Pattern Detector

Run with: python -m pytest tests/test_pattern_detector.py -v
"""

import json
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from improvement.pattern_detector import PatternDetector


@pytest.fixture
def fixture_agents_dir():
    """Path to test fixture agents directory."""
    return Path(__file__).parent / 'fixtures' / 'agents'


@pytest.fixture
def detector(fixture_agents_dir):
    """PatternDetector instance with test fixtures."""
    return PatternDetector(agents_dir=str(fixture_agents_dir), threshold=1)


class TestPatternDetector:
    """Test suite for PatternDetector."""
    
    def test_initialization(self, fixture_agents_dir):
        """Test detector initializes correctly."""
        detector = PatternDetector(agents_dir=str(fixture_agents_dir))
        assert detector.agents_dir == fixture_agents_dir
        assert detector.threshold == 3  # Default
    
    def test_extract_keywords(self, detector):
        """Test keyword extraction."""
        text = "Git push failed due to authentication error"
        keywords = detector.extract_keywords(text)
        
        # Should extract meaningful words, ignore stop words
        assert 'git' in keywords
        assert 'push' in keywords
        assert 'failed' in keywords
        assert 'authentication' in keywords
        assert 'error' in keywords
        
        # Should not contain stop words
        assert 'to' not in keywords
        # 'due' is not in stop words list, so it may be included
    
    def test_categorize_entry(self, detector):
        """Test entry categorization."""
        assert detector.categorize_entry("Error occurred during git push") == 'error'
        assert detector.categorize_entry("Actually, this is wrong") == 'correction'
        assert detector.categorize_entry("Security vulnerability detected") == 'security'
        assert detector.categorize_entry("Test coverage is low") == 'testing'
        assert detector.categorize_entry("Git branch workflow") == 'git_workflow'
        assert detector.categorize_entry("Random text") == 'general'
    
    def test_compute_similarity(self, detector):
        """Test Jaccard similarity computation."""
        kw1 = {'git', 'push', 'failed'}
        kw2 = {'git', 'push', 'error'}
        
        similarity = detector.compute_similarity(kw1, kw2)
        
        # Should be high (2/4 = 0.5)
        assert 0.4 <= similarity <= 0.6
        
        # Test with disjoint sets
        kw3 = {'test', 'coverage'}
        similarity_disjoint = detector.compute_similarity(kw1, kw3)
        assert similarity_disjoint == 0.0
        
        # Test with identical sets
        similarity_identical = detector.compute_similarity(kw1, kw1)
        assert similarity_identical == 1.0
    
    def test_parse_entry(self, detector):
        """Test parsing markdown entries."""
        content = """# ERRORS

## [ERR-001] Test Error

**Logged**: 2026-03-09T10:00:00Z
**Priority**: high

### Summary
This is a test error entry

### Context
Testing the parser
"""
        
        entries = detector.parse_entry(content, 'test-agent', 'ERRORS')
        
        assert len(entries) == 1
        assert entries[0]['title'] == '[ERR-001] Test Error'
        assert 'test error entry' in entries[0]['content']
        assert entries[0]['agent_id'] == 'test-agent'
        assert entries[0]['file_type'] == 'ERRORS'
        assert 'test' in entries[0]['keywords']
        assert 'error' in entries[0]['keywords']
    
    def test_scan_agent_files(self, detector, fixture_agents_dir):
        """Test scanning agent learning files."""
        entries = detector.scan_agent_files()
        
        # Should find entries from 3 test agents
        # Each has ERRORS.md and LEARNINGS.md with 2 entries each
        assert len(entries) >= 6  # At least 6 entries
        
        # Check agent IDs are captured
        agent_ids = {entry['agent_id'] for entry in entries}
        assert 'faintech-test1' in agent_ids
        assert 'faintech-test2' in agent_ids
        assert 'faintech-test3' in agent_ids
    
    def test_cluster_patterns(self, detector):
        """Test pattern clustering."""
        entries = detector.scan_agent_files()
        detector.cluster_patterns(entries)
        
        # Should identify patterns
        assert len(detector.patterns) > 0
        
        # Check pattern structure
        for pattern_key, pattern_data in detector.patterns.items():
            assert 'count' in pattern_data
            assert 'agents' in pattern_data
            assert 'entries' in pattern_data
            assert pattern_data['count'] > 0
    
    def test_detect_git_pattern(self, detector):
        """Test detection of recurring git authentication pattern."""
        results = detector.detect()
        
        # Should detect git auth pattern across multiple agents
        candidates = results['promotion_candidates']
        
        # Should have some promotion candidates
        assert len(candidates) > 0
        
        # Check for git-related pattern (appears in test1 and test2)
        # Pattern names are built from top keywords, so check sample entries too
        git_patterns = [
            c for c in candidates 
            if 'git' in c['pattern'].lower() or 
               any('git' in e.get('title', '').lower() for e in c.get('sample_entries', []))
        ]
        assert len(git_patterns) > 0, "Should detect git-related pattern"
        
        # Verify structure
        for candidate in candidates:
            assert 'pattern' in candidate
            assert 'frequency' in candidate
            assert 'affected_agents' in candidate
            assert 'suggested_rule' in candidate
            assert 'priority' in candidate
            assert candidate['priority'] in ['HIGH', 'MEDIUM', 'LOW']
    
    def test_detect_security_pattern(self, detector):
        """Test detection of security-related patterns."""
        results = detector.detect()
        
        # Check for security patterns
        security_patterns = [
            c for c in results['promotion_candidates']
            if 'security' in c['pattern'].lower() or 
               any('security' in e.get('title', '').lower() 
                   for e in c.get('sample_entries', []))
        ]
        
        # test3 has security errors
        assert len(security_patterns) > 0, "Should detect security pattern"
    
    def test_priority_assignment(self, detector):
        """Test priority assignment based on frequency and agent count."""
        results = detector.detect()
        
        for candidate in results['promotion_candidates']:
            freq = candidate['frequency']
            num_agents = candidate['num_agents']
            
            # HIGH: 3+ occurrences across 2+ agents
            if freq >= 3 and num_agents >= 2:
                assert candidate['priority'] == 'HIGH'
            # MEDIUM: 3+ occurrences in 1 agent
            elif freq >= 3:
                assert candidate['priority'] == 'MEDIUM'
            # LOW: 2 occurrences
            elif freq >= 2:
                assert candidate['priority'] == 'LOW'
    
    def test_output_format(self, detector):
        """Test output JSON format."""
        results = detector.detect()
        
        # Check metadata
        assert 'metadata' in results
        metadata = results['metadata']
        assert 'scan_timestamp' in metadata
        assert 'agents_directory' in metadata
        assert 'total_entries_scanned' in metadata
        assert 'total_patterns_found' in metadata
        assert 'promotion_threshold' in metadata
        assert 'total_promotion_candidates' in metadata
        
        # Check candidates array
        assert 'promotion_candidates' in results
        assert isinstance(results['promotion_candidates'], list)
        
        # Verify candidate structure
        if results['promotion_candidates']:
            candidate = results['promotion_candidates'][0]
            required_fields = [
                'pattern', 'frequency', 'affected_agents', 'num_agents',
                'suggested_rule', 'priority', 'sample_entries', 'detected_at'
            ]
            for field in required_fields:
                assert field in candidate, f"Missing field: {field}"
    
    def test_threshold_filtering(self, fixture_agents_dir):
        """Test that threshold filters correctly."""
        # Higher threshold should result in fewer candidates
        detector_low = PatternDetector(agents_dir=str(fixture_agents_dir), threshold=1)
        detector_high = PatternDetector(agents_dir=str(fixture_agents_dir), threshold=5)
        
        results_low = detector_low.detect()
        results_high = detector_high.detect()
        
        # Lower threshold should have more or equal candidates
        assert len(results_low['promotion_candidates']) >= len(results_high['promotion_candidates'])
    
    def test_empty_directory(self, tmp_path):
        """Test handling of empty agents directory."""
        empty_dir = tmp_path / "agents"
        empty_dir.mkdir()
        
        detector = PatternDetector(agents_dir=str(empty_dir))
        results = detector.detect()
        
        assert results['metadata']['total_entries_scanned'] == 0
        assert results['metadata']['total_patterns_found'] == 0
        assert len(results['promotion_candidates']) == 0
    
    def test_suggest_rule(self, detector):
        """Test rule suggestion generation."""
        # Test different categories
        error_rule = detector.suggest_rule('git_push', 'error', 3)
        assert 'git_push' in error_rule.lower()
        assert 'check' in error_rule.lower() or 'escalate' in error_rule.lower()
        
        security_rule = detector.suggest_rule('api_key', 'security', 2)
        assert 'security' in security_rule.lower() or 'validate' in security_rule.lower()
        
        git_rule = detector.suggest_rule('branch', 'git_workflow', 4)
        assert 'git' in git_rule.lower() or 'branch' in git_rule.lower()


class TestIntegration:
    """Integration tests with real fixture data."""
    
    def test_full_pipeline(self, detector):
        """Test complete detection pipeline."""
        results = detector.detect()
        
        # Should successfully process all fixture data
        assert results['metadata']['total_entries_scanned'] > 0
        assert results['metadata']['total_patterns_found'] > 0
        
        # Should generate valid JSON output
        output_str = json.dumps(results, indent=2)
        assert len(output_str) > 0
        
        # Should be parseable
        parsed = json.loads(output_str)
        assert parsed == results
    
    def test_real_patterns_detected(self, detector):
        """Test that expected patterns are detected from fixtures."""
        results = detector.detect()
        
        candidates = results['promotion_candidates']
        
        # Should detect git-related patterns (present in test1 and test2)
        git_patterns = [
            c for c in candidates 
            if 'git' in c['pattern'].lower() or 
               any('git' in e.get('title', '').lower() for e in c.get('sample_entries', []))
        ]
        assert len(git_patterns) > 0, "Should detect git authentication pattern"
        
        # Should detect security patterns (present in test3)
        security_keywords = ['security', 'permission', 'auth']
        has_security = any(
            any(keyword in c['pattern'].lower() for keyword in security_keywords) or
            any(any(keyword in e.get('title', '').lower() for keyword in security_keywords)
                for e in c.get('sample_entries', []))
            for c in candidates
        )
        assert has_security, "Should detect security-related pattern"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
