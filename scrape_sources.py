#!/usr/bin/env python3
"""
Cannabis Source Scraper CLI
Scrapes cannabis industry supplier websites for the sourcing agent
"""

import asyncio
import argparse
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.scraper import CannabisSourceScraper

async def scrape_sources(args):
    """Main scraping function"""
    scraper = CannabisSourceScraper(args.sources_file)
    
    try:
        print("🌿 Cannabis Source Scraper")
        print("=" * 50)
        print(f"Sources file: {args.sources_file}")
        print(f"Max concurrent: {args.max_concurrent}")
        print(f"Output file: {args.output_file}")
        print()
        
        # Load sources to show count
        sources_data = scraper.sources_data
        total_sources = 0
        
        if sources_data.get('preferred_sources'):
            total_sources += len(sources_data['preferred_sources'])
        
        if sources_data.get('sources_by_state'):
            for state, state_data in sources_data['sources_by_state'].items():
                if state_data.get('materials'):
                    total_sources += len(state_data['materials'])
                if state_data.get('equipment'):
                    total_sources += len(state_data['equipment'])
        
        if sources_data.get('national_suppliers'):
            if sources_data['national_suppliers'].get('materials'):
                total_sources += len(sources_data['national_suppliers']['materials'])
            if sources_data['national_suppliers'].get('equipment'):
                total_sources += len(sources_data['national_suppliers']['equipment'])
        
        print(f"Found {total_sources} sources to scrape")
        print()
        
        if args.dry_run:
            print("DRY RUN MODE - No actual scraping will be performed")
            print("Sources that would be scraped:")
            
            # Show sources that would be scraped
            if sources_data.get('preferred_sources'):
                print("\nPreferred Sources:")
                for source in sources_data['preferred_sources']:
                    print(f"  ⭐ {source['name']} - {source['url']}")
            
            if sources_data.get('sources_by_state'):
                print("\nState Sources:")
                for state, state_data in sources_data['sources_by_state'].items():
                    print(f"\n  {state.upper()}:")
                    if state_data.get('materials'):
                        for source in state_data['materials']:
                            print(f"    📦 {source['name']} - {source['url']}")
                    if state_data.get('equipment'):
                        for source in state_data['equipment']:
                            print(f"    🔧 {source['name']} - {source['url']}")
            
            return
        
        # Start scraping
        print("Starting scraping process...")
        start_time = datetime.now()
        
        results = await scraper.scrape_all_sources(max_concurrent=args.max_concurrent)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Display results
        print("\n" + "=" * 50)
        print("SCRAPING RESULTS")
        print("=" * 50)
        print(f"Total sources: {results['total_sources']}")
        print(f"Successful scrapes: {results['successful_scrapes']}")
        print(f"Failed scrapes: {results['failed_scrapes']}")
        print(f"Success rate: {(results['successful_scrapes'] / results['total_sources'] * 100):.1f}%")
        print(f"Duration: {duration}")
        print()
        
        if results['successful_scrapes'] > 0:
            print("✅ Successfully scraped sources:")
            for result in results['results'][:5]:  # Show first 5
                print(f"  • {result['title']} - {result['url']}")
            if len(results['results']) > 5:
                print(f"  ... and {len(results['results']) - 5} more")
            print()
        
        if results['failed_scrapes'] > 0:
            print("❌ Failed scrapes:")
            for failure in results['failures'][:5]:  # Show first 5
                if isinstance(failure, dict):
                    url = failure.get('url', 'Unknown URL')
                    error = failure.get('error', 'Unknown error')
                    print(f"  • {url} - {error}")
                else:
                    print(f"  • {failure}")
            if len(results['failures']) > 5:
                print(f"  ... and {len(results['failures']) - 5} more")
            print()
        
        # Save results
        if args.output_file:
            scraper.save_scraped_data(results, args.output_file)
            print(f"📁 Results saved to: {args.output_file}")
        else:
            scraper.save_scraped_data(results)
            print("📁 Results saved to sources/scraped_data_[timestamp].json")
        
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        return 1
    finally:
        await scraper.close_session()
    
    return 0

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape cannabis industry supplier websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_sources.py                    # Scrape all sources
  python scrape_sources.py --dry-run          # Show what would be scraped
  python scrape_sources.py --max-concurrent 3 # Limit concurrent requests
  python scrape_sources.py --output results.json # Save to specific file
        """
    )
    
    parser.add_argument(
        '--sources-file',
        default='sources/sources.json',
        help='Path to sources JSON file (default: sources/sources.json)'
    )
    
    parser.add_argument(
        '--max-concurrent',
        type=int,
        default=5,
        help='Maximum concurrent requests (default: 5)'
    )
    
    parser.add_argument(
        '--output-file',
        help='Output file for scraped data (default: auto-generated)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be scraped without actually scraping'
    )
    
    args = parser.parse_args()
    
    # Check if sources file exists
    if not os.path.exists(args.sources_file):
        print(f"❌ Sources file not found: {args.sources_file}")
        print("Please create the sources.json file first.")
        return 1
    
    # Run the scraper
    return asyncio.run(scrape_sources(args))

if __name__ == "__main__":
    sys.exit(main()) 