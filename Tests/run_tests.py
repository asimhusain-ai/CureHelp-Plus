#!/usr/bin/env python3
"""
Test Runner for CureHelp+ Unit Tests
Runs all tests and provides a summary report
"""

import unittest
import sys
import os
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests(verbosity=2):
    """
    Run all unit tests and return results
    
    Args:
        verbosity (int): Level of detail in output (0=quiet, 1=normal, 2=verbose)
    
    Returns:
        unittest.TestResult: Test results object
    """
    # Discover and load all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with custom result
    runner = unittest.TextTestRunner(verbosity=verbosity, stream=sys.stdout)
    result = runner.run(suite)
    
    return result


def print_summary(result):
    """
    Print a summary of test results
    
    Args:
        result (unittest.TestResult): Test results object
    """
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    successes = total_tests - failures - errors - skipped
    
    print(f"Total Tests Run: {total_tests}")
    print(f"Successes: {successes}")
    print(f"Failures: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")
        
        if failures > 0:
            print(f"\n{failures} test(s) failed:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if errors > 0:
            print(f"\n{errors} test(s) had errors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
    
    print("="*70)
    
    # Calculate success rate
    if total_tests > 0:
        success_rate = (successes / total_tests) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    return result.wasSuccessful()


def run_specific_module(module_name, verbosity=2):
    """
    Run tests for a specific module
    
    Args:
        module_name (str): Name of test module (e.g., 'test_helper')
        verbosity (int): Level of detail in output
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    loader = unittest.TestLoader()
    
    try:
        # Load the specific module
        suite = loader.loadTestsFromName(module_name)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=verbosity, stream=sys.stdout)
        result = runner.run(suite)
        
        return result.wasSuccessful()
    
    except Exception as e:
        print(f"Error loading module '{module_name}': {e}")
        return False


def main():
    """Main entry point for test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run CureHelp+ Unit Tests')
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=2,
        help='Increase verbosity (can be used multiple times)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimal output'
    )
    parser.add_argument(
        '-m', '--module',
        type=str,
        help='Run tests for specific module (e.g., test_helper)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available test modules'
    )
    
    args = parser.parse_args()
    
    # Determine verbosity level
    if args.quiet:
        verbosity = 0
    else:
        verbosity = args.verbose
    
    # List available modules
    if args.list:
        print("Available test modules:")
        test_dir = os.path.dirname(os.path.abspath(__file__))
        for file in os.listdir(test_dir):
            if file.startswith('test_') and file.endswith('.py'):
                print(f"  - {file[:-3]}")
        return 0
    
    # Run specific module or all tests
    if args.module:
        print(f"Running tests for module: {args.module}")
        success = run_specific_module(args.module, verbosity)
    else:
        print("Running all CureHelp+ unit tests...")
        result = run_all_tests(verbosity)
        success = print_summary(result)
    
    # Return exit code
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
