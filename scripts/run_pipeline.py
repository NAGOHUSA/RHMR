#!/usr/bin/env python3
"""
Main pipeline orchestrator - runs all collection and processing steps
"""

import sys
from pathlib import Path
from datetime import datetime
import time

# Add scripts to path
scripts_dir = Path(__file__).parent
sys.path.append(str(scripts_dir))

def run_full_pipeline(zip_codes=None):
    """Run the complete data pipeline"""
    print("="*60)
    print("🏠 REAL ESTATE DATA PIPELINE")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    
    if zip_codes is None:
        zip_codes = ["31088", "31093", "31098"]
    
    try:
        # Step 1: Collect data for each ZIP code
        print("\n📊 STEP 1: Collecting data for each ZIP code...")
        from free_data_collector import FreeDataCollector
        
        for zip_code in zip_codes:
            print(f"\n  Processing ZIP {zip_code}...")
            collector = FreeDataCollector(zip_code)
            data = collector.aggregate_all_data()
            print(f"  ✓ Collected {len(data.get('properties', []))} properties")
        
        # Step 2: Create dashboard JSON
        print("\n📈 STEP 2: Creating dashboard...")
        from create_dashboard_json import create_dashboard_json
        
        dashboard = create_dashboard_json()
        
        # Step 3: Generate AI insights
        print("\n🤖 STEP 3: Generating AI insights...")
        from deepseek_ai_insights import DeepSeekAIInsights
        
        ai = DeepSeekAIInsights()
        insights = ai.generate_insights()
        
        # Step 4: Generate reports
        print("\n📄 STEP 4: Generating reports...")
        generate_reports()
        
        # Calculate execution time
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Total time: {elapsed:.1f} seconds")
        print(f"ZIP codes processed: {len(zip_codes)}")
        print(f"Data saved to: data/houston-county-ga/")
        print("\nFiles generated:")
        print("  - dashboard.json (main dashboard)")
        print("  - dashboard_simple.json (simplified)")
        print("  - market_trends.json (trend data)")
        print("  - ai_insights_summary.json (AI analysis)")
        print("  - pipeline_report.txt (execution report)")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ PIPELINE FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_reports():
    """Generate pipeline execution report"""
    report_dir = Path("data/houston-county-ga/reports")
    report_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Simple report file
    report_file = report_dir / f"pipeline_report_{timestamp}.txt"
    
    with open(report_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("REAL ESTATE DATA PIPELINE REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # List all generated files
        data_dir = Path("data/houston-county-ga")
        json_files = list(data_dir.rglob("*.json"))
        
        f.write("GENERATED FILES:\n")
        f.write("-"*40 + "\n")
        for json_file in json_files:
            size_kb = json_file.stat().st_size / 1024
            f.write(f"  {json_file.relative_to(data_dir.parent)} ({size_kb:.1f} KB)\n")
    
    # Also create a status file for monitoring
    status_file = Path("data/houston-county-ga/pipeline_status.json")
    status = {
        "last_run": datetime.now().isoformat(),
        "status": "success",
        "version": "1.0.0"
    }
    
    with open(status_file, 'w') as f:
        import json
        json.dump(status, f, indent=2)

if __name__ == "__main__":
    # Run the full pipeline
    success = run_full_pipeline()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
