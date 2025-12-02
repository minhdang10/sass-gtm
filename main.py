"""
Main orchestration script for SaaS Security GTM Tracker
Runs weekly data collection and generates output files
"""

import os
import sys
from datetime import datetime
from hiring_tracker import HiringTracker
from conversation_tracker import ConversationTracker
from data_processor import DataProcessor
from config import OUTPUT_DIR

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("SaaS Security GTM Signal Tracker")
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Initialize components
    hiring_tracker = HiringTracker()
    conversation_tracker = ConversationTracker()
    data_processor = DataProcessor()
    
    # 1. Collect Hiring Signals
    print("\n[1/2] Collecting Hiring Signals...")
    print("-" * 60)
    companies = hiring_tracker.collect_hiring_signals()
    
    # Process and deduplicate
    company_list = list(companies.values())
    company_list = data_processor.deduplicate_companies(company_list)
    
    # Enrich data
    for company in company_list:
        data_processor.enrich_company_data(company)
    
    # Rank companies
    ranked_companies = hiring_tracker.rank_companies(companies)
    
    # Generate output
    hiring_df = hiring_tracker.generate_output(ranked_companies)
    hiring_output_path = os.path.join(OUTPUT_DIR, "hiring_signals.csv")
    hiring_df.to_csv(hiring_output_path, index=False)
    print(f"\n✓ Hiring signals saved to: {hiring_output_path}")
    print(f"  Total companies identified: {len(ranked_companies)}")
    
    # 2. Collect Conversation Signals
    print("\n[2/2] Collecting Conversation Signals...")
    print("-" * 60)
    people, publishers = conversation_tracker.collect_conversation_signals()
    
    # Rank people and publishers
    ranked_people = conversation_tracker.rank_people(people)
    ranked_publishers = conversation_tracker.rank_publishers(publishers)
    
    # Generate outputs
    people_df = conversation_tracker.generate_people_output(ranked_people)
    people_output_path = os.path.join(OUTPUT_DIR, "conversation_signals_people.csv")
    people_df.to_csv(people_output_path, index=False)
    print(f"\n✓ People signals saved to: {people_output_path}")
    print(f"  Total people identified: {len(ranked_people)}")
    
    publishers_df = conversation_tracker.generate_publishers_output(ranked_publishers)
    publishers_output_path = os.path.join(OUTPUT_DIR, "conversation_signals_publishers.csv")
    publishers_df.to_csv(publishers_output_path, index=False)
    print(f"\n✓ Publisher signals saved to: {publishers_output_path}")
    print(f"  Total publishers identified: {len(ranked_publishers)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Data Collection Complete!")
    print("=" * 60)
    print(f"\nOutput Files:")
    print(f"  1. {hiring_output_path}")
    print(f"  2. {people_output_path}")
    print(f"  3. {publishers_output_path}")
    print(f"\nNext Steps:")
    print(f"  - Review the CSV files for actionable GTM signals")
    print(f"  - Schedule weekly runs (cron job or GitHub Actions)")
    print(f"  - Configure API credentials for full data access")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

