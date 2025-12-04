"""
Command-line interface for markdown-consolidator.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import NoReturn


def main() -> int:
    """
    Main entry point for mdconsolidate command.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        prog='mdconsolidate',
        description='Consolidate markdown files with intelligent synthesis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./docs ./consolidated
  %(prog)s ./notes ./merged --strategy comprehensive
  %(prog)s ./kb ./kb-out --threshold 0.5 --method topic
        """
    )
    parser.add_argument('source', type=Path, help='Source directory')
    parser.add_argument('output', type=Path, help='Output directory')
    parser.add_argument(
        '--strategy', '-s',
        choices=['authority', 'comprehensive', 'canonical'],
        default='authority',
        help='Merge strategy (default: authority)'
    )
    parser.add_argument(
        '--threshold', '-t',
        type=float, default=0.5,
        help='Similarity threshold (default: 0.5)'
    )
    parser.add_argument(
        '--method', '-m',
        choices=['topic', 'temporal', 'hierarchical', 'links', 'all'],
        default='topic',
        help='Clustering method (default: topic)'
    )
    parser.add_argument(
        '--exclude', '-e',
        nargs='*', default=[],
        help='Patterns to exclude'
    )
    parser.add_argument(
        '--keep-work', '-k',
        action='store_true',
        help='Keep intermediate work files'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output'
    )
    parser.add_argument(
        '--version', '-V',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    if not args.source.is_dir():
        print(f"Error: {args.source} is not a directory", file=sys.stderr)
        return 1
    
    from .consolidator import consolidate
    
    if not args.quiet:
        print("╔══════════════════════════════════════════════════════════╗")
        print("║  Markdown Consolidator                                    ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print(f"  Source:    {args.source}")
        print(f"  Output:    {args.output}")
        print(f"  Strategy:  {args.strategy}")
        print(f"  Threshold: {args.threshold}")
        print(f"  Method:    {args.method}")
        print()
    
    try:
        result = consolidate(
            source_dir=args.source,
            output_dir=args.output,
            strategy=args.strategy,
            threshold=args.threshold,
            method=args.method,
            exclude_patterns=args.exclude,
            keep_work_files=args.keep_work
        )
        
        if not args.quiet:
            print(f"✓ Consolidation complete!")
            print(f"  Files analyzed:    {result['files_analyzed']}")
            print(f"  Clusters created:  {result['clusters_created']}")
            print(f"  Files created:     {result['files_created']}")
            print(f"  Coverage:          {result['coverage']}%")
            
            if result['validation'].get('broken_links'):
                print(f"  ⚠️  Broken links:   {len(result['validation']['broken_links'])}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def inventory_cmd() -> int:
    """
    Entry point for mdconsolidate-inventory command.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        prog='mdconsolidate-inventory',
        description='Inventory markdown files in a directory'
    )
    parser.add_argument('directory', type=Path, help='Directory to analyze')
    parser.add_argument(
        '--output', '-o',
        type=Path, default=Path('inventory.json'),
        help='Output JSON file'
    )
    parser.add_argument('--exclude', '-e', nargs='*', default=[])
    parser.add_argument('--pretty', '-p', action='store_true')
    
    args = parser.parse_args()
    
    if not args.directory.is_dir():
        print(f"Error: {args.directory} is not a directory", file=sys.stderr)
        return 1
    
    from .inventory import inventory_directory
    
    print(f"Analyzing markdown files in {args.directory}...")
    files = inventory_directory(directory=args.directory, exclude_patterns=args.exclude)
    
    output = {
        'source_directory': str(args.directory.absolute()),
        'analyzed_at': datetime.now().isoformat(),
        'file_count': len(files),
        'total_words': sum(f.get('word_count', 0) for f in files if 'error' not in f),
        'files': files
    }
    
    indent = 2 if args.pretty else None
    args.output.write_text(json.dumps(output, indent=indent, default=str))
    
    print(f"Inventoried {len(files)} files → {args.output}")
    return 0


def analyze_cmd() -> int:
    """
    Entry point for mdconsolidate-analyze command.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        prog='mdconsolidate-analyze',
        description='Analyze relationships between markdown files'
    )
    parser.add_argument('inventory', type=Path, help='Inventory JSON file')
    parser.add_argument(
        '--output', '-o',
        type=Path, default=Path('relationships.json'),
        help='Output JSON file'
    )
    parser.add_argument('--threshold', '-t', type=float, default=0.3)
    parser.add_argument('--pretty', '-p', action='store_true')
    
    args = parser.parse_args()
    
    if not args.inventory.exists():
        print(f"Error: {args.inventory} not found", file=sys.stderr)
        return 1
    
    from .relationships import analyze_relationships
    
    inventory = json.loads(args.inventory.read_text())
    
    print("Analyzing relationships...")
    relationships = analyze_relationships(inventory=inventory, threshold=args.threshold)
    
    output = {
        'analyzed_at': datetime.now().isoformat(),
        'source_inventory': str(args.inventory),
        'similarity_threshold': args.threshold,
        **relationships,
        'summary': {
            'similar_pairs': len(relationships['content_similarities']),
            'section_overlaps': len(relationships['section_overlaps']),
            'link_clusters': len(relationships['link_relationships']['link_clusters']),
            'temporal_chains': len(relationships['temporal_chains']),
            'potential_conflicts': len(relationships['potential_conflicts'])
        }
    }
    
    indent = 2 if args.pretty else None
    args.output.write_text(json.dumps(output, indent=indent, default=str))
    
    print(f"Analysis complete → {args.output}")
    print(f"  Similar pairs: {output['summary']['similar_pairs']}")
    print(f"  Conflicts: {output['summary']['potential_conflicts']}")
    return 0


def cluster_cmd() -> int:
    """
    Entry point for mdconsolidate-cluster command.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        prog='mdconsolidate-cluster',
        description='Cluster related markdown files'
    )
    parser.add_argument('relationships', type=Path, help='Relationships JSON file')
    parser.add_argument(
        '--output', '-o',
        type=Path, default=Path('clusters.json'),
        help='Output JSON file'
    )
    parser.add_argument(
        '--method', '-m',
        choices=['topic', 'temporal', 'hierarchical', 'links', 'all'],
        default='topic'
    )
    parser.add_argument('--threshold', '-t', type=float, default=0.6)
    parser.add_argument('--pretty', '-p', action='store_true')
    
    args = parser.parse_args()
    
    if not args.relationships.exists():
        print(f"Error: {args.relationships} not found", file=sys.stderr)
        return 1
    
    from .clustering import cluster_files
    
    relationships = json.loads(args.relationships.read_text())
    
    print(f"Clustering with method: {args.method}...")
    clusters = cluster_files(relationships=relationships, method=args.method, threshold=args.threshold)
    
    output = {
        'clustered_at': datetime.now().isoformat(),
        'source_relationships': str(args.relationships),
        'method': args.method,
        'threshold': args.threshold,
        'cluster_count': len(clusters),
        'total_files_clustered': len(set(f for c in clusters for f in c['files'])),
        'clusters': clusters
    }
    
    indent = 2 if args.pretty else None
    args.output.write_text(json.dumps(output, indent=indent, default=str))
    
    print(f"Clustering complete → {args.output}")
    print(f"  Clusters: {len(clusters)}")
    return 0


def synthesize_cmd() -> int:
    """
    Entry point for mdconsolidate-synthesize command.

    Returns
    -------
    int
        Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        prog='mdconsolidate-synthesize',
        description='Synthesize consolidated files from clusters'
    )
    parser.add_argument('clusters', type=Path, help='Clusters JSON file')
    parser.add_argument(
        '--output', '-o',
        type=Path, default=Path('consolidated'),
        help='Output directory'
    )
    parser.add_argument(
        '--strategy', '-s',
        choices=['authority', 'comprehensive', 'canonical'],
        default='authority'
    )
    
    args = parser.parse_args()
    
    if not args.clusters.exists():
        print(f"Error: {args.clusters} not found", file=sys.stderr)
        return 1
    
    from .synthesis import synthesize_all
    
    clusters_data = json.loads(args.clusters.read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    
    print(f"Synthesizing with strategy: {args.strategy}...")
    results = synthesize_all(
        clusters=clusters_data['clusters'],
        output_dir=args.output,
        strategy=args.strategy,
    )
    
    print(f"Synthesis complete → {args.output}")
    print(f"  Files created: {len(results)}")
    for r in results:
        print(f"    → {Path(r['output_file']).name}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
