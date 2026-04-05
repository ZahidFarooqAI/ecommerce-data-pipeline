#!/usr/bin/env python3
"""
Test script to verify the ecommerce data pipeline components.
Run this to ensure everything is working locally.
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from src.config import DATA_FILE, PROCESSED_FILE
        from src.ingestion.processing.clean_data import clean_local_data
        from src.dashboard.app import load_local_data
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_cleaning():
    """Test that data cleaning works."""
    try:
        from src.ingestion.processing.clean_data import clean_local_data
        cleaned_path = clean_local_data()
        if Path(cleaned_path).exists():
            print(f"✅ Data cleaning successful: {cleaned_path}")
            return True
        else:
            print("❌ Cleaned file not found")
            return False
    except Exception as e:
        print(f"❌ Data cleaning error: {e}")
        return False

def test_dashboard_data():
    """Test that dashboard can load local data."""
    try:
        from src.dashboard.app import load_local_data
        df = load_local_data()
        if not df.empty:
            print(f"✅ Dashboard data loading successful: {len(df)} rows")
            return True
        else:
            print("❌ Dashboard data is empty")
            return False
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
        return False

def main():
    print("Testing ecommerce data pipeline...")
    print("=" * 50)

    tests = [
        ("Module imports", test_imports),
        ("Data cleaning", test_data_cleaning),
        ("Dashboard data loading", test_dashboard_data),
    ]

    passed = 0
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("🎉 All tests passed! The pipeline is ready.")
        print("\nNext steps:")
        print("1. Update src/config.py with your GCP settings")
        print("2. Run: python src/ingestion/run_pipeline.py")
        print("3. Run: streamlit run src/dashboard/app.py")
    else:
        print("❌ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
